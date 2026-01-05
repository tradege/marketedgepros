#!/usr/bin/env python3
"""
Migration script to update 'agent' role to 'affiliate' in the database
"""
import sys
sys.path.insert(0, '/var/www/MarketEdgePros/backend')

from src.database import db
from src.models.role import Role
from src.models.user import User
from src.app import create_app

def migrate_agent_to_affiliate():
    """Update agent role to affiliate"""
    app = create_app()
    
    with app.app_context():
        print("Starting migration: agent → affiliate")
        
        # 1. Update the role in roles table
        agent_role = Role.query.filter_by(name='agent').first()
        if agent_role:
            print(f"Found agent role (ID: {agent_role.id})")
            agent_role.name = 'affiliate'
            agent_role.label = 'Affiliate'
            agent_role.label_he = 'שותף'
            print("Updated role: agent → affiliate")
        else:
            print("No 'agent' role found in database")
            # Check if affiliate already exists
            affiliate_role = Role.query.filter_by(name='affiliate').first()
            if affiliate_role:
                print(f"'affiliate' role already exists (ID: {affiliate_role.id})")
            else:
                print("Creating new 'affiliate' role...")
                new_role = Role(
                    name='affiliate',
                    label='Affiliate',
                    label_he='שותף',
                    color='bg-green-100 text-green-800',
                    icon='🤝',
                    hierarchy=3,
                    permissions={
                        'can_create_users': False,
                        'can_create_without_verification': False,
                        'can_manage_commissions': False,
                        'can_view_all_users': False,
                        'can_delete_users': False,
                        'can_manage_programs': False,
                        'can_manage_payments': False,
                        'can_manage_roles': False
                    }
                )
                db.session.add(new_role)
                print("Created new 'affiliate' role")
        
        # 2. Update all users with role='agent' to role='affiliate'
        users_updated = User.query.filter_by(role='agent').update({'role': 'affiliate'})
        print(f"Updated {users_updated} users from 'agent' to 'affiliate'")
        
        # 3. Commit changes
        db.session.commit()
        print("✅ Migration completed successfully!")
        
        # 4. Verify
        print("\nVerification:")
        all_roles = Role.query.order_by(Role.hierarchy).all()
        for role in all_roles:
            user_count = User.query.filter_by(role=role.name).count()
            print(f"  - {role.name} ({role.label}): {user_count} users")

if __name__ == '__main__':
    migrate_agent_to_affiliate()

