"""Debug test for MT5 routes"""
import pytest
import uuid

class TestMT5Debug:
    def test_get_accounts_debug(self, client, session):
        """Debug test to see the actual error"""
        from src.models.user import User
        
        # Create and login user
        email = f'debug_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Debug', last_name='User', role='trader')
        user.set_password('Test123!')
        user.is_verified = True
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        print(f"\n=== LOGIN RESPONSE ===")
        print(f"Status: {response.status_code}")
        print(f"Data: {response.json}")
        
        assert response.status_code == 200
        
        # Get accounts
        response = client.get('/api/mt5/accounts')
        print(f"\n=== GET ACCOUNTS RESPONSE ===")
        print(f"Status: {response.status_code}")
        print(f"Data: {response.data}")
        print(f"JSON: {response.json if response.json else 'No JSON'}")
        
        # Show the actual error
        if response.status_code == 500:
            print(f"\n=== ERROR DETAILS ===")
            if response.json:
                print(f"Error message: {response.json.get('message', 'No message')}")
        
        assert response.status_code == 200
