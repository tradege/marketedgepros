"""
MT5 Integration Models for MarketEdgePros
"""
from src.database import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

class MT5Account(db.Model):
    """MT5 Trading Account Model"""
    __tablename__ = 'mt5_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    mt5_login = db.Column(db.String(50), unique=True, nullable=False)
    mt5_password_encrypted = db.Column(db.Text, nullable=False)
    mt5_group = db.Column(db.String(100))
    mt5_server = db.Column(db.String(100), default='185.56.137.162:443')
    balance = db.Column(db.Numeric(15, 2), default=0)
    equity = db.Column(db.Numeric(15, 2), default=0)
    margin = db.Column(db.Numeric(15, 2), default=0)
    free_margin = db.Column(db.Numeric(15, 2), default=0)
    margin_level = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='mt5_accounts')
    challenge = db.relationship('Challenge', backref='mt5_account', uselist=False)
    trades = db.relationship('MT5Trade', backref='account', lazy='dynamic', cascade='all, delete-orphan')
    positions = db.relationship('MT5Position', backref='account', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def mt5_password(self):
        """Decrypt password when accessed"""
        try:
            cipher = Fernet(os.getenv('ENCRYPTION_KEY', 'default_key_change_this').encode())
            return cipher.decrypt(self.mt5_password_encrypted.encode()).decode()
        except:
            return None
    
    @mt5_password.setter
    def mt5_password(self, password):
        """Encrypt password when set"""
        cipher = Fernet(os.getenv('ENCRYPTION_KEY', 'default_key_change_this').encode())
        self.mt5_password_encrypted = cipher.encrypt(password.encode()).decode()
    
    def to_dict(self, include_password=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'mt5_login': self.mt5_login,
            'mt5_group': self.mt5_group,
            'mt5_server': self.mt5_server,
            'balance': float(self.balance) if self.balance else 0,
            'equity': float(self.equity) if self.equity else 0,
            'margin': float(self.margin) if self.margin else 0,
            'free_margin': float(self.free_margin) if self.free_margin else 0,
            'margin_level': float(self.margin_level) if self.margin_level else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_password:
            data['mt5_password'] = self.mt5_password
        return data


class MT5Trade(db.Model):
    """MT5 Trade History Model"""
    __tablename__ = 'mt5_trades'
    
    id = db.Column(db.Integer, primary_key=True)
    mt5_account_id = db.Column(db.Integer, db.ForeignKey('mt5_accounts.id'), nullable=False)
    ticket = db.Column(db.BigInteger, unique=True, nullable=False)
    symbol = db.Column(db.String(20))
    trade_type = db.Column(db.String(10))
    volume = db.Column(db.Numeric(10, 2))
    open_price = db.Column(db.Numeric(15, 5))
    close_price = db.Column(db.Numeric(15, 5))
    stop_loss = db.Column(db.Numeric(15, 5))
    take_profit = db.Column(db.Numeric(15, 5))
    open_time = db.Column(db.DateTime)
    close_time = db.Column(db.DateTime)
    profit = db.Column(db.Numeric(15, 2))
    commission = db.Column(db.Numeric(15, 2))
    swap = db.Column(db.Numeric(15, 2))
    comment = db.Column(db.Text)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'mt5_account_id': self.mt5_account_id,
            'ticket': self.ticket,
            'symbol': self.symbol,
            'trade_type': self.trade_type,
            'volume': float(self.volume) if self.volume else 0,
            'open_price': float(self.open_price) if self.open_price else 0,
            'close_price': float(self.close_price) if self.close_price else 0,
            'stop_loss': float(self.stop_loss) if self.stop_loss else 0,
            'take_profit': float(self.take_profit) if self.take_profit else 0,
            'open_time': self.open_time.isoformat() if self.open_time else None,
            'close_time': self.close_time.isoformat() if self.close_time else None,
            'profit': float(self.profit) if self.profit else 0,
            'commission': float(self.commission) if self.commission else 0,
            'swap': float(self.swap) if self.swap else 0,
            'comment': self.comment,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MT5Position(db.Model):
    """MT5 Open Position Model"""
    __tablename__ = 'mt5_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    mt5_account_id = db.Column(db.Integer, db.ForeignKey('mt5_accounts.id'), nullable=False)
    ticket = db.Column(db.BigInteger, unique=True, nullable=False)
    symbol = db.Column(db.String(20))
    position_type = db.Column(db.String(10))
    volume = db.Column(db.Numeric(10, 2))
    price_open = db.Column(db.Numeric(15, 5))
    price_current = db.Column(db.Numeric(15, 5))
    stop_loss = db.Column(db.Numeric(15, 5))
    take_profit = db.Column(db.Numeric(15, 5))
    profit = db.Column(db.Numeric(15, 2))
    swap = db.Column(db.Numeric(15, 2))
    commission = db.Column(db.Numeric(15, 2))
    open_time = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'mt5_account_id': self.mt5_account_id,
            'ticket': self.ticket,
            'symbol': self.symbol,
            'position_type': self.position_type,
            'volume': float(self.volume) if self.volume else 0,
            'price_open': float(self.price_open) if self.price_open else 0,
            'price_current': float(self.price_current) if self.price_current else 0,
            'stop_loss': float(self.stop_loss) if self.stop_loss else 0,
            'take_profit': float(self.take_profit) if self.take_profit else 0,
            'profit': float(self.profit) if self.profit else 0,
            'swap': float(self.swap) if self.swap else 0,
            'commission': float(self.commission) if self.commission else 0,
            'open_time': self.open_time.isoformat() if self.open_time else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
