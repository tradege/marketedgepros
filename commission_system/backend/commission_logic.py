"""
Commission Calculation and Business Logic
MarketEdgePros - Prop Trading Firm Platform
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


def calculate_commission(db: Session, customer_id: int, order_amount: float, order_id: str):
    """
    Calculate and record commission when a customer makes a payment.
    
    Args:
        db: Database session
        customer_id: ID of the customer who made the payment
        order_amount: Payment amount in USD
        order_id: Unique order/payment identifier
        
    Returns:
        dict: Commission details including affiliate info and amount
    """
    from models_commission import User, Commission
    
    try:
        # Get customer
        customer = db.query(User).filter(User.id == customer_id).first()
        if not customer:
            logger.error(f"Customer {customer_id} not found")
            return {'error': 'Customer not found'}
        
        # Check if customer has a referrer (affiliate)
        if not customer.parent_id:
            logger.info(f"Customer {customer_id} has no referrer, no commission to calculate")
            return {'message': 'No referrer, no commission'}
        
        # Get affiliate (referrer)
        affiliate = db.query(User).filter(User.id == customer.parent_id).first()
        if not affiliate:
            logger.error(f"Affiliate {customer.parent_id} not found")
            return {'error': 'Affiliate not found'}
        
        # Calculate commission amount
        commission_amount = order_amount * (affiliate.commission_rate / 100)
        
        # Create commission record
        commission = Commission(
            affiliate_id=affiliate.id,
            customer_id=customer.id,
            order_id=order_id,
            amount=commission_amount,
            commission_rate=affiliate.commission_rate,
            status='pending',
            created_at=datetime.utcnow()
        )
        db.add(commission)
        
        # Increment paid customers count
        affiliate.paid_customers_count += 1
        
        # Add to pending commission
        affiliate.pending_commission += commission_amount
        
        # Check if affiliate reached 10 paid customers threshold
        if affiliate.paid_customers_count >= 10 and not affiliate.can_withdraw:
            # Release all pending commissions!
            release_pending_commissions(db, affiliate.id)
        
        db.commit()
        
        logger.info(f"Commission created: ${commission_amount} for affiliate {affiliate.id} from customer {customer.id}")
        
        return {
            'success': True,
            'commission_id': commission.id,
            'affiliate_id': affiliate.id,
            'amount': commission_amount,
            'paid_customers_count': affiliate.paid_customers_count,
            'threshold_reached': affiliate.paid_customers_count >= 10
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error calculating commission: {str(e)}")
        return {'error': str(e)}


def release_pending_commissions(db: Session, affiliate_id: int):
    """
    Release all pending commissions to affiliate's balance when they reach 10 customers.
    
    Args:
        db: Database session
        affiliate_id: ID of the affiliate
    """
    from models_commission import User, Commission
    
    try:
        affiliate = db.query(User).filter(User.id == affiliate_id).first()
        if not affiliate:
            return
        
        # Get all pending commissions
        pending_commissions = db.query(Commission).filter(
            Commission.affiliate_id == affiliate_id,
            Commission.status == 'pending'
        ).all()
        
        total_released = 0
        for commission in pending_commissions:
            commission.status = 'released'
            commission.released_at = datetime.utcnow()
            total_released += commission.amount
        
        # Move from pending to balance
        affiliate.commission_balance += affiliate.pending_commission
        affiliate.pending_commission = 0
        affiliate.can_withdraw = True
        
        db.commit()
        
        logger.info(f"Released ${total_released} in commissions for affiliate {affiliate_id}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error releasing commissions: {str(e)}")


def get_affiliate_stats(db: Session, user_id: int):
    """
    Get comprehensive statistics for an affiliate.
    
    Args:
        db: Database session
        user_id: ID of the affiliate
        
    Returns:
        dict: Affiliate statistics including commissions, balance, etc.
    """
    from models_commission import User, Commission
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {'error': 'User not found'}
        
        # Get all commissions
        commissions = db.query(Commission).filter(
            Commission.affiliate_id == user_id
        ).order_by(Commission.created_at.desc()).all()
        
        # Calculate totals
        total_earned = db.query(func.sum(Commission.amount)).filter(
            Commission.affiliate_id == user_id
        ).scalar() or 0
        
        total_paid = db.query(func.sum(Commission.amount)).filter(
            Commission.affiliate_id == user_id,
            Commission.status == 'paid'
        ).scalar() or 0
        
        # Format commission list
        commission_list = []
        for comm in commissions:
            customer = db.query(User).filter(User.id == comm.customer_id).first()
            commission_list.append({
                'id': comm.id,
                'customer_name': customer.name if customer else 'Unknown',
                'customer_email': customer.email if customer else 'Unknown',
                'amount': comm.amount,
                'status': comm.status,
                'created_at': comm.created_at.isoformat() if comm.created_at else None,
                'released_at': comm.released_at.isoformat() if comm.released_at else None,
            })
        
        return {
            'paid_customers_count': user.paid_customers_count,
            'pending_commission': user.pending_commission,
            'commission_balance': user.commission_balance,
            'can_withdraw': user.can_withdraw,
            'commission_rate': user.commission_rate,
            'total_earned': total_earned,
            'total_paid': total_paid,
            'commissions': commission_list,
            'threshold_progress': min(user.paid_customers_count, 10),
            'threshold_target': 10,
        }
        
    except Exception as e:
        logger.error(f"Error getting affiliate stats: {str(e)}")
        return {'error': str(e)}


def can_request_withdrawal(db: Session, user_id: int):
    """
    Check if user can request a withdrawal.
    
    Args:
        db: Database session
        user_id: ID of the user
        
    Returns:
        tuple: (can_withdraw: bool, reason: str, days_remaining: int)
    """
    from models_commission import User
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return (False, 'User not found', 0)
        
        # Check if user has balance
        if user.commission_balance <= 0:
            return (False, 'No balance available', 0)
        
        # Check if user reached 10 customers threshold
        if not user.can_withdraw:
            remaining = 10 - user.paid_customers_count
            return (False, f'Need {remaining} more paying customers', 0)
        
        # Check if 30 days passed since last withdrawal
        if user.last_withdrawal_date:
            days_since_last = (datetime.utcnow() - user.last_withdrawal_date).days
            if days_since_last < 30:
                days_remaining = 30 - days_since_last
                return (False, f'Wait {days_remaining} more days', days_remaining)
        
        return (True, 'Eligible to withdraw', 0)
        
    except Exception as e:
        logger.error(f"Error checking withdrawal eligibility: {str(e)}")
        return (False, str(e), 0)


def process_hierarchy_commissions(db: Session, customer_id: int, order_amount: float, order_id: str):
    """
    Process commissions for entire hierarchy (customer -> affiliate -> master -> super_master).
    
    Args:
        db: Database session
        customer_id: ID of the customer who made payment
        order_amount: Payment amount in USD
        order_id: Unique order identifier
        
    Returns:
        list: List of commission records created
    """
    from models_commission import User, Commission
    
    commissions_created = []
    
    try:
        # Get customer
        customer = db.query(User).filter(User.id == customer_id).first()
        if not customer or not customer.parent_id:
            return commissions_created
        
        # Walk up the hierarchy using tree_path
        current_user = customer
        processed_ids = set()
        
        while current_user.parent_id and current_user.parent_id not in processed_ids:
            parent = db.query(User).filter(User.id == current_user.parent_id).first()
            if not parent:
                break
            
            processed_ids.add(parent.id)
            
            # Calculate commission for this level
            if parent.commission_rate > 0:
                commission_amount = order_amount * (parent.commission_rate / 100)
                
                # Create commission record
                commission = Commission(
                    affiliate_id=parent.id,
                    customer_id=customer.id,
                    order_id=order_id,
                    amount=commission_amount,
                    commission_rate=parent.commission_rate,
                    status='pending',
                    created_at=datetime.utcnow()
                )
                db.add(commission)
                commissions_created.append(commission)
                
                # Increment paid customers count (only for direct referrer)
                if parent.id == customer.parent_id:
                    parent.paid_customers_count += 1
                
                # Add to pending commission
                parent.pending_commission += commission_amount
                
                # Check threshold
                if parent.paid_customers_count >= 10 and not parent.can_withdraw:
                    release_pending_commissions(db, parent.id)
            
            current_user = parent
        
        db.commit()
        logger.info(f"Created {len(commissions_created)} commission records for order {order_id}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing hierarchy commissions: {str(e)}")
    
    return commissions_created


def get_customers_by_affiliate(db: Session, affiliate_id: int):
    """
    Get all customers referred by an affiliate.
    
    Args:
        db: Database session
        affiliate_id: ID of the affiliate
        
    Returns:
        list: List of customer details
    """
    from models_commission import User
    
    try:
        customers = db.query(User).filter(
            User.parent_id == affiliate_id,
            User.role == 'customer'
        ).all()
        
        customer_list = []
        for customer in customers:
            # Check if customer has paid
            has_paid = db.query(Commission).filter(
                Commission.customer_id == customer.id
            ).first() is not None
            
            customer_list.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'created_at': customer.created_at.isoformat() if hasattr(customer, 'created_at') else None,
                'has_paid': has_paid,
            })
        
        return customer_list
        
    except Exception as e:
        logger.error(f"Error getting customers: {str(e)}")
        return []

