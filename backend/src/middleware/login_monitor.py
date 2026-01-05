"""
Failed Login Monitoring and Brute Force Protection
Tracks failed login attempts and implements exponential backoff
"""
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
import logging

# Configure logger
logger = logging.getLogger(__name__)

# In-memory storage for failed attempts (consider Redis for production)
failed_attempts = {}
blocked_ips = {}

# Configuration
MAX_ATTEMPTS = 5  # Maximum failed attempts before blocking
BLOCK_DURATION = timedelta(minutes=15)  # How long to block
ATTEMPT_WINDOW = timedelta(minutes=5)  # Time window to count attempts


def get_client_ip():
    """
    Get the real client IP address
    Handles proxy headers (X-Forwarded-For, X-Real-IP)
    
    Returns:
        str: Client IP address
    """
    # Check for proxy headers
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, take the first one
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


def is_ip_blocked(ip_address):
    """
    Check if an IP address is currently blocked
    
    Args:
        ip_address: The IP address to check
        
    Returns:
        tuple: (is_blocked, time_remaining)
    """
    if ip_address in blocked_ips:
        block_time = blocked_ips[ip_address]
        if datetime.utcnow() < block_time:
            time_remaining = (block_time - datetime.utcnow()).total_seconds()
            return True, time_remaining
        else:
            # Block expired, remove it
            del blocked_ips[ip_address]
            if ip_address in failed_attempts:
                del failed_attempts[ip_address]
    
    return False, 0


def record_failed_login(ip_address, email=None):
    """
    Record a failed login attempt
    
    Args:
        ip_address: The IP address of the attempt
        email: Optional email address used in the attempt
    """
    now = datetime.utcnow()
    
    # Initialize or get existing attempts for this IP
    if ip_address not in failed_attempts:
        failed_attempts[ip_address] = []
    
    # Add this attempt
    failed_attempts[ip_address].append({
        'timestamp': now,
        'email': email
    })
    
    # Clean old attempts (outside the window)
    cutoff_time = now - ATTEMPT_WINDOW
    failed_attempts[ip_address] = [
        attempt for attempt in failed_attempts[ip_address]
        if attempt['timestamp'] > cutoff_time
    ]
    
    # Count recent attempts
    recent_attempts = len(failed_attempts[ip_address])
    
    # Log the failed attempt
    logger.warning(
        f"Failed login attempt from {ip_address} "
        f"(email: {email or 'unknown'}) - "
        f"Attempt {recent_attempts}/{MAX_ATTEMPTS}"
    )
    
    # Block if exceeded max attempts
    if recent_attempts >= MAX_ATTEMPTS:
        block_until = now + BLOCK_DURATION
        blocked_ips[ip_address] = block_until
        
        logger.error(
            f"IP {ip_address} blocked due to {recent_attempts} failed login attempts. "
            f"Blocked until {block_until.isoformat()}"
        )
        
        return True  # IP is now blocked
    
    return False  # Not blocked yet


def record_successful_login(ip_address):
    """
    Record a successful login (clears failed attempts)
    
    Args:
        ip_address: The IP address of the successful login
    """
    if ip_address in failed_attempts:
        del failed_attempts[ip_address]
    
    if ip_address in blocked_ips:
        del blocked_ips[ip_address]
    
    logger.info(f"Successful login from {ip_address}")


def check_rate_limit(f):
    """
    Decorator to check if IP is blocked before allowing login
    
    Usage:
        @app.route('/api/auth/login', methods=['POST'])
        @check_rate_limit
        def login():
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        ip_address = get_client_ip()
        
        # Check if IP is blocked
        is_blocked, time_remaining = is_ip_blocked(ip_address)
        
        if is_blocked:
            minutes_remaining = int(time_remaining / 60)
            logger.warning(
                f"Blocked login attempt from {ip_address} - "
                f"{minutes_remaining} minutes remaining"
            )
            
            return jsonify({
                'error': 'Too many failed login attempts',
                'message': f'Your IP has been temporarily blocked. Please try again in {minutes_remaining} minutes.',
                'retry_after': int(time_remaining)
            }), 429  # Too Many Requests
        
        return f(*args, **kwargs)
    
    return decorated


def get_failed_attempts_stats():
    """
    Get statistics about failed login attempts
    For admin dashboard
    
    Returns:
        dict: Statistics about failed attempts and blocked IPs
    """
    now = datetime.utcnow()
    
    # Count active blocks
    active_blocks = sum(1 for block_time in blocked_ips.values() if block_time > now)
    
    # Count recent attempts (last hour)
    recent_attempts = 0
    for attempts in failed_attempts.values():
        recent_attempts += sum(
            1 for attempt in attempts
            if attempt['timestamp'] > now - timedelta(hours=1)
        )
    
    return {
        'active_blocks': active_blocks,
        'recent_attempts_1h': recent_attempts,
        'total_tracked_ips': len(failed_attempts),
        'blocked_ips': [
            {
                'ip': ip,
                'blocked_until': block_time.isoformat(),
                'time_remaining': int((block_time - now).total_seconds())
            }
            for ip, block_time in blocked_ips.items()
            if block_time > now
        ]
    }
