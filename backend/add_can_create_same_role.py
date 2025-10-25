#!/usr/bin/env python3
"""
Migration script to add can_create_same_role column to users table
and set it to True for root supermasters only
"""

from src.app import create_app
from src.database import db
from sqlalchemy import text

def migrate():
    app = create_app()
    
    with app.app_context():
        print("🔧 Adding can_create_same_role column to users table...")
        
        # Add column with default False
        try:
            db.session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN can_create_same_role BOOLEAN NOT NULL DEFAULT FALSE
            """))
            db.session.commit()
            print("✅ Column added successfully!")
        except Exception as e:
            if "already exists" in str(e) or "Duplicate column" in str(e):
                print("⚠️  Column already exists, skipping...")
                db.session.rollback()
            else:
                print(f"❌ Error adding column: {e}")
                db.session.rollback()
                return False
        
        # Set can_create_same_role = True for root supermasters
        # (supermasters with no parent_id)
        print("\n🔧 Setting can_create_same_role=True for root supermasters...")
        result = db.session.execute(text("""
            UPDATE users 
            SET can_create_same_role = TRUE 
            WHERE role = 'supermaster' 
            AND (parent_id IS NULL OR level = 0)
        """))
        db.session.commit()
        
        print(f"✅ Updated {result.rowcount} root supermaster(s)")
        
        # Show current state
        print("\n📊 Current users with can_create_same_role=True:")
        result = db.session.execute(text("""
            SELECT id, email, role, can_create_same_role, level, parent_id
            FROM users 
            WHERE can_create_same_role = TRUE
            ORDER BY id
        """))
        
        for row in result:
            print(f"  - {row.email} ({row.role}) - level={row.level}, parent_id={row.parent_id}")
        
        print("\n✅ Migration completed successfully!")
        return True

if __name__ == '__main__':
    migrate()

