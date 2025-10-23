#!/usr/bin/env python3
"""
Standalone script to add Supermaster user to the database
Run this on the server: python3 add_supermaster.py
"""

import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import create_app, db
from src.models.user import User
from werkzeug.security import generate_password_hash


def add_supermaster_user():
    """Add Supermaster user to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email='supermaster@marketedgepros.com').first()
        
        if existing_user:
            print("ℹ️  Supermaster user already exists!")
            print(f"   Email: {existing_user.email}")
            print(f"   Role: {existing_user.role}")
            print(f"   Active: {existing_user.is_active}")
            print(f"   Verified: {existing_user.is_verified}")
            return
        
        # Create new Supermaster user
        supermaster = User(
            email='supermaster@marketedgepros.com',
            password_hash=generate_password_hash('9449'),
            first_name='Super',
            last_name='Master',
            role='supermaster',
            is_verified=True,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        try:
            db.session.add(supermaster)
            db.session.commit()
            print("✅ Supermaster user created successfully!")
            print(f"   Email: {supermaster.email}")
            print(f"   Role: {supermaster.role}")
            print(f"   Password: 9449")
            print(f"   ID: {supermaster.id}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating Supermaster user: {e}")
            sys.exit(1)


if __name__ == '__main__':
    add_supermaster_user()

