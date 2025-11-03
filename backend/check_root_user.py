#!/usr/bin/env python3
"""
Check who is the Root Super Admin
"""
import sys
sys.path.insert(0, '/var/www/MarketEdgePros/backend')

from src.database import db
from src.models.user import User
from src.app import create_app

def check_root():
    """Check who is Root"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("ROOT SUPER ADMIN CHECK")
        print("=" * 70)
        
        # Find all Super Admins
        super_admins = User.query.filter_by(role='super_admin').all()
        
        print(f"\nTotal Super Admins: {len(super_admins)}\n")
        
        for user in super_admins:
            is_root = "✅ ROOT" if user.can_create_same_role else "Regular"
            print(f"{is_root}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.first_name} {user.last_name}")
            print(f"  ID: {user.id}")
            print(f"  can_create_same_role: {user.can_create_same_role}")
            print(f"  Created: {user.created_at}")
            print("-" * 70)

if __name__ == '__main__':
    check_root()

