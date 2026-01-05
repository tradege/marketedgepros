"""
Improved MT5 Service with Retry Logic, Rate Limiting, and Better Error Handling
Synchronous version for compatibility with existing routes
"""
import os
import requests
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class MT5APIError(Exception):
    """Base exception for MT5 API errors"""
    pass


class MT5AuthenticationError(MT5APIError):
    """Authentication failed"""
    pass


class MT5AccountNotFoundError(MT5APIError):
    """Account not found"""
    pass


class MT5RateLimitError(MT5APIError):
    """Rate limit exceeded"""
    pass


class RateLimiter:
    """Simple rate limiter for API requests"""
    
    def __init__(self, max_requests=10, time_window=1.0):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        # Check if we need to wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                logger.debug(f"Rate limit reached, sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
                self.requests = []
        
        # Add current request
        self.requests.append(now)


def retry_on_failure(max_retries=3, delay=1, backoff=2):
    """
    Decorator to retry function on failure
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.Timeout, 
                       requests.exceptions.ConnectionError) as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"{func.__name__} failed after {max_retries + 1} attempts")
                except MT5AuthenticationError:
                    # Don't retry authentication errors
                    raise
                except Exception as e:
                    last_exception = e
                    logger.error(f"{func.__name__} failed with unexpected error: {e}")
                    raise
            
            raise last_exception
        
        return wrapper
    return decorator


class MT5Service:
    """Improved Service for interacting with MT5 API"""
    
    def __init__(self):
        self.api_url = os.getenv('MT5_API_URL', "http://57.129.52.174:6710")
        self.username = os.getenv('MT5_USERNAME', "backofficeApi")
        self.password = os.getenv('MT5_PASSWORD', "Trade@2022")
        self.token = None
        self.token_expires_at = None
        self.rate_limiter = RateLimiter(max_requests=10, time_window=1.0)
        
        # Setup session with connection pooling and retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def authenticate(self) -> str:
        """
        Get JWT token from MT5 API with retry logic
        Token expires in 2 minutes, refresh 30 seconds before expiration
        """
        # Check if token is still valid
        if self.token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.token
        
        self.rate_limiter.wait_if_needed()
        
        try:
            url = f"{self.api_url}/Home/token"
            payload = {
                "userName": self.username,
                "password": self.password
            }
            
            response = self.session.post(url, json=payload, timeout=10)
            
            if response.status_code == 401:
                raise MT5AuthenticationError("Invalid credentials")
            
            response.raise_for_status()
            
            data = response.json()
            self.token = data.get('token')
            
            if not self.token:
                raise MT5AuthenticationError("No token received from API")
            
            # Token expires in 2 minutes, refresh 30 seconds before
            self.token_expires_at = datetime.now() + timedelta(seconds=90)
            
            logger.info("MT5 API authentication successful")
            return self.token
            
        except requests.exceptions.Timeout:
            logger.error("MT5 authentication timeout")
            raise MT5APIError("Authentication timeout - MT5 API not responding")
        except requests.exceptions.ConnectionError:
            logger.error("MT5 authentication connection error")
            raise MT5APIError("Cannot connect to MT5 API - check network/firewall")
        except MT5AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"MT5 authentication failed: {e}")
            raise MT5APIError(f"Authentication failed: {str(e)}")
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def create_account(self, name: str, group: str = "demo\\demoforex", 
                      leverage: int = 100, balance: float = 10000) -> Dict:
        """
        Create new MT5 trading account with retry logic
        
        Args:
            name: Account holder name
            group: MT5 group (default: demo\\demoforex)
            leverage: Account leverage (default: 100)
            balance: Initial balance (default: 10000)
            
        Returns:
            Dict with account details including login and password
            
        Raises:
            MT5APIError: If account creation fails
        """
        try:
            token = self.authenticate()
            self.rate_limiter.wait_if_needed()
            
            headers = {"Authorization": f"Bearer {token}"}
            
            url = f"{self.api_url}/Home/createAccount"
            payload = {
                "name": name,
                "group": group,
                "leverage": leverage,
                "balance": balance,
                "enable": True,
                "enableChangePassword": True,
                "enableReadOnly": False
            }
            
            response = self.session.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 404:
                raise MT5APIError(f"Group '{group}' not found")
            elif response.status_code == 400:
                error_msg = response.json().get('message', 'Bad request')
                raise MT5APIError(f"Invalid account parameters: {error_msg}")
            
            response.raise_for_status()
            
            account_data = response.json()
            
            if not account_data.get('login'):
                raise MT5APIError("Account created but no login received")
            
            logger.info(f"MT5 account created successfully: {account_data.get('login')}")
            return account_data
            
        except MT5APIError:
            raise
        except requests.exceptions.Timeout:
            raise MT5APIError("Account creation timeout - MT5 API not responding")
        except Exception as e:
            logger.error(f"Failed to create MT5 account: {e}")
            raise MT5APIError(f"Account creation failed: {str(e)}")
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def get_account_info(self, mt5_login: str) -> Dict:
        """
        Get account information from MT5 with retry logic
        
        Args:
            mt5_login: MT5 account login number
            
        Returns:
            Dict with account information
            
        Raises:
            MT5AccountNotFoundError: If account doesn't exist
            MT5APIError: If request fails
        """
        try:
            token = self.authenticate()
            self.rate_limiter.wait_if_needed()
            
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.api_url}/Home/getAccount"
            params = {"login": mt5_login}
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 404:
                raise MT5AccountNotFoundError(f"Account {mt5_login} not found")
            
            response.raise_for_status()
            
            account_data = response.json()
            logger.debug(f"Retrieved account info for {mt5_login}")
            return account_data
            
        except MT5AccountNotFoundError:
            raise
        except requests.exceptions.Timeout:
            raise MT5APIError(f"Timeout getting account {mt5_login}")
        except Exception as e:
            logger.error(f"Failed to get account info for {mt5_login}: {e}")
            raise MT5APIError(f"Failed to get account info: {str(e)}")
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def get_positions(self, mt5_login: str) -> List[Dict]:
        """
        Get open positions for account with retry logic
        
        Args:
            mt5_login: MT5 account login number
            
        Returns:
            List of open positions
        """
        try:
            token = self.authenticate()
            self.rate_limiter.wait_if_needed()
            
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.api_url}/Home/getPositions"
            params = {"login": mt5_login}
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 404:
                raise MT5AccountNotFoundError(f"Account {mt5_login} not found")
            
            response.raise_for_status()
            
            positions = response.json()
            logger.debug(f"Retrieved {len(positions)} positions for {mt5_login}")
            return positions
            
        except MT5AccountNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get positions for {mt5_login}: {e}")
            raise MT5APIError(f"Failed to get positions: {str(e)}")
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def get_trade_history(self, mt5_login: str, start_date: datetime, 
                         end_date: datetime = None) -> List[Dict]:
        """
        Get trade history for account with retry logic
        
        Args:
            mt5_login: MT5 account login number
            start_date: Start date for history
            end_date: End date for history (default: now)
            
        Returns:
            List of trades
        """
        try:
            token = self.authenticate()
            self.rate_limiter.wait_if_needed()
            
            if end_date is None:
                end_date = datetime.now()
            
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.api_url}/Home/getTradeHistory"
            params = {
                "login": mt5_login,
                "from": start_date.isoformat(),
                "to": end_date.isoformat()
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 404:
                raise MT5AccountNotFoundError(f"Account {mt5_login} not found")
            
            response.raise_for_status()
            
            trades = response.json()
            logger.debug(f"Retrieved {len(trades)} trades for {mt5_login}")
            return trades
            
        except MT5AccountNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get trade history for {mt5_login}: {e}")
            raise MT5APIError(f"Failed to get trade history: {str(e)}")
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def update_balance(self, mt5_login: str, amount: float, 
                      comment: str = "Balance adjustment") -> Dict:
        """
        Update account balance (deposit/withdrawal) with retry logic
        
        Args:
            mt5_login: MT5 account login number
            amount: Amount to add (positive) or subtract (negative)
            comment: Comment for the transaction
            
        Returns:
            Dict with updated account info
        """
        try:
            token = self.authenticate()
            self.rate_limiter.wait_if_needed()
            
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.api_url}/Home/updateBalance"
            payload = {
                "login": mt5_login,
                "amount": amount,
                "comment": comment
            }
            
            response = self.session.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 404:
                raise MT5AccountNotFoundError(f"Account {mt5_login} not found")
            elif response.status_code == 400:
                error_msg = response.json().get('message', 'Invalid amount')
                raise MT5APIError(f"Balance update failed: {error_msg}")
            
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Balance updated for {mt5_login}: {amount:+.2f}")
            return result
            
        except (MT5AccountNotFoundError, MT5APIError):
            raise
        except Exception as e:
            logger.error(f"Failed to update balance for {mt5_login}: {e}")
            raise MT5APIError(f"Balance update failed: {str(e)}")
    
    @retry_on_failure(max_retries=3, delay=1, backoff=2)
    def disable_account(self, mt5_login: str) -> Dict:
        """
        Disable MT5 account with retry logic
        
        Args:
            mt5_login: MT5 account login number
            
        Returns:
            Dict with operation result
        """
        try:
            token = self.authenticate()
            self.rate_limiter.wait_if_needed()
            
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.api_url}/Home/disableAccount"
            payload = {"login": mt5_login}
            
            response = self.session.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 404:
                raise MT5AccountNotFoundError(f"Account {mt5_login} not found")
            
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Account {mt5_login} disabled")
            return result
            
        except MT5AccountNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to disable account {mt5_login}: {e}")
            raise MT5APIError(f"Account disable failed: {str(e)}")
    
    def __del__(self):
        """Cleanup session on destruction"""
        if hasattr(self, 'session'):
            self.session.close()


# Global instance
mt5_service = MT5Service()
