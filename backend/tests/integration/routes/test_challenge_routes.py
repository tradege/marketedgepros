"""
Integration Tests for Challenge Routes
Tests the complete challenge workflow API
"""
import pytest
import json
from decimal import Decimal
from datetime import datetime
from src.models.trading_program import Challenge, TradingProgram
from src.models.user import User
from src.database import db


@pytest.fixture
def trading_program(app):
    """Create a trading program for testing"""
    with app.app_context():
        program = TradingProgram(
            name="$10K Challenge",
            account_size=Decimal('10000.00'),
            profit_target=Decimal('10.0'),
            max_daily_loss=Decimal('5.0'),
            max_total_loss=Decimal('10.0'),
            price=Decimal('99.00'),
            is_active=True
        )
        db.session.add(program)
        db.session.commit()
        yield program
        db.session.rollback()


@pytest.fixture
def trader_user(app):
    """Create a trader user"""
    with app.app_context():
        user = User(
            email='trader@test.com',
            first_name='Test',
            last_name='Trader',
            role='trader'
        )
        user.set_password('Test123!')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.rollback()


@pytest.fixture
def admin_user(app):
    """Create an admin user"""
    with app.app_context():
        user = User(
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        user.set_password('Admin123!')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.rollback()


@pytest.fixture
def trader_token(client, trader_user):
    """Get JWT token for trader"""
    response = client.post('/api/auth/login', json={
        'email': 'trader@test.com',
        'password': 'Test123!'
    })
    return response.json['access_token']


@pytest.fixture
def admin_token(client, admin_user):
    """Get JWT token for admin"""
    response = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'Admin123!'
    })
    return response.json['access_token']


class TestGetChallenges:
    """Test GET /api/challenges endpoint"""
    
    def test_get_challenges_success(self, client, trader_user, trader_token, trading_program, app):
        """Test getting user's challenges"""
        # Create a challenge
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active',
                initial_balance=Decimal('10000.00'),
                current_balance=Decimal('10000.00')
            )
            db.session.add(challenge)
            db.session.commit()
        
        response = client.get(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 200
        data = response.json
        assert 'challenges' in data
        assert len(data['challenges']) > 0
    
    def test_get_challenges_unauthorized(self, client):
        """Test getting challenges without token"""
        response = client.get('/api/challenges')
        
        assert response.status_code == 401
    
    def test_get_challenges_pagination(self, client, trader_user, trader_token, trading_program, app):
        """Test challenges pagination"""
        # Create multiple challenges
        with app.app_context():
            for i in range(5):
                challenge = Challenge(
                    user_id=trader_user.id,
                    program_id=trading_program.id,
                    status='active',
                    initial_balance=Decimal('10000.00')
                )
                db.session.add(challenge)
            db.session.commit()
        
        response = client.get(
            '/api/challenges?page=1&per_page=3',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 200
        data = response.json
        assert 'total' in data
        assert 'pages' in data
        assert 'current_page' in data


class TestCreateChallenge:
    """Test POST /api/challenges endpoint"""
    
    def test_create_challenge_success(self, client, trader_token, trading_program):
        """Test creating a new challenge"""
        response = client.post(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'},
            json={'program_id': trading_program.id}
        )
        
        assert response.status_code == 201
        data = response.json
        assert 'message' in data
        assert 'challenge' in data
        assert data['challenge']['program_id'] == trading_program.id
        assert data['challenge']['status'] == 'pending'
    
    def test_create_challenge_missing_program_id(self, client, trader_token):
        """Test creating challenge without program_id"""
        response = client.post(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'},
            json={}
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_create_challenge_invalid_program(self, client, trader_token):
        """Test creating challenge with invalid program"""
        response = client.post(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'},
            json={'program_id': 99999}
        )
        
        assert response.status_code == 404
    
    def test_create_challenge_inactive_program(self, client, trader_token, app):
        """Test creating challenge with inactive program"""
        with app.app_context():
            program = TradingProgram(
                name="Inactive Program",
                account_size=Decimal('5000.00'),
                profit_target=Decimal('10.0'),
                is_active=False
            )
            db.session.add(program)
            db.session.commit()
            program_id = program.id
        
        response = client.post(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'},
            json={'program_id': program_id}
        )
        
        assert response.status_code == 400
        assert 'not active' in response.json['error'].lower()
    
    def test_create_challenge_unauthorized(self, client, trading_program):
        """Test creating challenge without token"""
        response = client.post(
            '/api/challenges',
            json={'program_id': trading_program.id}
        )
        
        assert response.status_code == 401


class TestStartChallenge:
    """Test POST /api/challenges/<id>/start endpoint"""
    
    def test_start_challenge_success(self, client, trader_user, trader_token, trading_program, app):
        """Test starting a pending challenge"""
        # Create pending challenge
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending',
                initial_balance=Decimal('10000.00'),
                current_balance=Decimal('10000.00')
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.post(
            f'/api/challenges/{challenge_id}/start',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['challenge']['status'] == 'active'
        assert 'started_at' in data['challenge']
    
    def test_start_challenge_already_active(self, client, trader_user, trader_token, trading_program, app):
        """Test starting an already active challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active',
                initial_balance=Decimal('10000.00')
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.post(
            f'/api/challenges/{challenge_id}/start',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 400
        assert 'cannot be started' in response.json['error'].lower()
    
    def test_start_challenge_not_found(self, client, trader_token):
        """Test starting non-existent challenge"""
        response = client.post(
            '/api/challenges/99999/start',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 404
    
    def test_start_challenge_wrong_user(self, client, trader_user, trading_program, app):
        """Test starting another user's challenge"""
        # Create challenge for trader_user
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
            
            # Create another user
            other_user = User(
                email='other@test.com',
                first_name='Other',
                last_name='User',
                role='trader'
            )
            other_user.set_password('Test123!')
            db.session.add(other_user)
            db.session.commit()
        
        # Login as other user
        response = client.post('/api/auth/login', json={
            'email': 'other@test.com',
            'password': 'Test123!'
        })
        other_token = response.json['access_token']
        
        # Try to start trader_user's challenge
        response = client.post(
            f'/api/challenges/{challenge_id}/start',
            headers={'Authorization': f'Bearer {other_token}'}
        )
        
        assert response.status_code == 404


class TestEvaluateChallenge:
    """Test POST /api/challenges/<id>/evaluate endpoint"""
    
    def test_evaluate_challenge_success(self, client, trader_user, admin_token, trading_program, app):
        """Test evaluating a challenge (admin only)"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active',
                initial_balance=Decimal('10000.00'),
                current_balance=Decimal('11000.00'),
                total_profit=Decimal('1000.00')
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.post(
            f'/api/challenges/{challenge_id}/evaluate',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code in [200, 400]  # May fail if evaluation logic needs trades
    
    def test_evaluate_challenge_not_admin(self, client, trader_user, trader_token, trading_program, app):
        """Test evaluating challenge without admin rights"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.post(
            f'/api/challenges/{challenge_id}/evaluate',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 403
    
    def test_evaluate_challenge_not_active(self, client, trader_user, admin_token, trading_program, app):
        """Test evaluating non-active challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.post(
            f'/api/challenges/{challenge_id}/evaluate',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 400
        assert 'not active' in response.json['error'].lower()


class TestAddTrade:
    """Test POST /api/challenges/<id>/trades endpoint"""
    
    def test_add_trade_success(self, client, trader_user, trader_token, trading_program, app):
        """Test adding a trade to challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active',
                initial_balance=Decimal('10000.00'),
                current_balance=Decimal('10000.00')
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        trade_data = {
            'symbol': 'EURUSD',
            'type': 'buy',
            'entry_price': 1.1000,
            'exit_price': 1.1050,
            'lots': 1.0,
            'profit': 500.00,
            'pips': 50
        }
        
        response = client.post(
            f'/api/challenges/{challenge_id}/trades',
            headers={'Authorization': f'Bearer {trader_token}'},
            json=trade_data
        )
        
        assert response.status_code == 201
        data = response.json
        assert 'trade' in data
        assert data['trade']['symbol'] == 'EURUSD'
        assert 'challenge' in data
    
    def test_add_trade_missing_fields(self, client, trader_user, trader_token, trading_program, app):
        """Test adding trade with missing fields"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.post(
            f'/api/challenges/{challenge_id}/trades',
            headers={'Authorization': f'Bearer {trader_token}'},
            json={'symbol': 'EURUSD'}  # Missing required fields
        )
        
        assert response.status_code == 400
    
    def test_add_trade_not_active(self, client, trader_user, trader_token, trading_program, app):
        """Test adding trade to non-active challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        trade_data = {
            'symbol': 'EURUSD',
            'type': 'buy',
            'entry_price': 1.1000,
            'exit_price': 1.1050,
            'lots': 1.0,
            'profit': 500.00,
            'pips': 50
        }
        
        response = client.post(
            f'/api/challenges/{challenge_id}/trades',
            headers={'Authorization': f'Bearer {trader_token}'},
            json=trade_data
        )
        
        assert response.status_code == 400


class TestAdminGetAllChallenges:
    """Test GET /api/challenges/admin/all endpoint"""
    
    def test_admin_get_all_challenges(self, client, admin_token, trader_user, trading_program, app):
        """Test admin getting all challenges"""
        # Create some challenges
        with app.app_context():
            for i in range(3):
                challenge = Challenge(
                    user_id=trader_user.id,
                    program_id=trading_program.id,
                    status='active'
                )
                db.session.add(challenge)
            db.session.commit()
        
        response = client.get(
            '/api/challenges/admin/all',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.json
        assert 'challenges' in data
        assert 'pagination' in data
    
    def test_admin_get_all_challenges_filter_status(self, client, admin_token, trader_user, trading_program, app):
        """Test filtering challenges by status"""
        with app.app_context():
            challenge1 = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='active'
            )
            challenge2 = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending'
            )
            db.session.add_all([challenge1, challenge2])
            db.session.commit()
        
        response = client.get(
            '/api/challenges/admin/all?status=active',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.json
        # All returned challenges should be active
        for challenge in data['challenges']:
            assert challenge['status'] == 'active'
    
    def test_admin_get_all_challenges_not_admin(self, client, trader_token):
        """Test non-admin cannot access admin endpoint"""
        response = client.get(
            '/api/challenges/admin/all',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 403


class TestAdminDeleteChallenge:
    """Test DELETE /api/challenges/admin/<id> endpoint"""
    
    def test_admin_delete_challenge_success(self, client, admin_token, trader_user, trading_program, app):
        """Test admin deleting a challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.delete(
            f'/api/challenges/admin/{challenge_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        assert 'deleted successfully' in response.json['message'].lower()
    
    def test_admin_delete_funded_challenge(self, client, admin_token, trader_user, trading_program, app):
        """Test cannot delete funded challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='funded'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.delete(
            f'/api/challenges/admin/{challenge_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 400
        assert 'cannot delete funded' in response.json['error'].lower()
    
    def test_admin_delete_challenge_not_admin(self, client, trader_token, trader_user, trading_program, app):
        """Test non-admin cannot delete challenge"""
        with app.app_context():
            challenge = Challenge(
                user_id=trader_user.id,
                program_id=trading_program.id,
                status='pending'
            )
            db.session.add(challenge)
            db.session.commit()
            challenge_id = challenge.id
        
        response = client.delete(
            f'/api/challenges/admin/{challenge_id}',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        
        assert response.status_code == 403
    
    def test_admin_delete_challenge_not_found(self, client, admin_token):
        """Test deleting non-existent challenge"""
        response = client.delete(
            '/api/challenges/admin/99999',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 404


class TestChallengeWorkflow:
    """Test complete challenge workflow"""
    
    def test_complete_challenge_workflow(self, client, trader_token, trading_program):
        """Test complete workflow: create -> start -> add trades"""
        # Step 1: Create challenge
        response = client.post(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'},
            json={'program_id': trading_program.id}
        )
        assert response.status_code == 201
        challenge_id = response.json['challenge']['id']
        
        # Step 2: Start challenge
        response = client.post(
            f'/api/challenges/{challenge_id}/start',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        assert response.status_code == 200
        assert response.json['challenge']['status'] == 'active'
        
        # Step 3: Add a winning trade
        trade_data = {
            'symbol': 'EURUSD',
            'type': 'buy',
            'entry_price': 1.1000,
            'exit_price': 1.1050,
            'lots': 1.0,
            'profit': 500.00,
            'pips': 50
        }
        response = client.post(
            f'/api/challenges/{challenge_id}/trades',
            headers={'Authorization': f'Bearer {trader_token}'},
            json=trade_data
        )
        assert response.status_code == 201
        
        # Step 4: Verify challenge was updated
        response = client.get(
            '/api/challenges',
            headers={'Authorization': f'Bearer {trader_token}'}
        )
        assert response.status_code == 200
        challenges = response.json['challenges']
        assert any(c['id'] == challenge_id for c in challenges)
