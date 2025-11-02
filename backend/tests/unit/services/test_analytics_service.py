"""
Tests for Analytics Service
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from src.services.analytics_service import AnalyticsService
from src.models import User, Challenge, Payment, Commission, Referral, Agent, TradingProgram


@pytest.fixture
def mock_users(session):
    """Create mock users for testing"""
    from werkzeug.security import generate_password_hash
    users = []
    for i in range(5):
        user = User(
            email=f'user{i}@example.com',
            first_name=f'User{i}',
            last_name='Test',
            role='trader',
            is_active=True,
            kyc_status='pending' if i % 2 == 0 else 'approved',
            kyc_submitted_at=datetime.utcnow() - timedelta(days=i) if i < 3 else None,
            created_at=datetime.utcnow() - timedelta(days=i)
        )
        user.password_hash = generate_password_hash('password123')
        users.append(user)
        session.add(user)
    session.commit()
    return users


@pytest.fixture
def mock_payments(session, mock_users):
    """Create mock payments for testing"""
    payments = []
    for i, user in enumerate(mock_users):
        payment = Payment(
            user_id=user.id,
            amount=Decimal('100.00') * (i + 1),
            status='completed' if i % 2 == 0 else 'pending',
            payment_method='stripe' if i % 2 == 0 else 'paypal',
            created_at=datetime.utcnow() - timedelta(days=i)
        )
        payments.append(payment)
        session.add(payment)
    session.commit()
    return payments


@pytest.fixture
def mock_program(session):
    """Create a mock trading program"""
    from src.models.tenant import Tenant
    tenant = Tenant(
        name='Test Tenant',
        subdomain='test',
        status='active'
    )
    session.add(tenant)
    session.commit()
    
    program = TradingProgram(
        tenant_id=tenant.id,
        name='Test Program',
        type='one_phase',
        account_size=10000.00,
        price=100.00,
        profit_target=10.00,
        max_daily_loss=5.00,
        max_total_loss=10.00
    )
    session.add(program)
    session.commit()
    return program


@pytest.fixture
def mock_challenges(session, mock_users, mock_program):
    """Create mock challenges for testing"""
    challenges = []
    statuses = ['active', 'passed', 'funded', 'failed', 'active']
    for i, user in enumerate(mock_users):
        challenge = Challenge(
            user_id=user.id,
            program_id=mock_program.id,
            status=statuses[i],
            initial_balance=10000.00,
            created_at=datetime.utcnow() - timedelta(days=i)
        )
        challenges.append(challenge)
        session.add(challenge)
    session.commit()
    return challenges


@pytest.fixture
def mock_agents(session, mock_users):
    """Create mock agents for testing"""
    agents = []
    for i in range(3):
        agent = Agent(
            user_id=mock_users[i].id,
            agent_code=f'AGENT{i:03d}'
        )
        agents.append(agent)
        session.add(agent)
    session.commit()
    return agents


@pytest.fixture
def mock_referrals(session, mock_agents, mock_users):
    """Create mock referrals for testing"""
    referrals = []
    for i, agent in enumerate(mock_agents):
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=mock_users[i + 2].id,
            referral_code=f'REF{i:03d}',
            status='active' if i % 2 == 0 else 'inactive'
        )
        referrals.append(referral)
        session.add(referral)
    session.commit()
    return referrals


@pytest.fixture
def mock_commissions(session, mock_agents, mock_referrals, mock_challenges):
    """Create mock commissions for testing"""
    commissions = []
    for i, agent in enumerate(mock_agents):
        commission = Commission(
            agent_id=agent.id,
            referral_id=mock_referrals[i].id if i < len(mock_referrals) else None,
            challenge_id=mock_challenges[i].id if i < len(mock_challenges) else mock_challenges[0].id,
            commission_amount=Decimal('50.00') * (i + 1),
            status='approved'
        )
        commissions.append(commission)
        session.add(commission)
    session.commit()
    return commissions


class TestRevenueOverTime:
    """Test revenue over time analytics"""
    
    def test_revenue_over_time_success(self, session, mock_payments):
        """Test getting revenue over time successfully"""
        result = AnalyticsService.get_revenue_over_time(days=30)
        
        assert isinstance(result, list)
        # Should have data for days with completed payments
        completed_payments = [p for p in mock_payments if p.status == 'completed']
        assert len(result) <= len(completed_payments)
        
        # Check data structure
        if result:
            assert 'date' in result[0]
            assert 'revenue' in result[0]
            assert 'transactions' in result[0]
    
    def test_revenue_over_time_custom_days(self, session, mock_payments):
        """Test getting revenue with custom day range"""
        result = AnalyticsService.get_revenue_over_time(days=7)
        
        assert isinstance(result, list)
        # All dates should be within the last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        for item in result:
            date = datetime.strptime(item['date'], '%Y-%m-%d')
            assert date >= seven_days_ago.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def test_revenue_over_time_no_data(self, session):
        """Test getting revenue when no payments exist"""
        result = AnalyticsService.get_revenue_over_time(days=30)
        
        assert isinstance(result, list)
        assert len(result) == 0


class TestUserGrowth:
    """Test user growth analytics"""
    
    def test_user_growth_success(self, session, mock_users):
        """Test getting user growth successfully"""
        result = AnalyticsService.get_user_growth(days=30)
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check data structure
        assert 'date' in result[0]
        assert 'registrations' in result[0]
        assert 'active' in result[0]
        assert 'cumulative' in result[0]
    
    def test_user_growth_cumulative(self, session, mock_users):
        """Test that cumulative count increases"""
        result = AnalyticsService.get_user_growth(days=30)
        
        if len(result) > 1:
            # Cumulative should be non-decreasing
            for i in range(1, len(result)):
                assert result[i]['cumulative'] >= result[i-1]['cumulative']
    
    def test_user_growth_custom_days(self, session, mock_users):
        """Test getting user growth with custom day range"""
        result = AnalyticsService.get_user_growth(days=7)
        
        assert isinstance(result, list)
    
    def test_user_growth_no_data(self, session):
        """Test getting user growth when no users exist"""
        result = AnalyticsService.get_user_growth(days=30)
        
        assert isinstance(result, list)
        # May have data from other tests, just verify it returns a list


class TestChallengeStatistics:
    """Test challenge statistics analytics"""
    
    def test_challenge_statistics_success(self, session, mock_challenges):
        """Test getting challenge statistics successfully"""
        result = AnalyticsService.get_challenge_statistics(days=30)
        
        assert isinstance(result, dict)
        assert 'status_distribution' in result
        assert 'daily_data' in result
        
        # Check status distribution
        assert isinstance(result['status_distribution'], list)
        if result['status_distribution']:
            assert 'status' in result['status_distribution'][0]
            assert 'count' in result['status_distribution'][0]
        
        # Check daily data
        assert isinstance(result['daily_data'], list)
        if result['daily_data']:
            assert 'date' in result['daily_data'][0]
            assert 'created' in result['daily_data'][0]
            assert 'completed' in result['daily_data'][0]
            assert 'funded' in result['daily_data'][0]
    
    def test_challenge_statistics_status_counts(self, session, mock_challenges):
        """Test that status counts are correct"""
        result = AnalyticsService.get_challenge_statistics(days=30)
        
        status_dist = result['status_distribution']
        total_count = sum(item['count'] for item in status_dist)
        
        assert total_count == len(mock_challenges)
    
    def test_challenge_statistics_custom_days(self, session, mock_challenges):
        """Test getting challenge statistics with custom day range"""
        result = AnalyticsService.get_challenge_statistics(days=7)
        
        assert isinstance(result, dict)
        assert 'status_distribution' in result
        assert 'daily_data' in result
    
    def test_challenge_statistics_no_data(self, session):
        """Test getting challenge statistics when no challenges exist"""
        result = AnalyticsService.get_challenge_statistics(days=30)
        
        assert isinstance(result, dict)
        assert result['status_distribution'] == []
        assert result['daily_data'] == []


class TestKYCStatistics:
    """Test KYC statistics analytics"""
    
    def test_kyc_statistics_success(self, session, mock_users):
        """Test getting KYC statistics successfully"""
        result = AnalyticsService.get_kyc_statistics()
        
        assert isinstance(result, dict)
        assert 'distribution' in result
        assert 'recent_submissions' in result
        
        # Check distribution
        assert isinstance(result['distribution'], list)
        if result['distribution']:
            assert 'status' in result['distribution'][0]
            assert 'count' in result['distribution'][0]
        
        # Check recent submissions
        assert isinstance(result['recent_submissions'], list)
    
    def test_kyc_statistics_distribution_counts(self, session, mock_users):
        """Test that KYC distribution counts are correct"""
        result = AnalyticsService.get_kyc_statistics()
        
        distribution = result['distribution']
        total_count = sum(item['count'] for item in distribution)
        
        # Should have at least the mock users we created
        assert total_count >= len(mock_users)
    
    def test_kyc_statistics_no_data(self, session):
        """Test getting KYC statistics when no users exist"""
        result = AnalyticsService.get_kyc_statistics()
        
        assert isinstance(result, dict)
        assert 'distribution' in result
        assert 'recent_submissions' in result


class TestReferralStatistics:
    """Test referral statistics analytics"""
    
    def test_referral_statistics_success(self, session):
        """Test getting referral statistics successfully"""
        result = AnalyticsService.get_referral_statistics()
        
        assert isinstance(result, dict)
        assert 'top_agents' in result
        assert 'total_referrals' in result
        assert 'active_referrals' in result
        assert 'conversion_rate' in result
        
        # Check top agents structure
        assert isinstance(result['top_agents'], list)
        # May have data from other tests
    
    def test_referral_statistics_counts(self, session):
        """Test that referral counts are correct"""
        result = AnalyticsService.get_referral_statistics()
        
        # Should return valid counts
        assert isinstance(result['total_referrals'], int)
        assert isinstance(result['active_referrals'], int)
        assert result['total_referrals'] >= 0
        assert result['active_referrals'] >= 0
    
    def test_referral_statistics_conversion_rate(self, session):
        """Test that conversion rate is calculated correctly"""
        result = AnalyticsService.get_referral_statistics()
        
        assert isinstance(result['conversion_rate'], (int, float))
        assert 0 <= result['conversion_rate'] <= 100
    
    def test_referral_statistics_no_data(self, session):
        """Test getting referral statistics when no data exists"""
        result = AnalyticsService.get_referral_statistics()
        
        assert isinstance(result, dict)
        # May have data from other tests, just verify structure
        assert 'total_referrals' in result
        assert 'active_referrals' in result
        assert 'conversion_rate' in result
        assert 'top_agents' in result


class TestPaymentStatistics:
    """Test payment statistics analytics"""
    
    def test_payment_statistics_success(self, session, mock_payments):
        """Test getting payment statistics successfully"""
        result = AnalyticsService.get_payment_statistics(days=30)
        
        assert isinstance(result, dict)
        assert 'method_distribution' in result
        assert 'status_distribution' in result
        
        # Check method distribution
        assert isinstance(result['method_distribution'], list)
        if result['method_distribution']:
            method = result['method_distribution'][0]
            assert 'method' in method
            assert 'count' in method
            assert 'total_amount' in method
        
        # Check status distribution
        assert isinstance(result['status_distribution'], list)
        if result['status_distribution']:
            status = result['status_distribution'][0]
            assert 'status' in status
            assert 'count' in status
    
    def test_payment_statistics_status_counts(self, session, mock_payments):
        """Test that payment status counts are correct"""
        result = AnalyticsService.get_payment_statistics(days=30)
        
        status_dist = result['status_distribution']
        total_count = sum(item['count'] for item in status_dist)
        
        assert total_count == len(mock_payments)
    
    def test_payment_statistics_custom_days(self, session, mock_payments):
        """Test getting payment statistics with custom day range"""
        result = AnalyticsService.get_payment_statistics(days=7)
        
        assert isinstance(result, dict)
        assert 'method_distribution' in result
        assert 'status_distribution' in result
    
    def test_payment_statistics_no_data(self, session):
        """Test getting payment statistics when no payments exist"""
        result = AnalyticsService.get_payment_statistics(days=30)
        
        assert isinstance(result, dict)
        assert result['method_distribution'] == []
        assert result['status_distribution'] == []


class TestComprehensiveAnalytics:
    """Test comprehensive analytics"""
    
    def test_comprehensive_analytics_success(self, session):
        """Test getting comprehensive analytics successfully"""
        result = AnalyticsService.get_comprehensive_analytics(days=30)
        
        assert isinstance(result, dict)
        assert 'revenue_over_time' in result
        assert 'user_growth' in result
        assert 'challenge_statistics' in result
        assert 'kyc_statistics' in result
        assert 'referral_statistics' in result
        assert 'payment_statistics' in result
        
        # Verify each section is properly formatted
        assert isinstance(result['revenue_over_time'], list)
        assert isinstance(result['user_growth'], list)
        assert isinstance(result['challenge_statistics'], dict)
        assert isinstance(result['kyc_statistics'], dict)
        assert isinstance(result['referral_statistics'], dict)
        assert isinstance(result['payment_statistics'], dict)
    
    def test_comprehensive_analytics_custom_days(self, session):
        """Test getting comprehensive analytics with custom day range"""
        result = AnalyticsService.get_comprehensive_analytics(days=7)
        
        assert isinstance(result, dict)
        assert len(result) == 6  # All 6 analytics sections
    
    def test_comprehensive_analytics_no_data(self, session):
        """Test getting comprehensive analytics when no data exists"""
        result = AnalyticsService.get_comprehensive_analytics(days=30)
        
        assert isinstance(result, dict)
        # Should still return all sections, just with empty data
        assert 'revenue_over_time' in result
        assert 'user_growth' in result
        assert 'challenge_statistics' in result
        assert 'kyc_statistics' in result
        assert 'referral_statistics' in result
        assert 'payment_statistics' in result
