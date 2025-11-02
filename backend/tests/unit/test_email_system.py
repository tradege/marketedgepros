"""
Tests for Email System (Templates, Service, Queue)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.utils.email_templates import (
    get_welcome_template,
    get_verification_template,
    get_password_reset_template,
    get_challenge_purchased_template,
    get_commission_earned_template,
    get_withdrawal_approved_template
)
from src.services.email_service_async import EmailServiceAsync


class TestEmailTemplates:
    """Test email template generation"""
    
    def test_welcome_template_contains_required_elements(self):
        """Test welcome template has all required elements"""
        template = get_welcome_template()
        
        assert 'Welcome to MarketEdgePros' in template
        assert '{{ user_name }}' in template
        assert '{{ login_url }}' in template
        assert 'MarketEdgePros' in template
    
    def test_verification_template_contains_code(self):
        """Test verification template has code placeholder"""
        template = get_verification_template()
        
        assert '{{ verification_code }}' in template
        assert 'Verify Your Email' in template
        assert '{{ user_name }}' in template
    
    def test_password_reset_template_contains_link(self):
        """Test password reset template has reset link"""
        template = get_password_reset_template()
        
        assert '{{ reset_url }}' in template
        assert 'Reset Your Password' in template
        assert '{{ user_name }}' in template
    
    def test_challenge_purchased_template(self):
        """Test challenge purchased template"""
        template = get_challenge_purchased_template()
        
        assert '{{ challenge_name }}' in template
        assert '{{ challenge_url }}' in template
        assert 'Challenge' in template
    
    def test_commission_earned_template(self):
        """Test commission earned template"""
        template = get_commission_earned_template()
        
        assert '{{ amount }}' in template
        assert '{{ commission_type }}' in template
        assert 'Commission' in template
    
    def test_withdrawal_approved_template(self):
        """Test withdrawal approved template"""
        template = get_withdrawal_approved_template()
        
        assert '{{ amount }}' in template
        assert 'Withdrawal' in template
    
    def test_all_templates_have_base_structure(self):
        """Test all templates have proper HTML structure"""
        templates = [
            get_welcome_template(),
            get_verification_template(),
            get_password_reset_template(),
            get_challenge_purchased_template(),
            get_commission_earned_template(),
            get_withdrawal_approved_template()
        ]
        
        for template in templates:
            assert '<!DOCTYPE html>' in template
            assert '<html' in template
            assert '</html>' in template
            assert 'MarketEdgePros' in template
    
    def test_templates_have_responsive_styling(self):
        """Test templates include responsive CSS"""
        template = get_welcome_template()
        
        assert 'max-width: 600px' in template
        assert 'font-family' in template
        assert 'background' in template


class TestEmailServiceAsync:
    """Test async email service"""
    
    @patch('src.tasks.email_tasks.send_welcome_email_task')
    def test_send_welcome_email(self, mock_task):
        """Test sending welcome email queues task"""
        mock_task.delay = Mock(return_value=True)
        
        result = EmailServiceAsync.send_welcome_email('test@example.com', 'John Doe')
        
        assert result is True
        mock_task.delay.assert_called_once_with('test@example.com', 'John Doe')
    
    @patch('src.tasks.email_tasks.send_verification_email_task')
    def test_send_verification_email(self, mock_task):
        """Test sending verification email queues task"""
        mock_task.delay = Mock(return_value=True)
        
        result = EmailServiceAsync.send_verification_email(
            'test@example.com', 'John Doe', '123456'
        )
        
        assert result is True
        mock_task.delay.assert_called_once_with('test@example.com', 'John Doe', '123456')
    
    @patch('src.tasks.email_tasks.send_password_reset_email_task')
    def test_send_password_reset_email(self, mock_task):
        """Test sending password reset email queues task"""
        mock_task.delay = Mock(return_value=True)
        
        result = EmailServiceAsync.send_password_reset_email(
            'test@example.com', 'John Doe', 'reset_token_123'
        )
        
        assert result is True
        mock_task.delay.assert_called_once_with(
            'test@example.com', 'John Doe', 'reset_token_123'
        )
    
    @patch('src.tasks.email_tasks.send_challenge_purchased_email_task')
    def test_send_challenge_purchased_email(self, mock_task):
        """Test sending challenge purchased email queues task"""
        mock_task.delay = Mock(return_value=True)
        
        result = EmailServiceAsync.send_challenge_purchased_email(
            'test@example.com', 'John Doe', '10K Challenge', 1
        )
        
        assert result is True
        mock_task.delay.assert_called_once_with(
            'test@example.com', 'John Doe', '10K Challenge', 1
        )
    
    @patch('src.tasks.email_tasks.send_commission_earned_email_task')
    def test_send_commission_earned_email(self, mock_task):
        """Test sending commission earned email queues task"""
        mock_task.delay = Mock(return_value=True)
        
        result = EmailServiceAsync.send_commission_earned_email(
            'test@example.com', 'John Doe', 100.50, 'Direct Referral'
        )
        
        assert result is True
        mock_task.delay.assert_called_once_with(
            'test@example.com', 'John Doe', 100.50, 'Direct Referral'
        )
    
    @patch('src.tasks.email_tasks.send_withdrawal_approved_email_task')
    def test_send_withdrawal_approved_email(self, mock_task):
        """Test sending withdrawal approved email queues task"""
        mock_task.delay = Mock(return_value=True)
        
        result = EmailServiceAsync.send_withdrawal_approved_email(
            'test@example.com', 'John Doe', 500.00
        )
        
        assert result is True
        mock_task.delay.assert_called_once_with('test@example.com', 'John Doe', 500.00)
    
    @patch('src.tasks.email_tasks.send_email_task')
    def test_send_custom_email(self, mock_task):
        """Test sending custom email with template"""
        mock_task.delay = Mock(return_value=True)
        
        template = '<html><body>{{ message }}</body></html>'
        context = {'message': 'Hello World'}
        
        result = EmailServiceAsync.send_custom_email(
            'test@example.com', 'Custom Subject', template, context
        )
        
        assert result is True
        mock_task.delay.assert_called_once_with(
            'test@example.com', 'Custom Subject', template, context
        )
    
    @patch('src.tasks.email_tasks.send_welcome_email_task')
    def test_email_service_handles_exceptions(self, mock_task):
        """Test email service handles exceptions gracefully"""
        mock_task.delay = Mock(side_effect=Exception('Task queue error'))
        
        result = EmailServiceAsync.send_welcome_email('test@example.com', 'John Doe')
        
        assert result is False


class TestEmailTaskRetry:
    """Test email task retry logic"""
    
    def test_task_retry_configuration(self):
        """Test that tasks are configured with retry"""
        from src.celery_config import celery_app
        
        # Check retry configuration
        assert celery_app.conf.task_autoretry_for == (Exception,)
        assert celery_app.conf.task_retry_kwargs == {'max_retries': 3}
        assert celery_app.conf.task_retry_backoff is True
    
    def test_task_queues_configured(self):
        """Test that email queue is configured"""
        from src.celery_config import celery_app
        
        # Check that email queue exists
        queue_names = [q.name for q in celery_app.conf.task_queues]
        assert 'emails' in queue_names
        assert 'default' in queue_names


class TestEmailIntegration:
    """Integration tests for email system"""
    
    @patch('src.tasks.email_tasks.send_welcome_email_task')
    def test_welcome_email_flow(self, mock_task):
        """Test complete welcome email flow"""
        mock_task.delay = Mock(return_value=True)
        
        # Simulate user registration
        user_email = 'newuser@example.com'
        user_name = 'New User'
        
        # Send welcome email
        result = EmailServiceAsync.send_welcome_email(user_email, user_name)
        
        # Verify
        assert result is True
        mock_task.delay.assert_called_once()
        args = mock_task.delay.call_args[0]
        assert args[0] == user_email
        assert args[1] == user_name
    
    @patch('src.tasks.email_tasks.send_commission_earned_email_task')
    def test_commission_notification_flow(self, mock_task):
        """Test commission notification flow"""
        mock_task.delay = Mock(return_value=True)
        
        # Simulate commission earned
        result = EmailServiceAsync.send_commission_earned_email(
            'agent@example.com',
            'Agent Name',
            250.00,
            'Binary Commission'
        )
        
        # Verify
        assert result is True
        mock_task.delay.assert_called_once()

