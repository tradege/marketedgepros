"""
Comprehensive tests for Leads Routes
"""
import pytest
from src.models.lead import Lead
from src.models.course_enrollment import CourseEnrollment

class TestLeadsRoutes:
    """Test leads routes"""
    
    def test_course_signup_success(self, client):
        """Test successful course signup"""
        response = client.post('/api/v1/leads/course-signup', json={
            'email': 'john@example.com',
            'name': 'John Doe',
            'source': 'facebook'
        })
        
        assert response.status_code == 201
        data = response.json
        assert data['message'] == 'Successfully signed up for the course'
        assert data['email'] == 'john@example.com'
    
    def test_course_signup_missing_email(self, client):
        """Test course signup with missing email"""
        response = client.post('/api/v1/leads/course-signup', json={
            'name': 'John Doe'
        })
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_course_signup_missing_name(self, client):
        """Test course signup with missing name"""
        response = client.post('/api/v1/leads/course-signup', json={
            'email': 'john@example.com'
        })
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_course_signup_existing_lead(self, client):
        """Test course signup with existing lead"""
        # First signup
        client.post('/api/v1/leads/course-signup', json={
            'email': 'existing@example.com',
            'name': 'Existing User'
        })
        
        # Second signup with same email
        response = client.post('/api/v1/leads/course-signup', json={
            'email': 'existing@example.com',
            'name': 'Updated Name'
        })
        
        assert response.status_code == 201
        assert response.json['email'] == 'existing@example.com'
    
    def test_course_signup_single_name(self, client):
        """Test course signup with single name (no last name)"""
        response = client.post('/api/v1/leads/course-signup', json={
            'email': 'single@example.com',
            'name': 'Madonna'
        })
        
        assert response.status_code == 201
        assert response.json['email'] == 'single@example.com'
    
    def test_course_signup_default_source(self, client):
        """Test course signup with default source"""
        response = client.post('/api/v1/leads/course-signup', json={
            'email': 'default@example.com',
            'name': 'Default User'
        })
        
        assert response.status_code == 201
        assert response.json['email'] == 'default@example.com'
    
    def test_course_signup_creates_lead(self, client, app):
        """Test that course signup creates lead in database"""
        client.post('/api/v1/leads/course-signup', json={
            'email': 'newlead@example.com',
            'name': 'New Lead'
        })
        
        with app.app_context():
            lead = Lead.query.filter_by(email='newlead@example.com').first()
            assert lead is not None
            assert lead.first_name == 'New'
            assert lead.last_name == 'Lead'
    
    def test_course_signup_creates_enrollment(self, client, app):
        """Test that course signup creates enrollment"""
        client.post('/api/v1/leads/course-signup', json={
            'email': 'enroll@example.com',
            'name': 'Enroll User'
        })
        
        with app.app_context():
            enrollment = CourseEnrollment.query.filter_by(email='enroll@example.com').first()
            assert enrollment is not None
            assert enrollment.name == 'Enroll User'
