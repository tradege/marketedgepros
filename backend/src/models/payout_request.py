from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, JSON
from src.extensions import db

class PayoutRequest(db.Model):
    """Model for trader payout requests"""
    __tablename__ = "payout_requests"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(Integer, ForeignKey("trading_programs.id", ondelete="SET NULL"))
    amount = Column(Numeric(10, 2), nullable=False)
    profit_split_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    # Status: pending, approved, processing, paid, rejected, cancelled
    payout_mode = Column(String(20), nullable=False)
    # Mode: on_demand_full, on_demand_rules, standard
    payment_method = Column(String(50))
    payment_details = Column(JSON)
    request_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    approved_date = Column(DateTime)
    processed_date = Column(DateTime)
    paid_date = Column(DateTime)
    approved_by = Column(Integer, ForeignKey("users.id"))
    notes = Column(Text)
    rejection_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<PayoutRequest {self.id}: ${self.amount} - {self.status}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "program_id": self.program_id,
            "amount": float(self.amount) if self.amount else 0,
            "profit_split_amount": float(self.profit_split_amount) if self.profit_split_amount else 0,
            "status": self.status,
            "payout_mode": self.payout_mode,
            "payment_method": self.payment_method,
            "payment_details": self.payment_details,
            "request_date": self.request_date.isoformat() if self.request_date else None,
            "approved_date": self.approved_date.isoformat() if self.approved_date else None,
            "processed_date": self.processed_date.isoformat() if self.processed_date else None,
            "paid_date": self.paid_date.isoformat() if self.paid_date else None,
            "approved_by": self.approved_by,
            "notes": self.notes,
            "rejection_reason": self.rejection_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
