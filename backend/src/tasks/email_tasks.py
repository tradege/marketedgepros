"""
Celery tasks for sending emails asynchronously using SendGrid
"""
import logging
import os
from src.celery_config import celery_app
from flask import render_template_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name='src.tasks.email_tasks.send_email')
def send_email_task(self, to, subject, template, context=None):
    """
    Send email asynchronously using SendGrid API
    
    Args:
        to: Recipient email address (string or list)
        subject: Email subject
        template: HTML template content
        context: Template context variables (dict)
    """
    try:
        from src.app import create_app
        
        app = create_app()
        
        with app.app_context():
            # Render template
            if context:
                html_content = render_template_string(template, **context)
            else:
                html_content = template
            
            # Get SendGrid configuration
            sendgrid_api_key = app.config.get('SENDGRID_API_KEY') or os.environ.get('SENDGRID_API_KEY')
            from_email = app.config.get('SENDGRID_FROM_EMAIL') or os.environ.get('SENDGRID_FROM_EMAIL', 'info@marketedgepros.com')
            
            if not sendgrid_api_key:
                raise ValueError('SENDGRID_API_KEY not configured')
            
            # Create SendGrid message
            message = Mail(
                from_email=from_email,
                to_emails=to if isinstance(to, str) else to,
                subject=subject,
                html_content=html_content
            )
            
            # Send email via SendGrid
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            
            logger.info(f'Email sent successfully to {to}: {subject} (Status: {response.status_code})')
            return {
                'status': 'success',
                'to': to,
                'subject': subject,
                'status_code': response.status_code
            }
            
    except Exception as e:
        logger.error(f'Failed to send email to {to}: {str(e)}')
        # Retry with exponential backoff (max 3 retries)
        if self.request.retries < 3:
            raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        else:
            logger.error(f'Max retries reached for email to {to}')
            raise


@celery_app.task(name='src.tasks.email_tasks.send_welcome_email')
def send_welcome_email_task(user_email, user_name):
    """Send welcome email to new user"""
    from src.utils.email_templates import get_welcome_template
    
    template = get_welcome_template()
    context = {
        'user_name': user_name,
        'login_url': 'https://app.marketedgepros.com/login'
    }
    
    return send_email_task.delay(
        to=user_email,
        subject='Welcome to MarketEdgePros!',
        template=template,
        context=context
    )


@celery_app.task(name='src.tasks.email_tasks.send_verification_email')
def send_verification_email_task(user_email, user_name, verification_code):
    """Send email verification code"""
    from src.utils.email_templates import get_verification_template
    
    template = get_verification_template()
    context = {
        'user_name': user_name,
        'verification_code': verification_code
    }
    
    return send_email_task.delay(
        to=user_email,
        subject='Verify Your Email - MarketEdgePros',
        template=template,
        context=context
    )


@celery_app.task(name='src.tasks.email_tasks.send_password_reset_email')
def send_password_reset_email_task(user_email, user_name, reset_token):
    """Send password reset email"""
    from src.utils.email_templates import get_password_reset_template
    
    template = get_password_reset_template()
    context = {
        'user_name': user_name,
        'reset_url': f'https://app.marketedgepros.com/reset-password?token={reset_token}'
    }
    
    return send_email_task.delay(
        to=user_email,
        subject='Reset Your Password - MarketEdgePros',
        template=template,
        context=context
    )


@celery_app.task(name='src.tasks.email_tasks.send_challenge_purchased_email')
def send_challenge_purchased_email_task(user_email, user_name, challenge_name, challenge_id):
    """Send challenge purchase confirmation"""
    from src.utils.email_templates import get_challenge_purchased_template
    
    template = get_challenge_purchased_template()
    context = {
        'user_name': user_name,
        'challenge_name': challenge_name,
        'challenge_url': f'https://app.marketedgepros.com/challenges/{challenge_id}'
    }
    
    return send_email_task.delay(
        to=user_email,
        subject=f'Challenge Purchased: {challenge_name}',
        template=template,
        context=context
    )


@celery_app.task(name='src.tasks.email_tasks.send_commission_earned_email')
def send_commission_earned_email_task(user_email, user_name, amount, commission_type):
    """Send commission earned notification"""
    from src.utils.email_templates import get_commission_earned_template
    
    template = get_commission_earned_template()
    context = {
        'user_name': user_name,
        'amount': amount,
        'commission_type': commission_type,
        'dashboard_url': 'https://app.marketedgepros.com/dashboard'
    }
    
    return send_email_task.delay(
        to=user_email,
        subject=f'Commission Earned: ${amount}',
        template=template,
        context=context
    )


@celery_app.task(name='src.tasks.email_tasks.send_withdrawal_approved_email')
def send_withdrawal_approved_email_task(user_email, user_name, amount):
    """Send withdrawal approval notification"""
    from src.utils.email_templates import get_withdrawal_approved_template
    
    template = get_withdrawal_approved_template()
    context = {
        'user_name': user_name,
        'amount': amount
    }
    
    return send_email_task.delay(
        to=user_email,
        subject=f'Withdrawal Approved: ${amount}',
        template=template,
        context=context
    )

