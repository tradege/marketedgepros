"""
Email Service with Celery Queue Support
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class EmailServiceAsync:
    """
    Email service that sends emails asynchronously using Celery
    """
    
    @staticmethod
    def send_welcome_email(user_email: str, user_name: str) -> bool:
        """
        Send welcome email to new user
        
        Args:
            user_email: User's email address
            user_name: User's name
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_welcome_email_task
            send_welcome_email_task.delay(user_email, user_name)
            logger.info(f'Welcome email queued for {user_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue welcome email: {str(e)}')
            return False
    
    @staticmethod
    def send_verification_email(user_email: str, user_name: str, verification_code: str) -> bool:
        """
        Send email verification code
        
        Args:
            user_email: User's email address
            user_name: User's name
            verification_code: 6-digit verification code
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_verification_email_task
            send_verification_email_task.delay(user_email, user_name, verification_code)
            logger.info(f'Verification email queued for {user_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue verification email: {str(e)}')
            return False
    
    @staticmethod
    def send_password_reset_email(user_email: str, user_name: str, reset_token: str) -> bool:
        """
        Send password reset email
        
        Args:
            user_email: User's email address
            user_name: User's name
            reset_token: Password reset token
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_password_reset_email_task
            send_password_reset_email_task.delay(user_email, user_name, reset_token)
            logger.info(f'Password reset email queued for {user_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue password reset email: {str(e)}')
            return False
    
    @staticmethod
    def send_challenge_purchased_email(user_email: str, user_name: str, 
                                      challenge_name: str, challenge_id: int) -> bool:
        """
        Send challenge purchase confirmation
        
        Args:
            user_email: User's email address
            user_name: User's name
            challenge_name: Name of the challenge
            challenge_id: Challenge ID
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_challenge_purchased_email_task
            send_challenge_purchased_email_task.delay(
                user_email, user_name, challenge_name, challenge_id
            )
            logger.info(f'Challenge purchased email queued for {user_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue challenge purchased email: {str(e)}')
            return False
    
    @staticmethod
    def send_commission_earned_email(user_email: str, user_name: str, 
                                     amount: float, commission_type: str) -> bool:
        """
        Send commission earned notification
        
        Args:
            user_email: User's email address
            user_name: User's name
            amount: Commission amount
            commission_type: Type of commission (e.g., 'Direct Referral', 'Binary')
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_commission_earned_email_task
            send_commission_earned_email_task.delay(
                user_email, user_name, amount, commission_type
            )
            logger.info(f'Commission earned email queued for {user_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue commission earned email: {str(e)}')
            return False
    
    @staticmethod
    def send_withdrawal_approved_email(user_email: str, user_name: str, amount: float) -> bool:
        """
        Send withdrawal approval notification
        
        Args:
            user_email: User's email address
            user_name: User's name
            amount: Withdrawal amount
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_withdrawal_approved_email_task
            send_withdrawal_approved_email_task.delay(user_email, user_name, amount)
            logger.info(f'Withdrawal approved email queued for {user_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue withdrawal approved email: {str(e)}')
            return False
    
    @staticmethod
    def send_custom_email(user_email: str, subject: str, template: str, 
                         context: Optional[dict] = None) -> bool:
        """
        Send custom email with template
        
        Args:
            user_email: User's email address
            subject: Email subject
            template: HTML template content
            context: Template context variables
            
        Returns:
            bool: True if task was queued successfully
        """
        try:
            from src.tasks.email_tasks import send_email_task
            send_email_task.delay(user_email, subject, template, context)
            logger.info(f'Custom email queued for {user_email}: {subject}')
            return True
        except Exception as e:
            logger.error(f'Failed to queue custom email: {str(e)}')
            return False

