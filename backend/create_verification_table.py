#!/usr/bin/env python3
"""
Create verification_attempts table
"""
import sys
sys.path.insert(0, '/home/ubuntu/MarketEdgePros/backend')

from src.app import create_app
from src.database import db
from src.models.verification_attempt import VerificationAttempt

app = create_app()

with app.app_context():
    # Create table
    db.create_all()
    print("✅ verification_attempts table created successfully!")
    
    # Verify table exists
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'verification_attempts' in tables:
        print("✅ Table verified in database")
        
        # Show columns
        columns = inspector.get_columns('verification_attempts')
        print("\nTable columns:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
    else:
        print("❌ Table not found!")

