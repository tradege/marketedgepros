from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from src.models.payout_request import PayoutRequest
from src.models.user import User
from src.models.trading_program import TradingProgram
from src.extensions import db
from src.services.scaling_service import ScalingService

class PayoutService:
    """Service for managing payout requests and processing"""
    
    @staticmethod
    def can_request_payout(user: User, program: TradingProgram) -> Dict:
        """Check if user can request a payout"""
        errors = []
        
        # Check if user has available balance
        if not user.available_balance or user.available_balance <= 0:
            errors.append("No available balance to withdraw")
        # Check minimum payout amount (only if balance exists)
        elif user.available_balance < program.minimum_payout_amount:
            errors.append(f"Minimum payout amount is ${program.minimum_payout_amount}")
        
        # Check payout mode specific rules
        if program.payout_mode == "on_demand_rules":
            # Check minimum trading days
            # TODO: Implement trading days calculation
            pass
        
        # Check if there's a pending payout
        pending_payout = db.session.query(PayoutRequest).filter(
            and_(
                PayoutRequest.user_id == user.id,
                PayoutRequest.status.in_(["pending", "approved", "processing"])
            )
        ).first()
        
        if pending_payout:
            errors.append("You already have a pending payout request")
        
        return {
            "can_request": len(errors) == 0,
            "errors": errors,
            "available_balance": float(user.available_balance) if user.available_balance else 0,
            "minimum_amount": float(program.minimum_payout_amount),
            "payout_mode": program.payout_mode,
            "profit_split": program.profit_split_percentage
        }
    
    @staticmethod
    def request_payout(
        user: User,
        program: TradingProgram,
        amount: Decimal,
        payment_method: str,
        payment_details: Dict = None
    ) -> PayoutRequest:
        """Create a new payout request"""
        
        # Validate
        validation = PayoutService.can_request_payout(user, program)
        if not validation["can_request"]:
            raise ValueError(", ".join(validation["errors"]))
        
        # Validate amount
        if amount > user.available_balance:
            raise ValueError("Amount exceeds available balance")
        
        if amount < program.minimum_payout_amount:
            raise ValueError(f"Minimum payout amount is ${program.minimum_payout_amount}")
        
        # Calculate profit split amount
        profit_split_percentage = program.profit_split_percentage / 100
        profit_split_amount = amount * Decimal(str(profit_split_percentage))
        
        # Create payout request
        payout = PayoutRequest(
            user_id=user.id,
            program_id=program.id,
            amount=amount,
            profit_split_amount=profit_split_amount,
            status="pending",
            payout_mode=program.payout_mode,
            payment_method=payment_method,
            payment_details=payment_details,
            request_date=datetime.utcnow()
        )
        
        db.session.add(payout)
        
        # Deduct from available balance (reserve it)
        user.available_balance -= amount
        
        db.session.commit()
        
        # TODO: Send notification email
        
        return payout
    
    @staticmethod
    def approve_payout(payout_id: int, approver_id: int, notes: str = None) -> PayoutRequest:
        """Approve a payout request"""
        payout = db.session.query(PayoutRequest).get(payout_id)
        
        if not payout:
            raise ValueError("Payout request not found")
        
        if payout.status != "pending":
            raise ValueError(f"Cannot approve payout with status: {payout.status}")
        
        payout.status = "approved"
        payout.approved_by = approver_id
        payout.approved_date = datetime.utcnow()
        payout.notes = notes
        
        db.session.commit()
        
        # Update scaling progress
        try:
            ScalingService.update_profit(payout.user_id, payout.amount)
        except Exception as e:
            # Log error but don't fail the payout approval
            print(f"Error updating scaling progress: {e}")
        
        # TODO: Send notification email
        # TODO: Trigger payment processing
        
        return payout
    
    @staticmethod
    def reject_payout(payout_id: int, approver_id: int, reason: str) -> PayoutRequest:
        """Reject a payout request"""
        payout = db.session.query(PayoutRequest).get(payout_id)
        
        if not payout:
            raise ValueError("Payout request not found")
        
        if payout.status != "pending":
            raise ValueError(f"Cannot reject payout with status: {payout.status}")
        
        # Return amount to available balance
        user = db.session.query(User).get(payout.user_id)
        user.available_balance += payout.amount
        
        payout.status = "rejected"
        payout.approved_by = approver_id
        payout.approved_date = datetime.utcnow()
        payout.rejection_reason = reason
        
        db.session.commit()
        
        # TODO: Send notification email
        
        return payout
    
    @staticmethod
    def mark_as_paid(payout_id: int, notes: str = None) -> PayoutRequest:
        """Mark a payout as paid"""
        payout = db.session.query(PayoutRequest).get(payout_id)
        
        if not payout:
            raise ValueError("Payout request not found")
        
        if payout.status not in ["approved", "processing"]:
            raise ValueError(f"Cannot mark as paid payout with status: {payout.status}")
        
        payout.status = "paid"
        payout.paid_date = datetime.utcnow()
        if notes:
            payout.notes = (payout.notes or "") + f"\n{notes}"
        
        # Update user statistics
        user = db.session.query(User).get(payout.user_id)
        user.total_withdrawn += payout.profit_split_amount
        user.payout_count += 1
        
        db.session.commit()
        
        # TODO: Send notification email
        
        return payout
    
    @staticmethod
    def get_user_payouts(user_id: int, status: str = None) -> List[PayoutRequest]:
        """Get all payouts for a user"""
        query = db.session.query(PayoutRequest).filter(PayoutRequest.user_id == user_id)
        
        if status:
            query = query.filter(PayoutRequest.status == status)
        
        return query.order_by(PayoutRequest.request_date.desc()).all()
    
    @staticmethod
    def get_pending_payouts() -> List[PayoutRequest]:
        """Get all pending payout requests"""
        return db.session.query(PayoutRequest).filter(
            PayoutRequest.status == "pending"
        ).order_by(PayoutRequest.request_date.asc()).all()
    
    @staticmethod
    def get_payout_statistics(user_id: int = None) -> Dict:
        """Get payout statistics"""
        query = db.session.query(PayoutRequest)
        
        if user_id:
            query = query.filter(PayoutRequest.user_id == user_id)
        
        total_requested = query.count()
        total_pending = query.filter(PayoutRequest.status == "pending").count()
        total_approved = query.filter(PayoutRequest.status == "approved").count()
        total_paid = query.filter(PayoutRequest.status == "paid").count()
        total_rejected = query.filter(PayoutRequest.status == "rejected").count()
        
        total_amount_paid = db.session.query(
            db.func.sum(PayoutRequest.profit_split_amount)
        ).filter(
            and_(
                PayoutRequest.status == "paid",
                PayoutRequest.user_id == user_id if user_id else True
            )
        ).scalar() or 0
        
        return {
            "total_requested": total_requested,
            "total_pending": total_pending,
            "total_approved": total_approved,
            "total_paid": total_paid,
            "total_rejected": total_rejected,
            "total_amount_paid": float(total_amount_paid),
            "success_rate": (total_paid / total_requested * 100) if total_requested > 0 else 0
        }
