"""
Tenant model for White Label multi-tenancy support
"""
from src.database import db, TimestampMixin
from sqlalchemy.dialects.postgresql import JSONB


class Tenant(db.Model, TimestampMixin):
    """Tenant model for White Label system"""
    
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=False, index=True)
    custom_domain = db.Column(db.String(255), unique=True)
    
    # Status
    status = db.Column(db.String(20), default='active', nullable=False)  # active, suspended, inactive
    tier = db.Column(db.String(20), default='basic', nullable=False)  # basic, pro, enterprise
    
    # Parent-Child hierarchy for unlimited sub-tenants
    parent_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=True)
    
    # Branding
    logo_url = db.Column(db.String(500))
    favicon_url = db.Column(db.String(500))
    primary_color = db.Column(db.String(7), default='#1a1a1a')
    secondary_color = db.Column(db.String(7), default='#00ff88')
    accent_color = db.Column(db.String(7), default='#ff6b35')
    
    # Custom CSS
    custom_css = db.Column(db.Text)
    
    # Settings
    settings = db.Column(JSONB, default={})
    
    # Contact
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    
    # Relationships
    parent = db.relationship('Tenant', remote_side=[id], backref='children')
    users = db.relationship('User', back_populates='tenant', lazy='dynamic')
    programs = db.relationship("TradingProgram", back_populates="tenant", lazy="dynamic")

    # Add indexes for performance
    __table_args__ = (db.Index("ix_tenant_status", "status"),)
    
    def __repr__(self):
        return f'<Tenant {self.name}>'
    
    def get_full_hierarchy(self):
        """Get full parent hierarchy"""
        hierarchy = [self]
        current = self.parent
        while current:
            hierarchy.insert(0, current)
            current = current.parent
        return hierarchy
    
    def get_all_children(self, include_self=True):
        """Get all children recursively"""
        children = [self] if include_self else []
        for child in self.children:
            children.extend(child.get_all_children(include_self=True))
        return children
    
    def to_dict(self):
        """Convert tenant to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'subdomain': self.subdomain,
            'custom_domain': self.custom_domain,
            'status': self.status,
            'tier': self.tier,
            'parent_id': self.parent_id,
            'branding': {
                'logo_url': self.logo_url,
                'favicon_url': self.favicon_url,
                'primary_color': self.primary_color,
                'secondary_color': self.secondary_color,
                'accent_color': self.accent_color,
                'custom_css': self.custom_css
            },
            'settings': self.settings,
            'contact': {
                'email': self.contact_email,
                'phone': self.contact_phone
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

