#!/usr/bin/env python3
"""
Check current roles in database
"""
import sys
sys.path.insert(0, '/var/www/MarketEdgePros/backend')

from src.database import db
from src.models.role import Role
from src.models.user import User
from src.app import create_app

def check_roles():
    """Check all roles and their users"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("CURRENT ROLES IN DATABASE")
        print("=" * 60)
        
        all_roles = Role.query.order_by(Role.hierarchy).all()
        
        for role in all_roles:
            user_count = User.query.filter_by(role=role.name).count()
            print(f"\nID: {role.id}")
            print(f"Name: {role.name}")
            print(f"Label: {role.label}")
            print(f"Label (Hebrew): {role.label_he}")
            print(f"Hierarchy: {role.hierarchy}")
            print(f"Users: {user_count}")
            print(f"Active: {role.is_active}")
            print("-" * 60)
        
        print("\n" + "=" * 60)
        print("USERS BY ROLE")
        print("=" * 60)
        
        for role in all_roles:
            users = User.query.filter_by(role=role.name).all()
            if users:
                print(f"\n{role.label} ({role.name}):")
                for user in users:
                    print(f"  - {user.email} (ID: {user.id})")

if __name__ == '__main__':
    check_roles()

