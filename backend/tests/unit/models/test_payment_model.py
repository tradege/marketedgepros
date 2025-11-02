"""
Unit tests for Payment model
"""
import pytest
from decimal import Decimal
from datetime import datetime
from src.models import Payment, User

@pytest.mark.unit
@pytest.mark.payment
class TestPaymentModel:
    """Test Payment model functionality"""
    
    def test_create_payment(self, session, trader_user):
        """Test creating a payment"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='stripe',
            payment_type='credit_card',
            status='pending',
            purpose='challenge_purchase',
            reference_id=1
        )
        session.add(payment)
        session.commit()
        
        assert payment.id is not None
        assert payment.user_id == trader_user.id
        assert payment.amount == Decimal('100.00')
        assert payment.currency == 'USD'
        assert payment.status == 'pending'
        assert payment.approval_status == 'approved'  # Default
    
    def test_payment_status_transitions(self, session, trader_user):
        """Test payment status transitions"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('50.00'),
            status='pending'
        )
        session.add(payment)
        session.commit()
        
        # Pending -> Completed
        payment.status = 'completed'
        payment.completed_at = datetime.utcnow()
        session.commit()
        
        assert payment.status == 'completed'
        assert payment.completed_at is not None
        
        # Can transition to refunded
        payment.status = 'refunded'
        session.commit()
        
        assert payment.status == 'refunded'
    
    def test_payment_approval_workflow(self, session, trader_user, admin_user):
        """Test payment approval workflow for cash/free payments"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('200.00'),
            payment_type='cash',
            approval_status='pending',
            status='pending'
        )
        session.add(payment)
        session.commit()
        
        assert payment.approval_status == 'pending'
        
        # Approve payment
        payment.approval_status = 'approved'
        payment.approved_by = admin_user.id
        payment.approved_at = datetime.utcnow()
        session.commit()
        
        assert payment.approval_status == 'approved'
        assert payment.approved_by == admin_user.id
        assert payment.approved_at is not None
    
    def test_payment_rejection(self, session, trader_user, admin_user):
        """Test payment rejection"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('300.00'),
            payment_type='cash',
            approval_status='pending'
        )
        session.add(payment)
        session.commit()
        
        # Reject payment
        payment.approval_status = 'rejected'
        payment.approved_by = admin_user.id
        payment.rejection_reason = 'Invalid receipt'
        payment.admin_notes = 'Receipt does not match amount'
        session.commit()
        
        assert payment.approval_status == 'rejected'
        assert payment.rejection_reason == 'Invalid receipt'
        assert payment.admin_notes is not None
    
    def test_payment_with_transaction_id(self, session, trader_user):
        """Test payment with unique transaction ID"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('75.00'),
            transaction_id='txn_123456789'
        )
        session.add(payment)
        session.commit()
        
        # Verify uniqueness
        found = Payment.query.filter_by(transaction_id='txn_123456789').first()
        assert found is not None
        assert found.id == payment.id
    
    def test_payment_to_dict(self, session, trader_user):
        """Test payment serialization"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('150.00'),
            currency='USD',
            payment_method='paypal',
            status='completed'
        )
        session.add(payment)
        session.commit()
        
        payment_dict = payment.to_dict()
        
        assert payment_dict['id'] == payment.id
        assert payment_dict['user_id'] == trader_user.id
        assert payment_dict['amount'] == 150.00
        assert payment_dict['currency'] == 'USD'
        assert payment_dict['status'] == 'completed'
    
    def test_payment_purpose_and_reference(self, session, trader_user):
        """Test payment purpose and reference tracking"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('500.00'),
            purpose='challenge_purchase',
            reference_id=42
        )
        session.add(payment)
        session.commit()
        
        assert payment.purpose == 'challenge_purchase'
        assert payment.reference_id == 42
    
    def test_payment_relationship_with_user(self, session, trader_user):
        """Test payment relationship with user"""
        payment1 = Payment(user_id=trader_user.id, amount=Decimal('100.00'))
        payment2 = Payment(user_id=trader_user.id, amount=Decimal('200.00'))
        
        session.add_all([payment1, payment2])
        session.commit()
        
        # Access payments through user
        user_payments = trader_user.payments
        assert len(user_payments) >= 2
        assert payment1 in user_payments
        assert payment2 in user_payments
    
    def test_payment_decimal_precision(self, session, trader_user):
        """Test payment amount decimal precision"""
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('99.99')
        )
        session.add(payment)
        session.commit()
        
        # Reload from database
        session.refresh(payment)
        
        assert payment.amount == Decimal('99.99')
        assert str(payment.amount) == '99.99'
    
    def test_payment_provider_response(self, session, trader_user):
        """Test storing provider response"""
        import json
        
        provider_data = {
            'stripe_payment_intent': 'pi_123456',
            'status': 'succeeded',
            'amount': 10000
        }
        
        payment = Payment(
            user_id=trader_user.id,
            amount=Decimal('100.00'),
            payment_method='stripe',
            provider_response=json.dumps(provider_data)
        )
        session.add(payment)
        session.commit()
        
        # Verify provider response is stored
        assert payment.provider_response is not None
        stored_data = json.loads(payment.provider_response)
        assert stored_data['stripe_payment_intent'] == 'pi_123456'
