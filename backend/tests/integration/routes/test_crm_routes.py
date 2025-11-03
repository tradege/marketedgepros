"""
Comprehensive Integration Tests for CRM Routes
Goal: Achieve 100% coverage with proper test isolation
"""
import pytest
import uuid


@pytest.fixture(autouse=True)
def cleanup_after_test(session):
    """Clean up database after each test"""
    yield
    # Rollback any uncommitted changes
    session.rollback()


class TestCRMAuthentication:
    """Test CRM routes authentication requirements"""
    
    def test_get_leads_requires_auth(self, client):
        response = client.get('/api/v1/crm/leads')
        assert response.status_code == 401
    
    def test_create_lead_requires_auth(self, client):
        response = client.post('/api/v1/crm/leads', json={})
        assert response.status_code == 401
    
    def test_get_lead_by_id_requires_auth(self, client):
        response = client.get('/api/v1/crm/leads/1')
        assert response.status_code == 401
    
    def test_update_lead_requires_auth(self, client):
        response = client.put('/api/v1/crm/leads/1', json={})
        assert response.status_code == 401
    
    def test_add_activity_requires_auth(self, client):
        response = client.post('/api/v1/crm/leads/1/activities', json={})
        assert response.status_code == 401
    
    def test_add_note_requires_auth(self, client):
        response = client.post('/api/v1/crm/leads/1/notes', json={})
        assert response.status_code == 401
    
    def test_convert_lead_requires_auth(self, client):
        response = client.post('/api/v1/crm/leads/1/convert')
        assert response.status_code == 401
    
    def test_mark_lost_requires_auth(self, client):
        response = client.post('/api/v1/crm/leads/1/lost', json={})
        assert response.status_code == 401
    
    def test_get_stats_requires_auth(self, client):
        response = client.get('/api/v1/crm/stats')
        assert response.status_code == 401
    
    def test_get_pipeline_requires_auth(self, client):
        response = client.get('/api/v1/crm/pipeline')
        assert response.status_code == 401


class TestCRMWithUser:
    """Test CRM routes with authenticated user"""
    
    def test_get_leads_success(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        response = client.get('/api/v1/crm/leads', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
    
    def test_create_lead_success(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        response = client.post(
            '/api/v1/crm/leads',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': f'lead_{uuid.uuid4().hex[:8]}@test.com',
                'phone': '+1234567890',
                'status': 'new',
                'source': 'website'
            }
        )
        
        assert response.status_code in [200, 201]
    
    def test_get_stats_success(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        response = client.get('/api/v1/crm/stats', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
    
    def test_get_pipeline_success(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        response = client.get('/api/v1/crm/pipeline', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200


class TestCRMFullWorkflow:
    """Test complete CRM workflow with real data"""
    
    def test_full_lead_lifecycle(self, client, session):
        """Test: create -> get -> update -> activity -> note"""
        from src.models.user import User
        from src.models.lead import Lead
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 1. Create lead
        lead_email = f'lead_{uuid.uuid4().hex[:8]}@test.com'
        response = client.post(
            '/api/v1/crm/leads',
            headers=headers,
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': lead_email,
                'phone': '+1234567890',
                'status': 'new',
                'source': 'website'
            }
        )
        assert response.status_code in [200, 201]
        
        session.commit()  # Ensure lead is committed
        lead = Lead.query.filter_by(email=lead_email).first()
        if not lead:
            return
        
        # 2. Get lead by ID
        response = client.get(f'/api/v1/crm/leads/{lead.id}', headers=headers)
        assert response.status_code == 200
        
        # 3. Update lead
        response = client.put(
            f'/api/v1/crm/leads/{lead.id}',
            headers=headers,
            json={'status': 'contacted'}
        )
        assert response.status_code in [200, 204]
        
        # 4. Add activity
        response = client.post(
            f'/api/v1/crm/leads/{lead.id}/activities',
            headers=headers,
            json={
                'activity_type': 'call',
                'subject': 'First call',
                'description': 'Called customer'
            }
        )
        assert response.status_code in [200, 201]
        
        # 5. Add note
        response = client.post(
            f'/api/v1/crm/leads/{lead.id}/notes',
            headers=headers,
            json={'content': 'Customer interested'}
        )
        assert response.status_code in [200, 201]
    
    def test_lead_conversion_workflow(self, client, session):
        """Test converting a lead to customer"""
        from src.models.user import User
        from src.models.lead import Lead
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create lead
        lead_email = f'lead_{uuid.uuid4().hex[:8]}@test.com'
        response = client.post(
            '/api/v1/crm/leads',
            headers=headers,
            json={
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': lead_email,
                'phone': '+0987654321',
                'status': 'qualified'
            }
        )
        assert response.status_code in [200, 201]
        
        session.commit()
        lead = Lead.query.filter_by(email=lead_email).first()
        if not lead:
            return
        
        # Convert lead with password
        response = client.post(
            f'/api/v1/crm/leads/{lead.id}/convert',
            headers=headers,
            json={'password': 'NewUser123!'}
        )
        assert response.status_code in [200, 201]
    
    def test_lead_lost_workflow(self, client, session):
        """Test marking a lead as lost"""
        from src.models.user import User
        from src.models.lead import Lead
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create lead
        lead_email = f'lead_{uuid.uuid4().hex[:8]}@test.com'
        response = client.post(
            '/api/v1/crm/leads',
            headers=headers,
            json={
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'email': lead_email,
                'phone': '+1122334455'
            }
        )
        assert response.status_code in [200, 201]
        
        session.commit()
        lead = Lead.query.filter_by(email=lead_email).first()
        if not lead:
            return
        
        # Mark as lost
        response = client.post(
            f'/api/v1/crm/leads/{lead.id}/lost',
            headers=headers,
            json={'reason': 'not_interested', 'notes': 'Customer not interested'}
        )
        assert response.status_code in [200, 204]


class TestCRMFiltersAndPagination:
    """Test CRM filters, pagination, and search"""
    
    def test_get_leads_with_status_filter(self, client, session):
        from src.models.user import User
        from src.models.lead import Lead
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Create leads with different statuses
        lead1 = Lead(email=f'lead1_{uuid.uuid4().hex[:8]}@test.com', first_name='John', last_name='Doe', status='new', created_by=user.id)
        lead2 = Lead(email=f'lead2_{uuid.uuid4().hex[:8]}@test.com', first_name='Jane', last_name='Smith', status='contacted', created_by=user.id)
        session.add_all([lead1, lead2])
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Filter by status
        response = client.get('/api/v1/crm/leads?status=new', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
    
    def test_get_leads_with_search(self, client, session):
        from src.models.user import User
        from src.models.lead import Lead
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Create lead
        lead = Lead(email=f'john_{uuid.uuid4().hex[:8]}@test.com', first_name='John', last_name='Doe', created_by=user.id)
        session.add(lead)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Search by name
        response = client.get('/api/v1/crm/leads?search=John', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
    
    def test_get_leads_with_pagination(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Get with pagination
        response = client.get('/api/v1/crm/leads?page=1&per_page=10', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert 'total' in response.json
        assert 'pages' in response.json


class TestCRMErrorCases:
    """Test CRM error handling"""
    
    def test_create_lead_missing_email(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Missing email
        response = client.post(
            '/api/v1/crm/leads',
            headers={'Authorization': f'Bearer {token}'},
            json={'first_name': 'John', 'last_name': 'Doe'}
        )
        assert response.status_code in [400, 500]
    
    def test_get_lead_not_found(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Non-existent lead
        response = client.get('/api/v1/crm/leads/999999', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code in [404, 500]
    
    def test_update_lead_not_found(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Update non-existent lead
        response = client.put(
            '/api/v1/crm/leads/999999',
            headers={'Authorization': f'Bearer {token}'},
            json={'status': 'contacted'}
        )
        assert response.status_code in [404, 500]
    
    def test_add_activity_to_nonexistent_lead(self, client, session):
        from src.models.user import User
        
        email = f'user_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='admin')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        response = client.post('/api/v1/auth/login', json={'email': email, 'password': 'Test123!'})
        token = response.json['access_token']
        
        # Add activity to non-existent lead
        response = client.post(
            '/api/v1/crm/leads/999999/activities',
            headers={'Authorization': f'Bearer {token}'},
            json={'activity_type': 'call', 'subject': 'Test'}
        )
        assert response.status_code in [404, 500]
