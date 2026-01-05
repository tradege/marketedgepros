"""
MT5 Challenge Service
Handles automatic MT5 account creation when user purchases a challenge
"""
import logging
from datetime import datetime
from src.database import db
from src.models.mt5_models import MT5Account
from src.models.trading_program import Challenge, TradingProgram
from src.services.mt5_service import mt5_service
from cryptography.fernet import Fernet
import os

logger = logging.getLogger(__name__)


class MT5ChallengeService:
    """Service for managing MT5 accounts for challenges"""
    
    @staticmethod
    async def create_mt5_account_for_challenge(challenge_id):
        """
        Create MT5 account when challenge is paid
        
        Args:
            challenge_id: Challenge ID
            
        Returns:
            dict: MT5 account data or None if failed
        """
        try:
            # Get challenge with program details
            challenge = Challenge.query.get(challenge_id)
            if not challenge:
                logger.error(f"Challenge {challenge_id} not found")
                return None
            
            # Check if MT5 account already exists
            existing_account = MT5Account.query.filter_by(challenge_id=challenge_id).first()
            if existing_account:
                logger.warning(f"MT5 account already exists for challenge {challenge_id}")
                return existing_account.to_dict()
            
            # Get program details
            program = TradingProgram.query.get(challenge.program_id)
            if not program:
                logger.error(f"Program {challenge.program_id} not found")
                return None
            
            # Determine account parameters based on program
            account_params = MT5ChallengeService._get_account_parameters(program, challenge)
            
            # Create MT5 account via API
            logger.info(f"Creating MT5 account for challenge {challenge_id}")
            mt5_data = await mt5_service.create_account(
                name=f"User {challenge.user_id} - Challenge {challenge_id}",
                group=account_params['group'],
                leverage=account_params['leverage'],
                balance=account_params['balance']
            )
            
            if not mt5_data or 'login' not in mt5_data:
                logger.error(f"Failed to create MT5 account for challenge {challenge_id}")
                return None
            
            # Save MT5 account to database
            mt5_account = MT5Account(
                user_id=challenge.user_id,
                challenge_id=challenge_id,
                mt5_login=mt5_data.get('login'),
                mt5_password_encrypted=mt5_data.get('password'),  # Will be encrypted by model
                mt5_group=mt5_data.get('group'),
                mt5_server=os.getenv('MT5_SERVER', '185.56.137.162:443'),
                balance=account_params['balance'],
                equity=account_params['balance'],
                status='active'
            )
            
            db.session.add(mt5_account)
            
            # Update challenge with MT5 account number
            challenge.account_number = str(mt5_data.get('login'))
            challenge.status = 'active'
            
            db.session.commit()
            
            logger.info(f"MT5 account {mt5_account.mt5_login} created for challenge {challenge_id}")
            
            return {
                'mt5_login': mt5_account.mt5_login,
                'mt5_password': mt5_data.get('password'),  # Return plain password once
                'mt5_server': mt5_account.mt5_server,
                'balance': mt5_account.balance,
                'leverage': account_params['leverage']
            }
            
        except Exception as e:
            logger.error(f"Failed to create MT5 account for challenge {challenge_id}: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def _get_account_parameters(program, challenge):
        """
        Get MT5 account parameters based on program and challenge
        
        Args:
            program: TradingProgram instance
            challenge: Challenge instance
            
        Returns:
            dict: Account parameters
        """
        # Determine account balance
        balance = challenge.initial_balance or program.account_size or 10000
        
        # Determine leverage (default 1:100)
        leverage = 100
        if hasattr(program, 'leverage') and program.leverage:
            leverage = program.leverage
        
        # Determine MT5 group based on account size and type
        # Format: demo\demoforex or live\liveforex
        account_type = "demo"  # Start with demo for challenges
        
        # Group naming convention based on balance
        if balance <= 10000:
            group = f"{account_type}\\{account_type}forex-10k"
        elif balance <= 25000:
            group = f"{account_type}\\{account_type}forex-25k"
        elif balance <= 50000:
            group = f"{account_type}\\{account_type}forex-50k"
        elif balance <= 100000:
            group = f"{account_type}\\{account_type}forex-100k"
        else:
            group = f"{account_type}\\{account_type}forex-200k"
        
        return {
            'balance': float(balance),
            'leverage': int(leverage),
            'group': group,
            'account_type': account_type
        }
    
    @staticmethod
    async def disable_mt5_account_for_challenge(challenge_id, reason="Challenge ended"):
        """
        Disable MT5 account when challenge ends/fails
        
        Args:
            challenge_id: Challenge ID
            reason: Reason for disabling
            
        Returns:
            bool: Success status
        """
        try:
            # Get MT5 account
            mt5_account = MT5Account.query.filter_by(challenge_id=challenge_id).first()
            if not mt5_account:
                logger.warning(f"No MT5 account found for challenge {challenge_id}")
                return False
            
            # Disable trading via MT5 API
            await mt5_service.disable_trading(mt5_account.mt5_login)
            
            # Update database
            mt5_account.status = 'disabled'
            mt5_account.updated_at = datetime.utcnow()
            
            # Update challenge
            challenge = Challenge.query.get(challenge_id)
            if challenge:
                challenge.status = 'ended'
            
            db.session.commit()
            
            logger.info(f"MT5 account {mt5_account.mt5_login} disabled for challenge {challenge_id}: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable MT5 account for challenge {challenge_id}: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    async def update_challenge_from_mt5(challenge_id):
        """
        Update challenge progress from MT5 account data
        
        Args:
            challenge_id: Challenge ID
            
        Returns:
            dict: Updated challenge data
        """
        try:
            # Get MT5 account
            mt5_account = MT5Account.query.filter_by(challenge_id=challenge_id).first()
            if not mt5_account:
                return None
            
            # Get fresh data from MT5
            mt5_data = await mt5_service.get_account_info(mt5_account.mt5_login)
            if not mt5_data:
                return None
            
            # Update MT5 account in database
            mt5_account.balance = mt5_data.get('balance', mt5_account.balance)
            mt5_account.equity = mt5_data.get('equity', mt5_account.equity)
            mt5_account.margin = mt5_data.get('margin', mt5_account.margin)
            mt5_account.free_margin = mt5_data.get('freeMargin', mt5_account.free_margin)
            mt5_account.updated_at = datetime.utcnow()
            
            # Update challenge
            challenge = Challenge.query.get(challenge_id)
            if challenge:
                challenge.current_balance = mt5_account.balance
                
                # Calculate profit/loss
                initial_balance = challenge.initial_balance or 10000
                current_balance = mt5_account.balance or initial_balance
                
                profit_loss = current_balance - initial_balance
                if profit_loss > 0:
                    challenge.total_profit = profit_loss
                else:
                    challenge.total_loss = abs(profit_loss)
                
                # Calculate drawdown
                max_balance = challenge.max_balance or initial_balance
                if current_balance < max_balance:
                    challenge.max_drawdown = max_balance - current_balance
                else:
                    challenge.max_balance = current_balance
                
                challenge.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'balance': mt5_account.balance,
                'equity': mt5_account.equity,
                'profit_loss': profit_loss if challenge else 0,
                'drawdown': challenge.max_drawdown if challenge else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to update challenge {challenge_id} from MT5: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_mt5_credentials(challenge_id, user_id):
        """
        Get MT5 credentials for a challenge (for user only)
        
        Args:
            challenge_id: Challenge ID
            user_id: User ID (for verification)
            
        Returns:
            dict: MT5 credentials or None
        """
        try:
            # Get MT5 account
            mt5_account = MT5Account.query.filter_by(
                challenge_id=challenge_id,
                user_id=user_id
            ).first()
            
            if not mt5_account:
                return None
            
            return {
                'login': mt5_account.mt5_login,
                'password': mt5_account.get_decrypted_password(),
                'server': mt5_account.mt5_server,
                'group': mt5_account.mt5_group
            }
            
        except Exception as e:
            logger.error(f"Failed to get MT5 credentials for challenge {challenge_id}: {e}")
            return None


# Singleton instance
mt5_challenge_service = MT5ChallengeService()
