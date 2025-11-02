"""
Unit tests for KYC & Verification System
"""
import pytest
from datetime import datetime, timedelta
from src.models import VerificationAttempt

@pytest.mark.unit
class TestVerificationAttempt:
    """Test verification attempt tracking"""
    
    def test_create_verification_attempt(self, session):
        """Test creating a verification attempt"""
        attempt = VerificationAttempt(
            email='test@example.com',
            code_entered='123456',
            success=True,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )
        session.add(attempt)
        session.commit()
        
        assert attempt.id is not None
        assert attempt.email == 'test@example.com'
        assert attempt.code_entered == '123456'
        assert attempt.success is True
    
    def test_log_successful_attempt(self, session):
        """Test logging successful verification attempt"""
        attempt = VerificationAttempt.log_attempt(
            email='success@example.com',
            code_entered='999999',
            success=True,
            ip_address='10.0.0.1',
            user_agent='Chrome/90.0'
        )
        
        assert attempt.success is True
        assert attempt.failure_reason is None
    
    def test_log_failed_attempt(self, session):
        """Test logging failed verification attempt"""
        attempt = VerificationAttempt.log_attempt(
            email='fail@example.com',
            code_entered='000000',
            success=False,
            ip_address='10.0.0.2',
            failure_reason='invalid_code'
        )
        
        assert attempt.success is False
        assert attempt.failure_reason == 'invalid_code'
    
    def test_get_recent_failures_by_email(self, session):
        """Test getting recent failures by email"""
        email = 'ratelimit@example.com'
        
        # Create 3 failed attempts
        for i in range(3):
            VerificationAttempt.log_attempt(
                email=email,
                code_entered=f'{i}00000',
                success=False,
                failure_reason='invalid_code'
            )
        
        failures = VerificationAttempt.get_recent_failures_by_email(email, minutes=15)
        assert failures == 3
    
    def test_get_recent_failures_by_ip(self, session):
        """Test getting recent failures by IP"""
        ip = '192.168.1.100'
        
        # Create 4 failed attempts from same IP
        for i in range(4):
            VerificationAttempt.log_attempt(
                email=f'user{i}@example.com',
                code_entered='123456',
                success=False,
                ip_address=ip,
                failure_reason='invalid_code'
            )
        
        failures = VerificationAttempt.get_recent_failures_by_ip(ip, minutes=15)
        assert failures == 4
    
    def test_rate_limiting_by_email(self, session):
        """Test rate limiting by email"""
        email = 'spam@example.com'
        ip = '10.0.0.5'
        
        # Create 5 failed attempts (should trigger rate limit)
        for i in range(5):
            VerificationAttempt.log_attempt(
                email=email,
                code_entered='000000',
                success=False,
                ip_address=ip
            )
        
        is_limited = VerificationAttempt.is_rate_limited(email, ip, max_attempts=5)
        assert is_limited is True
    
    def test_rate_limiting_by_ip(self, session):
        """Test rate limiting by IP"""
        ip = '192.168.1.200'
        
        # Create 6 failed attempts from same IP with different emails
        for i in range(6):
            VerificationAttempt.log_attempt(
                email=f'different{i}@example.com',
                code_entered='000000',
                success=False,
                ip_address=ip
            )
        
        is_limited = VerificationAttempt.is_rate_limited('new@example.com', ip, max_attempts=5)
        assert is_limited is True
    
    def test_no_rate_limit_with_few_attempts(self, session):
        """Test no rate limiting with few attempts"""
        email = 'normal@example.com'
        ip = '10.0.0.10'
        
        # Create only 2 failed attempts
        for i in range(2):
            VerificationAttempt.log_attempt(
                email=email,
                code_entered='000000',
                success=False,
                ip_address=ip
            )
        
        is_limited = VerificationAttempt.is_rate_limited(email, ip, max_attempts=5)
        assert is_limited is False
    
    def test_successful_attempts_dont_count_for_rate_limit(self, session):
        """Test that successful attempts don't count for rate limiting"""
        email = 'success@example.com'
        ip = '10.0.0.20'
        
        # Create 3 failed and 2 successful attempts
        for i in range(3):
            VerificationAttempt.log_attempt(
                email=email,
                code_entered='000000',
                success=False,
                ip_address=ip
            )
        
        for i in range(2):
            VerificationAttempt.log_attempt(
                email=email,
                code_entered='999999',
                success=True,
                ip_address=ip
            )
        
        # Should not be rate limited (only 3 failures)
        is_limited = VerificationAttempt.is_rate_limited(email, ip, max_attempts=5)
        assert is_limited is False
    
    def test_old_failures_dont_count(self, session):
        """Test that old failures don't count for rate limiting"""
        email = 'old@example.com'
        ip = '10.0.0.30'
        
        # Create an old failed attempt (20 minutes ago)
        old_attempt = VerificationAttempt(
            email=email,
            code_entered='000000',
            success=False,
            ip_address=ip,
            created_at=datetime.utcnow() - timedelta(minutes=20)
        )
        session.add(old_attempt)
        session.commit()
        
        # Should not be rate limited (attempt is outside 15-minute window)
        is_limited = VerificationAttempt.is_rate_limited(email, ip, max_attempts=5, window_minutes=15)
        assert is_limited is False
    
    def test_failure_reasons(self, session):
        """Test different failure reasons"""
        reasons = ['invalid_code', 'expired', 'already_used', 'too_many_attempts']
        
        for reason in reasons:
            attempt = VerificationAttempt.log_attempt(
                email='test@example.com',
                code_entered='123456',
                success=False,
                failure_reason=reason
            )
            assert attempt.failure_reason == reason
    
    def test_ip_tracking(self, session):
        """Test IP address tracking"""
        ipv4 = '192.168.1.1'
        ipv6 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        
        attempt_v4 = VerificationAttempt.log_attempt(
            email='ipv4@example.com',
            code_entered='123456',
            success=True,
            ip_address=ipv4
        )
        
        attempt_v6 = VerificationAttempt.log_attempt(
            email='ipv6@example.com',
            code_entered='123456',
            success=True,
            ip_address=ipv6
        )
        
        assert attempt_v4.ip_address == ipv4
        assert attempt_v6.ip_address == ipv6
    
    def test_user_agent_tracking(self, session):
        """Test user agent tracking"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        ]
        
        for ua in user_agents:
            attempt = VerificationAttempt.log_attempt(
                email='test@example.com',
                code_entered='123456',
                success=True,
                user_agent=ua
            )
            assert attempt.user_agent == ua
    
    def test_get_suspicious_activity(self, session):
        """Test detecting suspicious activity"""
        # Create suspicious email (15 failures)
        suspicious_email = 'attacker@example.com'
        for i in range(15):
            VerificationAttempt.log_attempt(
                email=suspicious_email,
                code_entered='000000',
                success=False,
                ip_address='10.0.0.100'
            )
        
        # Create suspicious IP (12 failures from different emails)
        suspicious_ip = '192.168.1.250'
        for i in range(12):
            VerificationAttempt.log_attempt(
                email=f'victim{i}@example.com',
                code_entered='000000',
                success=False,
                ip_address=suspicious_ip
            )
        
        suspicious = VerificationAttempt.get_suspicious_activity(hours=24, threshold=10)
        
        # Check suspicious emails
        suspicious_email_list = [item['email'] for item in suspicious['emails']]
        assert suspicious_email in suspicious_email_list
        
        # Check suspicious IPs
        suspicious_ip_list = [item['ip'] for item in suspicious['ips']]
        assert suspicious_ip in suspicious_ip_list
    
    def test_verification_attempt_timestamps(self, session):
        """Test automatic timestamp tracking"""
        attempt = VerificationAttempt.log_attempt(
            email='timestamp@example.com',
            code_entered='123456',
            success=True
        )
        
        assert attempt.created_at is not None
        assert attempt.updated_at is not None
    
    def test_multiple_attempts_same_email(self, session):
        """Test multiple attempts for same email"""
        email = 'retry@example.com'
        
        # First attempt fails
        attempt1 = VerificationAttempt.log_attempt(
            email=email,
            code_entered='000000',
            success=False,
            failure_reason='invalid_code'
        )
        
        # Second attempt succeeds
        attempt2 = VerificationAttempt.log_attempt(
            email=email,
            code_entered='999999',
            success=True
        )
        
        assert attempt1.success is False
        assert attempt2.success is True
        
        # Both attempts should exist
        attempts = VerificationAttempt.query.filter_by(email=email).all()
        assert len(attempts) == 2
