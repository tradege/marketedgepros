from datetime import datetime
from src.database import db

class Trade(db.Model):
    """Individual trade record"""
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    
    # Trade details
    ticket = db.Column(db.String(100), unique=True)
    symbol = db.Column(db.String(20), nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # buy, sell
    
    # Volumes
    volume = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Prices
    open_price = db.Column(db.Numeric(15, 5), nullable=False)
    close_price = db.Column(db.Numeric(15, 5))
    stop_loss = db.Column(db.Numeric(15, 5))
    take_profit = db.Column(db.Numeric(15, 5))
    
    # P&L
    profit = db.Column(db.Numeric(15, 2))
    commission = db.Column(db.Numeric(10, 2), default=0)
    swap = db.Column(db.Numeric(10, 2), default=0)
    
    # Status
    status = db.Column(db.String(20), default='open')  # open, closed
    
    # Dates
    open_time = db.Column(db.DateTime, nullable=False)
    close_time = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'ticket': self.ticket,
            'symbol': self.symbol,
            'trade_type': self.trade_type,
            'volume': float(self.volume) if self.volume else None,
            'open_price': float(self.open_price) if self.open_price else None,
            'close_price': float(self.close_price) if self.close_price else None,
            'stop_loss': float(self.stop_loss) if self.stop_loss else None,
            'take_profit': float(self.take_profit) if self.take_profit else None,
            'profit': float(self.profit) if self.profit else None,
            'commission': float(self.commission) if self.commission else None,
            'swap': float(self.swap) if self.swap else None,
            'status': self.status,
            'open_time': self.open_time.isoformat() if self.open_time else None,
            'close_time': self.close_time.isoformat() if self.close_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

