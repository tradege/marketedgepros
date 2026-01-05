"""
Lead model for CRM system
"""
from src.database import db, TimestampMixin
from datetime import datetime


class Lead(db.Model, TimestampMixin):
    """Lead model for CRM"""
    
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Contact Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(20))
    country_code = db.Column(db.String(2))
    
    # Lead Details
    status = db.Column(db.String(20), default='new', nullable=False, index=True)
    # Status: new, contacted, qualified, negotiating, converted, lost
    
    source = db.Column(db.String(50), default='website', index=True)
    # Source: website, referral, agent, social_media, paid_ads, organic, other
    
    score = db.Column(db.Integer, default=0)  # Lead score 0-100
    
    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    assigned_at = db.Column(db.DateTime)
    
    # Interest
    interested_program_id = db.Column(db.Integer, db.ForeignKey('trading_programs.id'))
    budget = db.Column(db.Numeric(10, 2))  # Expected budget
    
    # Conversion
    converted_to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    converted_at = db.Column(db.DateTime)
    
    # Lost Reason
    lost_reason = db.Column(db.String(50))
    # Reasons: no_budget, no_response, not_interested, competitor, other
    lost_notes = db.Column(db.Text)
    lost_at = db.Column(db.DateTime)
    
    # Additional Info
    company = db.Column(db.String(200))
    job_title = db.Column(db.String(100))
    notes = db.Column(db.Text)
    tags = db.Column(db.String(500))  # Comma-separated tags
    
    # Tracking
    last_contacted_at = db.Column(db.DateTime)
    next_follow_up = db.Column(db.DateTime, index=True)
    
    # Relationships
    assigned_user = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_leads')
    converted_user = db.relationship('User', foreign_keys=[converted_to_user_id], backref='converted_from_lead')
    interested_program = db.relationship('TradingProgram', backref='interested_leads')
    activities = db.relationship('LeadActivity', back_populates='lead', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lead {self.first_name} {self.last_name} - {self.status}>'
    
    def calculate_score(self):
        """Calculate lead score based on various factors"""
        score = 0
        
        # Email provided
        if self.email:
            score += 10
        
        # Phone provided
        if self.phone:
            score += 10
        
        # Budget specified
        if self.budget and self.budget > 0:
            score += 20
        
        # Interested in specific program
        if self.interested_program_id:
            score += 15
        
        # Has been contacted
        if self.last_contacted_at:
            score += 10
        
        # Recent activity (within 7 days)
        if self.last_contacted_at:
            days_since_contact = (datetime.utcnow() - self.last_contacted_at).days
            if days_since_contact <= 7:
                score += 20
            elif days_since_contact <= 30:
                score += 10
        
        # Has company info
        if self.company:
            score += 5
        
        # Qualified status
        if self.status == 'qualified':
            score += 10
        
        self.score = min(score, 100)  # Cap at 100
        return self.score
    
    def convert_to_user(self, user_id):
        """Mark lead as converted"""
        self.status = 'converted'
        self.converted_to_user_id = user_id
        self.converted_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_lost(self, reason, notes=None):
        """Mark lead as lost"""
        self.status = 'lost'
        self.lost_reason = reason
        self.lost_notes = notes
        self.lost_at = datetime.utcnow()
        db.session.commit()
    
    def assign_to(self, user_id):
        """Assign lead to a user"""
        self.assigned_to = user_id
        self.assigned_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert lead to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'country_code': self.country_code,
            'status': self.status,
            'source': self.source,
            'score': self.score,
            'assigned_to': self.assigned_to,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'interested_program_id': self.interested_program_id,
            'budget': float(self.budget) if self.budget else None,
            'company': self.company,
            'job_title': self.job_title,
            'notes': self.notes,
            'tags': self.tags.split(',') if self.tags else [],
            'last_contacted_at': self.last_contacted_at.isoformat() if self.last_contacted_at else None,
            'next_follow_up': self.next_follow_up.isoformat() if self.next_follow_up else None,
            'converted_at': self.converted_at.isoformat() if self.converted_at else None,
            'lost_reason': self.lost_reason,
            'lost_at': self.lost_at.isoformat() if self.lost_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LeadActivity(db.Model, TimestampMixin):
    """Activity log for leads"""
    
    __tablename__ = 'lead_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Activity Type
    activity_type = db.Column(db.String(50), nullable=False, index=True)
    # Types: call, email, meeting, note, status_change, assignment, other
    
    # Activity Details
    subject = db.Column(db.String(200))
    description = db.Column(db.Text)
    outcome = db.Column(db.String(50))  # success, no_answer, callback, other
    
    # Scheduled Activity
    scheduled_at = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    lead = db.relationship('Lead', back_populates='activities')
    user = db.relationship('User', backref='lead_activities')
    
    def __repr__(self):
        return f'<LeadActivity {self.activity_type} for Lead {self.lead_id}>'
    
    def mark_completed(self):
        """Mark activity as completed"""
        self.completed = True
        self.completed_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert activity to dictionary"""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'subject': self.subject,
            'description': self.description,
            'outcome': self.outcome,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LeadNote(db.Model, TimestampMixin):
    """Notes for leads"""
    
    __tablename__ = 'lead_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    is_important = db.Column(db.Boolean, default=False)
    
    # Relationships
    lead = db.relationship('Lead', backref='lead_notes')
    user = db.relationship('User', backref='created_lead_notes')
    
    def __repr__(self):
        return f'<LeadNote for Lead {self.lead_id}>'
    
    def to_dict(self):
        """Convert note to dictionary"""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'user_id': self.user_id,
            'content': self.content,
            'is_important': self.is_important,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user': {
                'id': self.user.id,
                'name': f"{self.user.first_name} {self.user.last_name}"
            } if self.user else None
        }

