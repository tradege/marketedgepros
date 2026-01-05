"""
Integration Tests for Payout Routes
Professional tests for financial transaction safety
"""
import pytest
import uuid
from datetime import datetime
from decimal import Decimal
from src.database import db


def extract_cookie_value(response, cookie_name):
    """Helper to extract cookie value from response"""
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if cookie.startswith(f'{cookie_name}='):
            token_part = cookie.split(';')[0]
            return token_part.split('=', 1)[1]
    return None


class TestPayoutAuth:
    """Test authentication requirements for payout endpoints"""
    
    def test_check_eligibility_requires_auth(self, client):
        """Test that check eligibility requires authentication"""
        response = client.get('/api/payouts/check-eligibility')
        assert response.status_code == 401
    
    def test_request_payout_requires_auth(self, client):
        """Test that request payout requires authentication"""
        response = client.post('/api/payouts/request', json={
            'amount': 100.00,
            'payment_method': 'bank_transfer'
        })
        assert response.status_code == 401
    
    def test_my_payouts_requires_auth(self, client):
        """Test that my payouts requires authentication"""
        response = client.get('/api/payouts/my-payouts')
        assert response.status_code == 401


class TestPayoutEligibility:
    """Test payout eligibility checking"""
    
    def test_check_eligibility_eligible_user(self, client, session):
        """Test eligibility check for eligible user"""
        from src.models.user import User
        from src.models.trading_program import TradingProgram, Challenge
        from src.models.mt5_models import MT5Account
        from src.models.tenant import Tenant
        
        # Create tenant
        tenant = Tenant(
            name='Test Tenant',
            subdomain=f'test_{uuid.uuid4().hex[:8]}'
        )
        session.add(tenant)
        session.flush()
        
        # Create user
        email = f"eligible_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            first_name='Eligible',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        user.available_balance = 1000.00  # Set available balance for payout
        session.add(user)
        session.commit()
        
        # Create program and challenge
        program = TradingProgram(
            tenant_id=tenant.id,
            name='Test Program',
            type='one_phase',
            account_size=10000.00,
            profit_target=10.00,
            max_daily_loss=5.00,
            max_total_loss=10.00,
            profit_split=80.00,
            price=100.00
        )
        session.add(program)
        session.commit()
        
        challenge = Challenge(
            user_id=user.id,
            program_id=program.id,
            status='passed',
            current_balance=11000.00
        )
        session.add(challenge)
        session.commit()
        
        # Create MT5 account
        mt5_account = MT5Account(
            user_id=user.id,
            challenge_id=challenge.id,
            mt5_login='12345',
            mt5_password_encrypted='encrypted',
            mt5_server='demo',
            balance=11000.00,
            status='active'
        )
        session.add(mt5_account)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Check eligibility
        response = client.get(
            '/api/payouts/check-eligibility',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'can_request' in data


class TestPayoutRequest:
    """Test payout request creation"""
    
    def test_request_payout_success(self, client, session):
        """Test successful payout request"""
        from src.models.user import User
        from src.models.trading_program import TradingProgram, Challenge
        from src.models.mt5_models import MT5Account
        from src.models.tenant import Tenant
        
        # Create tenant
        tenant = Tenant(
            name='Test Tenant',
            subdomain=f'test_{uuid.uuid4().hex[:8]}'
        )
        session.add(tenant)
        session.flush()
        
        # Create user
        email = f"requester_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            first_name='Request',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        user.available_balance = 1000.00  # Set available balance for payout
        session.add(user)
        session.commit()
        
        # Create program and challenge
        program = TradingProgram(
            tenant_id=tenant.id,
            name='Test Program',
            type='one_phase',
            account_size=10000.00,
            profit_target=10.00,
            max_daily_loss=5.00,
            max_total_loss=10.00,
            profit_split=80.00,
            price=100.00
        )
        session.add(program)
        session.commit()
        
        challenge = Challenge(
            user_id=user.id,
            program_id=program.id,
            status='passed',
            current_balance=11000.00
        )
        session.add(challenge)
        session.commit()
        
        # Create MT5 account
        mt5_account = MT5Account(
            user_id=user.id,
            challenge_id=challenge.id,
            mt5_login='12345',
            mt5_password_encrypted='encrypted',
            mt5_server='demo',
            balance=11000.00,
            status='active'
        )
        session.add(mt5_account)
        session.commit()
        
        # Login
        login_response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(login_response, 'access_token')
        
        # Request payout
        response = client.post('/api/payouts/request',
            headers={'Authorization': f'Bearer {token}'},
            json={
            'amount': 500.00,
            'payment_method': 'bank_transfer',
            'payout_mode': 'on_demand_full'
        })
        assert response.status_code in [200, 201]
        data = response.get_json()
        assert 'payout' in data or 'id' in data or 'payout_id' in data
    
    def test_request_payout_validation_errors(self, client, session):
        """Test payout request with validation errors"""
        from src.models.user import User
        
        # Create user
        email = f"validator_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            first_name='Valid',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Request payout with missing fields
        response = client.post('/api/payouts/request',
            headers={'Authorization': f'Bearer {token}'},
            json={})
        assert response.status_code in [400, 422, 500]


class TestPayoutRetrieval:
    """Test payout retrieval endpoints"""
    
    def test_get_my_payouts_with_data(self, client, session):
        """Test getting user's payouts"""
        from src.models.user import User
        from src.models.payout_request import PayoutRequest
        
        # Create user
        email = f"getter_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            first_name='Get',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Create payout request
        payout = PayoutRequest(
            user_id=user.id,
            amount=Decimal('500.00'),
            profit_split_amount=Decimal('400.00'),
            status='pending',
            payout_mode='on_demand_full',
            payment_method='bank_transfer'
        )
        session.add(payout)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Get my payouts
        response = client.get('/api/payouts/my-payouts',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, (list, dict))


class TestPayoutAdmin:
    """Test admin payout endpoints"""
    
    def test_admin_pending_payouts_requires_admin(self, client, session):
        """Test that admin endpoints require admin role"""
        from src.models.user import User
        
        # Create regular user
        email = f"regular_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            first_name='Regular',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Try to access admin endpoint
        response = client.get('/api/payouts/admin/pending',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code in [403, 401]
    
    def test_approve_payout_success(self, client, session):
        """Test approving a payout"""
        from src.models.user import User
        from src.models.payout_request import PayoutRequest
        
        # Create admin user
        admin_email = f"admin_{uuid.uuid4().hex[:8]}@test.com"
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='User',
            role='supermaster'
        )
        admin.set_password('Test123!')
        admin.is_verified = True
        session.add(admin)
        session.commit()
        
        # Create regular user
        user_email = f"user_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=user_email,
            first_name='Test',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Create payout request
        payout = PayoutRequest(
            user_id=user.id,
            amount=Decimal('500.00'),
            profit_split_amount=Decimal('400.00'),
            status='pending',
            payout_mode='on_demand_full',
            payment_method='bank_transfer'
        )
        session.add(payout)
        session.commit()
        payout_id = payout.id
        
        # Login as admin
        response = client.post('/api/v1/auth/login', json={
            'email': admin_email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Approve payout
        response = client.post(f'/api/payouts/admin/{payout_id}/approve',
            headers={'Authorization': f'Bearer {token}'},
            json={})
        assert response.status_code in [200, 201]
    
    def test_reject_payout_success(self, client, session):
        """Test rejecting a payout"""
        from src.models.user import User
        from src.models.payout_request import PayoutRequest
        
        # Create admin user
        admin_email = f"admin_{uuid.uuid4().hex[:8]}@test.com"
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='User',
            role='supermaster'
        )
        admin.set_password('Test123!')
        admin.is_verified = True
        session.add(admin)
        session.commit()
        
        # Create regular user
        user_email = f"user_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=user_email,
            first_name='Test',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Create payout request
        payout = PayoutRequest(
            user_id=user.id,
            amount=Decimal('500.00'),
            profit_split_amount=Decimal('400.00'),
            status='pending',
            payout_mode='on_demand_full',
            payment_method='bank_transfer'
        )
        session.add(payout)
        session.commit()
        payout_id = payout.id
        
        # Login as admin
        response = client.post('/api/v1/auth/login', json={
            'email': admin_email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Reject payout
        response = client.post(f'/api/payouts/admin/{payout_id}/reject',
            headers={'Authorization': f'Bearer {token}'},
            json={
            'reason': 'Test rejection'
        })
        assert response.status_code in [200, 201]
    
    def test_mark_paid_success(self, client, session):
        """Test marking payout as paid"""
        from src.models.user import User
        from src.models.payout_request import PayoutRequest
        
        # Create admin user
        admin_email = f"admin_{uuid.uuid4().hex[:8]}@test.com"
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='User',
            role='supermaster'
        )
        admin.set_password('Test123!')
        admin.is_verified = True
        session.add(admin)
        session.commit()
        
        # Create regular user
        user_email = f"user_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=user_email,
            first_name='Test',
            last_name='User',
            role='trader'
        )
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Create approved payout request
        payout = PayoutRequest(
            user_id=user.id,
            amount=Decimal('500.00'),
            profit_split_amount=Decimal('400.00'),
            status='approved',
            payout_mode='on_demand_full',
            payment_method='bank_transfer'
        )
        session.add(payout)
        session.commit()
        payout_id = payout.id
        
        # Login as admin
        response = client.post('/api/v1/auth/login', json={
            'email': admin_email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Mark as paid
        response = client.post(f'/api/payouts/admin/{payout_id}/mark-paid',
            headers={'Authorization': f'Bearer {token}'},
            json={})
        assert response.status_code in [200, 201]
    
    def test_admin_statistics_success(self, client, session):
        """Test getting admin statistics"""
        from src.models.user import User
        
        # Create admin user
        admin_email = f"admin_{uuid.uuid4().hex[:8]}@test.com"
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='User',
            role='supermaster'
        )
        admin.set_password('Test123!')
        admin.is_verified = True
        session.add(admin)
        session.commit()
        
        # Login as admin
        response = client.post('/api/v1/auth/login', json={
            'email': admin_email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Get statistics
        response = client.get('/api/payouts/admin/statistics',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)


class TestPayoutEdgeCases:
    """Test edge cases and security"""
    
    def test_get_payout_unauthorized_access(self, client, session):
        """Test that users cannot access other users' payouts"""
        from src.models.user import User
        from src.models.payout_request import PayoutRequest
        
        # Create two users
        user1_email = f"user1_{uuid.uuid4().hex[:8]}@test.com"
        user1 = User(
            email=user1_email,
            first_name='User',
            last_name='One',
            role='trader'
        )
        user1.set_password('Test123!')
        user1.is_verified = True
        session.add(user1)
        session.commit()
        
        user2_email = f"user2_{uuid.uuid4().hex[:8]}@test.com"
        user2 = User(
            email=user2_email,
            first_name='User',
            last_name='Two',
            role='trader'
        )
        user2.set_password('Test123!')
        user2.is_verified = True
        session.add(user2)
        session.commit()
        
        # Create payout for user1
        payout = PayoutRequest(
            user_id=user1.id,
            amount=Decimal('500.00'),
            profit_split_amount=Decimal('400.00'),
            status='pending',
            payout_mode='on_demand_full',
            payment_method='bank_transfer'
        )
        session.add(payout)
        session.commit()
        payout_id = payout.id
        
        # Login as user2
        response = client.post('/api/v1/auth/login', json={
            'email': user2_email,
            'password': 'Test123!'
        })
        token = extract_cookie_value(response, 'access_token')
        
        # Try to access user1's payout
        response = client.get(f'/api/payouts/{payout_id}',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code in [403, 404]
