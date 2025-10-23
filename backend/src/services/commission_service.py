"""
Commission Service
Handles automatic commission calculation and tracking
"""
from src.database import db
from src.models import Commission, Agent, Referral, Challenge, User
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class CommissionService:
    """Service for managing commissions"""
    
    @staticmethod
    def calculate_and_create_commission(challenge_id, sale_amount):
        """
        Calculate and create commission when a challenge is purchased
        
        Args:
            challenge_id: ID of the purchased challenge
            sale_amount: Total sale amount
            
        Returns:
            Commission object if created, None otherwise
        """
        try:
            # Get the challenge
            challenge = Challenge.query.get(challenge_id)
            if not challenge:
                logger.error(f"Challenge {challenge_id} not found")
                return None
            
            # Get the user who purchased
            user = User.query.get(challenge.user_id)
            if not user:
                logger.error(f"User {challenge.user_id} not found")
                return None
            
            # Check if user was referred by an agent
            referral = Referral.query.filter_by(
                referred_user_id=user.id,
                status='active'
            ).first()
            
            if not referral:
                logger.info(f"No active referral found for user {user.id}")
                return None
            
            # Get the agent
            agent = Agent.query.get(referral.agent_id)
            if not agent or not agent.is_active:
                logger.warning(f"Agent {referral.agent_id} not found or inactive")
                return None
            
            # Calculate commission
            commission_rate = agent.commission_rate
            commission_amount = (Decimal(str(sale_amount)) * commission_rate) / Decimal('100')
            
            # Check if commission already exists for this challenge
            existing_commission = Commission.query.filter_by(
                challenge_id=challenge_id
            ).first()
            
            if existing_commission:
                logger.warning(f"Commission already exists for challenge {challenge_id}")
                return existing_commission
            
            # Create commission record
            commission = Commission(
                agent_id=agent.id,
                referral_id=referral.id,
                challenge_id=challenge_id,
                sale_amount=sale_amount,
                commission_rate=commission_rate,
                commission_amount=commission_amount,
                status='pending'
            )
            
            db.session.add(commission)
            
            # Update agent statistics
            agent.total_sales = (agent.total_sales or Decimal('0')) + Decimal(str(sale_amount))
            agent.pending_balance = (agent.pending_balance or Decimal('0')) + commission_amount
            
            # Update referral statistics
            referral.total_purchases = (referral.total_purchases or 0) + 1
            referral.total_spent = (referral.total_spent or Decimal('0')) + Decimal(str(sale_amount))
            
            db.session.commit()
            
            logger.info(f"Commission created: {commission.id} for agent {agent.id}, amount: {commission_amount}")
            
            # Send email notification
            try:
                from src.services.email_service import EmailService
                EmailService.send_commission_earned_email(agent.user, commission, challenge)
            except Exception as email_error:
                logger.error(f"Failed to send commission email: {email_error}")
            
            return commission
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating commission: {str(e)}")
            return None
    
    @staticmethod
    def approve_commission(commission_id, approved_by_id):
        """
        Approve a commission
        
        Args:
            commission_id: ID of the commission
            approved_by_id: ID of the user approving
            
        Returns:
            Commission object if approved, None otherwise
        """
        try:
            commission = Commission.query.get(commission_id)
            if not commission:
                return None
            
            if commission.status != 'pending':
                logger.warning(f"Commission {commission_id} is not pending")
                return None
            
            commission.status = 'approved'
            commission.approved_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Commission {commission_id} approved by user {approved_by_id}")
            
            return commission
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error approving commission: {str(e)}")
            return None
    
    @staticmethod
    def mark_commission_paid(commission_id, payment_method, transaction_id):
        """
        Mark a commission as paid
        
        Args:
            commission_id: ID of the commission
            payment_method: Payment method used
            transaction_id: Transaction ID
            
        Returns:
            Commission object if marked paid, None otherwise
        """
        try:
            commission = Commission.query.get(commission_id)
            if not commission:
                return None
            
            if commission.status != 'approved':
                logger.warning(f"Commission {commission_id} is not approved")
                return None
            
            # Get agent
            agent = Agent.query.get(commission.agent_id)
            if not agent:
                return None
            
            # Update commission
            commission.status = 'paid'
            commission.paid_at = datetime.utcnow()
            commission.payment_method = payment_method
            commission.transaction_id = transaction_id
            
            # Update agent balances
            agent.pending_balance = (agent.pending_balance or Decimal('0')) - commission.commission_amount
            agent.total_earned = (agent.total_earned or Decimal('0')) + commission.commission_amount
            agent.total_withdrawn = (agent.total_withdrawn or Decimal('0')) + commission.commission_amount
            
            db.session.commit()
            
            logger.info(f"Commission {commission_id} marked as paid")
            
            return commission
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking commission as paid: {str(e)}")
            return None
    
    @staticmethod
    def get_agent_commissions(agent_id, status=None, page=1, per_page=20):
        """
        Get commissions for an agent
        
        Args:
            agent_id: ID of the agent
            status: Filter by status (optional)
            page: Page number
            per_page: Items per page
            
        Returns:
            Paginated commissions
        """
        query = Commission.query.filter_by(agent_id=agent_id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Commission.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return pagination
    
    @staticmethod
    def get_agent_commission_stats(agent_id):
        """
        Get commission statistics for an agent
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Dictionary with statistics
        """
        try:
            agent = Agent.query.get(agent_id)
            if not agent:
                return None
            
            # Get commission counts by status
            pending_count = Commission.query.filter_by(
                agent_id=agent_id,
                status='pending'
            ).count()
            
            approved_count = Commission.query.filter_by(
                agent_id=agent_id,
                status='approved'
            ).count()
            
            paid_count = Commission.query.filter_by(
                agent_id=agent_id,
                status='paid'
            ).count()
            
            # Get total amounts
            pending_amount = db.session.query(
                db.func.sum(Commission.commission_amount)
            ).filter(
                Commission.agent_id == agent_id,
                Commission.status == 'pending'
            ).scalar() or Decimal('0')
            
            approved_amount = db.session.query(
                db.func.sum(Commission.commission_amount)
            ).filter(
                Commission.agent_id == agent_id,
                Commission.status == 'approved'
            ).scalar() or Decimal('0')
            
            paid_amount = db.session.query(
                db.func.sum(Commission.commission_amount)
            ).filter(
                Commission.agent_id == agent_id,
                Commission.status == 'paid'
            ).scalar() or Decimal('0')
            
            return {
                'agent_id': agent_id,
                'commission_rate': float(agent.commission_rate),
                'pending_balance': float(agent.pending_balance),
                'total_earned': float(agent.total_earned),
                'total_withdrawn': float(agent.total_withdrawn),
                'total_sales': float(agent.total_sales),
                'pending': {
                    'count': pending_count,
                    'amount': float(pending_amount)
                },
                'approved': {
                    'count': approved_count,
                    'amount': float(approved_amount)
                },
                'paid': {
                    'count': paid_count,
                    'amount': float(paid_amount)
                },
                'total_commissions': pending_count + approved_count + paid_count,
                'total_commission_amount': float(pending_amount + approved_amount + paid_amount)
            }
            
        except Exception as e:
            logger.error(f"Error getting commission stats: {str(e)}")
            return None

