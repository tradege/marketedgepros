"""
Unit tests for Commission model
"""
import pytest
from decimal import Decimal
from datetime import datetime
from src.models import Commission, Agent, Referral

@pytest.mark.unit
@pytest.mark.commission
class TestCommissionModel:
    """Test Commission model functionality"""
    
    def test_create_commission(self, session, agent_user, referral, challenge):
        """Test creating a commission"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        # referral fixture is used instead
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('100.00'),
            commission_rate=Decimal('10.00'),
            commission_amount=Decimal('10.00'),
            status='pending'
        )
        session.add(commission)
        session.commit()
        
        assert commission.id is not None
        assert commission.agent_id == agent.id
        assert commission.sale_amount == Decimal('100.00')
        assert commission.commission_rate == Decimal('10.00')
        assert commission.commission_amount == Decimal('10.00')
        assert commission.status == 'pending'
    
    def test_calculate_commission_basic(self):
        """Test basic commission calculation"""
        # 10% of 100 = 10
        result = Commission.calculate_commission(100, 10)
        assert result == Decimal('10.00')
        
        # 15% of 200 = 30
        result = Commission.calculate_commission(200, 15)
        assert result == Decimal('30.00')
        
        # 5.5% of 1000 = 55
        result = Commission.calculate_commission(1000, 5.5)
        assert result == Decimal('55.00')
    
    def test_calculate_commission_with_decimals(self):
        """Test commission calculation with decimal values"""
        # 10% of 99.99 = 9.999 -> 10.00 (rounded)
        result = Commission.calculate_commission(Decimal('99.99'), Decimal('10.00'))
        assert result == Decimal('10.00')
        
        # 7.5% of 133.33 = 9.99975 -> 10.00 (rounded)
        result = Commission.calculate_commission(Decimal('133.33'), Decimal('7.5'))
        assert result == Decimal('10.00')
    
    def test_calculate_commission_edge_cases(self):
        """Test commission calculation edge cases"""
        # Zero amount
        result = Commission.calculate_commission(0, 10)
        assert result == Decimal('0')
        
        # Zero rate
        result = Commission.calculate_commission(100, 0)
        assert result == Decimal('0')
        
        # None values
        result = Commission.calculate_commission(None, 10)
        assert result == Decimal('0')
        
        result = Commission.calculate_commission(100, None)
        assert result == Decimal('0')
    
    def test_calculate_commission_invalid_rate(self):
        """Test commission calculation with invalid rate"""
        # Rate > 100
        with pytest.raises(ValueError, match='Commission rate must be between 0 and 100'):
            Commission.calculate_commission(100, 150)
        
        # Negative rate
        with pytest.raises(ValueError, match='Commission rate must be between 0 and 100'):
            Commission.calculate_commission(100, -5)
    
    def test_validate_commission_correct(self, session, agent_user, referral, challenge):
        """Test validating a correctly calculated commission"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('200.00'),
            commission_rate=Decimal('10.00'),
            commission_amount=Decimal('20.00')
        )
        
        assert commission.validate_commission() is True
    
    def test_validate_commission_incorrect(self, session, agent_user, referral, challenge):
        """Test validating an incorrectly calculated commission"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('200.00'),
            commission_rate=Decimal('10.00'),
            commission_amount=Decimal('25.00')  # Wrong! Should be 20.00
        )
        
        assert commission.validate_commission() is False
    
    def test_commission_status_transitions(self, session, agent_user, referral_user, referral, challenge):
        """Test commission status transitions"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('100.00'),
            commission_rate=Decimal('10.00'),
            commission_amount=Decimal('10.00'),
            status='pending'
        )
        session.add(commission)
        session.commit()
        
        # Pending -> Approved
        commission.status = 'approved'
        commission.approved_at = datetime.utcnow()
        session.commit()
        
        assert commission.status == 'approved'
        assert commission.approved_at is not None
        
        # Approved -> Paid
        commission.status = 'paid'
        commission.paid_at = datetime.utcnow()
        commission.payment_method = 'bank_transfer'
        commission.transaction_id = 'txn_abc123'
        session.commit()
        
        assert commission.status == 'paid'
        assert commission.paid_at is not None
        assert commission.transaction_id == 'txn_abc123'
    
    def test_commission_to_dict(self, session, agent_user, referral_user, referral, challenge):
        """Test commission serialization"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('150.00'),
            commission_rate=Decimal('12.00'),
            commission_amount=Decimal('18.00'),
            status='approved'
        )
        session.add(commission)
        session.commit()
        
        commission_dict = commission.to_dict()
        
        assert commission_dict['id'] == commission.id
        assert commission_dict['agent_id'] == agent.id
        assert commission_dict['sale_amount'] == 150.00
        assert commission_dict['commission_rate'] == 12.00
        assert commission_dict['commission_amount'] == 18.00
        assert commission_dict['status'] == 'approved'
    
    def test_commission_relationships(self, session, agent_user, referral_user, referral, challenge):
        """Test commission relationships"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('100.00'),
            commission_rate=Decimal('10.00'),
            commission_amount=Decimal('10.00')
        )
        session.add(commission)
        session.commit()
        
        # Test relationships
        assert commission.referral is not None
        assert commission.referral.id == referral.id
        assert commission.challenge is not None
        assert commission.challenge.id == challenge.id
    
    def test_commission_decimal_precision(self, session, agent_user, referral_user, referral, challenge):
        """Test commission decimal precision"""
        from src.models import Agent, Referral
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        commission = Commission(
            agent_id=agent.id,
            referral_id=referral.id,
            challenge_id=challenge.id,
            sale_amount=Decimal('123.45'),
            commission_rate=Decimal('7.89'),
            commission_amount=Decimal('9.74')  # 123.45 * 7.89 / 100 = 9.74
        )
        session.add(commission)
        session.commit()
        
        # Reload from database
        session.refresh(commission)
        
        assert commission.sale_amount == Decimal('123.45')
        assert commission.commission_rate == Decimal('7.89')
        assert commission.commission_amount == Decimal('9.74')
