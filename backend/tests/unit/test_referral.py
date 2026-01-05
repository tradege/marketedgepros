"""
Unit tests for Referral System
"""
import pytest
from decimal import Decimal
from datetime import datetime
from src.models import Referral

@pytest.mark.unit
class TestReferralSystem:
    """Test referral system functionality"""
    
    def test_create_referral(self, session, agent_user, referral_user):
        """Test creating a referral"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REF123',
            status='pending'
        )
        session.add(referral)
        session.commit()
        
        assert referral.id is not None
        assert referral.agent_id == agent.id
        assert referral.referred_user_id == referral_user.id
        assert referral.referral_code == 'REF123'
    
    def test_referral_status_transitions(self, session, agent_user, referral_user):
        """Test referral status transitions"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REF456',
            status='pending'
        )
        session.add(referral)
        session.commit()
        
        assert referral.status == 'pending'
        
        # Activate after first purchase
        referral.status = 'active'
        referral.first_purchase_at = datetime.utcnow()
        session.commit()
        
        assert referral.status == 'active'
        assert referral.first_purchase_at is not None
    
    def test_referral_purchase_tracking(self, session, agent_user, referral_user):
        """Test tracking referral purchases"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REF789',
            status='active',
            total_purchases=0,
            total_spent=Decimal('0.00')
        )
        session.add(referral)
        session.commit()
        
        # Track first purchase
        referral.total_purchases = 1
        referral.total_spent = Decimal('100.00')
        session.commit()
        
        assert referral.total_purchases == 1
        assert referral.total_spent == Decimal('100.00')
        
        # Track second purchase
        referral.total_purchases = 2
        referral.total_spent = Decimal('250.00')
        session.commit()
        
        assert referral.total_purchases == 2
        assert referral.total_spent == Decimal('250.00')
    
    def test_referral_code_tracking(self, session, agent_user, referral_user):
        """Test referral code tracking"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='AGENT001',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )
        session.add(referral)
        session.commit()
        
        assert referral.referral_code == 'AGENT001'
        assert referral.ip_address == '192.168.1.1'
        assert referral.user_agent == 'Mozilla/5.0'
    
    def test_referral_to_dict(self, session, agent_user, referral_user):
        """Test referral serialization"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REFDICT',
            status='active',
            total_purchases=5,
            total_spent=Decimal('500.00')
        )
        session.add(referral)
        session.commit()
        
        ref_dict = referral.to_dict()
        
        assert ref_dict['referral_code'] == 'REFDICT'
        assert ref_dict['status'] == 'active'
        assert ref_dict['total_purchases'] == 5
        assert ref_dict['total_spent'] == 500.00
    
    def test_referral_relationship_with_user(self, session, agent_user, referral_user):
        """Test referral relationship with referred user"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REFREL'
        )
        session.add(referral)
        session.commit()
        
        assert referral.referred_user is not None
        assert referral.referred_user.id == referral_user.id
    
    def test_multiple_referrals_per_agent(self, session, agent_user):
        """Test agent with multiple referrals"""
        from src.models import Agent, User
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        # Create multiple referred users
        for i in range(3):
            user = User(
                email=f'referred{i}@example.com',
                first_name=f'Referred{i}',
                last_name='User',
                role='trader',
                parent_id=agent_user.id,
                is_active=True
            )
            user.set_password('Password123!')
            session.add(user)
            session.commit()
            
            referral = Referral(
                agent_id=agent.id,
                referred_user_id=user.id,
                referral_code=f'REF{i}'
            )
            session.add(referral)
        
        session.commit()
        
        referrals = Referral.query.filter_by(agent_id=agent.id).all()
        assert len(referrals) >= 3
    
    def test_referral_inactive_status(self, session, agent_user, referral_user):
        """Test marking referral as inactive"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REFINACT',
            status='active'
        )
        session.add(referral)
        session.commit()
        
        # Mark as inactive
        referral.status = 'inactive'
        session.commit()
        
        assert referral.status == 'inactive'
    
    def test_referral_first_purchase_tracking(self, session, agent_user, referral_user):
        """Test tracking first purchase date"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REFFIRST',
            status='pending'
        )
        session.add(referral)
        session.commit()
        
        assert referral.first_purchase_at is None
        
        # Record first purchase
        now = datetime.utcnow()
        referral.first_purchase_at = now
        referral.status = 'active'
        session.commit()
        
        assert referral.first_purchase_at == now
    
    def test_referral_decimal_precision(self, session, agent_user, referral_user):
        """Test referral decimal precision for total_spent"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        referral = Referral(
            agent_id=agent.id,
            referred_user_id=referral_user.id,
            referral_code='REFPREC',
            total_spent=Decimal('123.45')
        )
        session.add(referral)
        session.commit()
        
        assert referral.total_spent == Decimal('123.45')
