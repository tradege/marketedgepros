"""
Monitoring Database Models
Tables for tracking monitoring events and violations
"""

from src.database import db, TimestampMixin
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime


class MonitoringEvent(db.Model, TimestampMixin):
    """Track all monitoring events"""
    
    __tablename__ = 'monitoring_events'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    
    # Event details
    event_type = db.Column(db.String(50), nullable=False)  # 'sync', 'violation', 'disable', 'warning'
    event_data = db.Column(JSONB, default={})
    
    # Metadata
    severity = db.Column(db.String(20), default='info')  # 'info', 'warning', 'critical'
    
    # Relationships
    challenge = db.relationship('Challenge', backref='monitoring_events')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_monitoring_events_challenge', 'challenge_id'),
        db.Index('idx_monitoring_events_type', 'event_type'),
        db.Index('idx_monitoring_events_created', 'created_at'),
        db.Index('idx_monitoring_events_severity', 'severity'),
    )
    
    def __repr__(self):
        return f'<MonitoringEvent {self.id} - {self.event_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'severity': self.severity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ViolationLog(db.Model, TimestampMixin):
    """Track all rule violations"""
    
    __tablename__ = 'violation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    
    # Violation details
    violation_type = db.Column(db.String(50), nullable=False)  # 'daily_loss', 'max_loss', 'profit_target'
    violation_data = db.Column(JSONB, default={})
    
    # Actions taken
    action_taken = db.Column(db.String(50))  # 'account_disabled', 'notification_sent', 'manual_review'
    action_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Resolution
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolution_notes = db.Column(db.Text)
    
    # Relationships
    challenge = db.relationship('Challenge', backref='violation_logs')
    resolver = db.relationship('User', foreign_keys=[resolved_by])
    
    # Indexes
    __table_args__ = (
        db.Index('idx_violation_logs_challenge', 'challenge_id'),
        db.Index('idx_violation_logs_type', 'violation_type'),
        db.Index('idx_violation_logs_created', 'created_at'),
        db.Index('idx_violation_logs_resolved', 'resolved'),
    )
    
    def __repr__(self):
        return f'<ViolationLog {self.id} - {self.violation_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'violation_type': self.violation_type,
            'violation_data': self.violation_data,
            'action_taken': self.action_taken,
            'action_timestamp': self.action_timestamp.isoformat() if self.action_timestamp else None,
            'resolved': self.resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MonitoringAlert(db.Model, TimestampMixin):
    """Track alerts sent to admins"""
    
    __tablename__ = 'monitoring_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    
    # Alert details
    alert_type = db.Column(db.String(50), nullable=False)  # 'approaching_limit', 'violation', 'system_error'
    alert_level = db.Column(db.String(20), nullable=False)  # 'info', 'warning', 'critical'
    alert_message = db.Column(db.Text)
    alert_data = db.Column(JSONB, default={})
    
    # Delivery
    channels = db.Column(JSONB, default=[])  # ['email', 'slack', 'sms']
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Acknowledgment
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    challenge = db.relationship('Challenge', backref='monitoring_alerts')
    acknowledger = db.relationship('User', foreign_keys=[acknowledged_by])
    
    # Indexes
    __table_args__ = (
        db.Index('idx_monitoring_alerts_challenge', 'challenge_id'),
        db.Index('idx_monitoring_alerts_level', 'alert_level'),
        db.Index('idx_monitoring_alerts_acknowledged', 'acknowledged'),
        db.Index('idx_monitoring_alerts_sent', 'sent_at'),
    )
    
    def __repr__(self):
        return f'<MonitoringAlert {self.id} - {self.alert_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'alert_type': self.alert_type,
            'alert_level': self.alert_level,
            'alert_message': self.alert_message,
            'alert_data': self.alert_data,
            'channels': self.channels,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'acknowledged': self.acknowledged,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'acknowledged_by': self.acknowledged_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Migration SQL
"""
-- Create monitoring_events table
CREATE TABLE monitoring_events (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB DEFAULT '{}',
    severity VARCHAR(20) DEFAULT 'info',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_monitoring_events_challenge ON monitoring_events(challenge_id);
CREATE INDEX idx_monitoring_events_type ON monitoring_events(event_type);
CREATE INDEX idx_monitoring_events_created ON monitoring_events(created_at);
CREATE INDEX idx_monitoring_events_severity ON monitoring_events(severity);

-- Create violation_logs table
CREATE TABLE violation_logs (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    violation_type VARCHAR(50) NOT NULL,
    violation_data JSONB DEFAULT '{}',
    action_taken VARCHAR(50),
    action_timestamp TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id),
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_violation_logs_challenge ON violation_logs(challenge_id);
CREATE INDEX idx_violation_logs_type ON violation_logs(violation_type);
CREATE INDEX idx_violation_logs_created ON violation_logs(created_at);
CREATE INDEX idx_violation_logs_resolved ON violation_logs(resolved);

-- Create monitoring_alerts table
CREATE TABLE monitoring_alerts (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    alert_level VARCHAR(20) NOT NULL,
    alert_message TEXT,
    alert_data JSONB DEFAULT '{}',
    channels JSONB DEFAULT '[]',
    sent_at TIMESTAMP DEFAULT NOW(),
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    acknowledged_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_monitoring_alerts_challenge ON monitoring_alerts(challenge_id);
CREATE INDEX idx_monitoring_alerts_level ON monitoring_alerts(alert_level);
CREATE INDEX idx_monitoring_alerts_acknowledged ON monitoring_alerts(acknowledged);
CREATE INDEX idx_monitoring_alerts_sent ON monitoring_alerts(sent_at);
"""
