"""
Role Model - Database-driven role management
"""
from datetime import datetime
from src.database import db


class Role(db.Model):
    """Role model for managing user roles and permissions"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # supermaster, admin, agent, trader
    label = db.Column(db.String(100), nullable=False)  # Super Master, Master, Agent, Trader
    label_he = db.Column(db.String(100))  # Hebrew label
    color = db.Column(db.String(100))  # Tailwind CSS classes
    icon = db.Column(db.String(10))  # Emoji or icon
    hierarchy = db.Column(db.Integer, nullable=False)  # 1=highest, 4=lowest
    
    # Permissions (JSON)
    permissions = db.Column(db.JSON, default={})
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert role to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'label_he': self.label_he,
            'color': self.color,
            'icon': self.icon,
            'hierarchy': self.hierarchy,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def seed_default_roles():
        """Seed default roles if they don't exist"""
        default_roles = [
            {
                'name': 'supermaster',
                'label': 'Super Master',
                'label_he': 'סופר מנהל',
                'color': 'bg-purple-100 text-purple-800',
                'icon': '👑',
                'hierarchy': 1,
                'permissions': {
                    'can_create_users': True,
                    'can_create_without_verification': True,
                    'can_manage_commissions': True,
                    'can_view_all_users': True,
                    'can_delete_users': True,
                    'can_manage_programs': True,
                    'can_manage_payments': True,
                    'can_manage_roles': True
                }
            },
            {
                'name': 'super_admin',
                'label': 'Super Admin',
                'label_he': 'מנהל על',
                'color': 'bg-purple-100 text-purple-800',
                'icon': '👑',
                'hierarchy': 1,
                'permissions': {
                    'can_create_users': True,
                    'can_create_without_verification': True,
                    'can_manage_commissions': True,
                    'can_view_all_users': True,
                    'can_delete_users': True,
                    'can_manage_programs': True,
                    'can_manage_payments': True,
                    'can_manage_roles': True
                }
            },
            {
                'name': 'admin',
                'label': 'Master',
                'label_he': 'מנהל',
                'color': 'bg-blue-100 text-blue-800',
                'icon': '⭐',
                'hierarchy': 2,
                'permissions': {
                    'can_create_users': True,
                    'can_create_without_verification': False,
                    'can_manage_commissions': False,
                    'can_view_all_users': False,
                    'can_delete_users': False,
                    'can_manage_programs': False,
                    'can_manage_payments': False,
                    'can_manage_roles': False
                }
            },
            {
                'name': 'agent',
                'label': 'Agent',
                'label_he': 'סוכן',
                'color': 'bg-green-100 text-green-800',
                'icon': '🤝',
                'hierarchy': 3,
                'permissions': {
                    'can_create_users': False,
                    'can_create_without_verification': False,
                    'can_manage_commissions': False,
                    'can_view_all_users': False,
                    'can_delete_users': False,
                    'can_manage_programs': False,
                    'can_manage_payments': False,
                    'can_manage_roles': False
                }
            },
            {
                'name': 'trader',
                'label': 'Trader',
                'label_he': 'משתמש',
                'color': 'bg-gray-100 text-gray-800',
                'icon': '📊',
                'hierarchy': 4,
                'permissions': {
                    'can_create_users': False,
                    'can_create_without_verification': False,
                    'can_manage_commissions': False,
                    'can_view_all_users': False,
                    'can_delete_users': False,
                    'can_manage_programs': False,
                    'can_manage_payments': False,
                    'can_manage_roles': False
                }
            }
        ]
        
        for role_data in default_roles:
            existing_role = Role.query.filter_by(name=role_data['name']).first()
            if not existing_role:
                role = Role(**role_data)
                db.session.add(role)
        
        db.session.commit()

