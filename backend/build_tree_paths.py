#!/usr/bin/env python3
"""
Migration script to build tree_path for all existing users.

This script:
1. Finds all supermasters and assigns them root tree_paths (1, 2, 3...)
2. Assigns all other users under the first supermaster
3. Updates level and tree_path for all users

Run this ONCE after deploying the hierarchy scoping system.
"""

from src.app import create_app
from src.models.user import User
from src.database import db

def build_tree_paths():
    """Build tree_path for all users"""
    
    app = create_app()
    with app.app_context():
        print("🔧 Building tree_path for all users...")
        print("=" * 60)
        
        # Get all users
        all_users = User.query.all()
        print(f"📊 Found {len(all_users)} users")
        
        # Find supermasters
        supermasters = [u for u in all_users if u.role == 'supermaster']
        other_users = [u for u in all_users if u.role != 'supermaster']
        
        print(f"👑 Supermasters: {len(supermasters)}")
        print(f"👥 Other users: {len(other_users)}")
        print()
        
        # Assign tree_path to supermasters
        for idx, sm in enumerate(supermasters, start=1):
            sm.tree_path = str(idx)
            sm.level = 0
            sm.parent_id = None
            print(f"✅ {sm.email} (supermaster) -> tree_path={sm.tree_path}, level={sm.level}")
        
        # Commit supermasters first
        db.session.commit()
        print()
        
        # Assign other users under first supermaster
        if supermasters and other_users:
            first_supermaster = supermasters[0]
            print(f"📌 Assigning other users under: {first_supermaster.email}")
            print()
            
            for idx, user in enumerate(other_users, start=1):
                user.parent_id = first_supermaster.id
                user.level = 1
                user.tree_path = f"{first_supermaster.tree_path}.{idx}"
                print(f"✅ {user.email} ({user.role}) -> tree_path={user.tree_path}, level={user.level}, parent={first_supermaster.email}")
            
            db.session.commit()
        
        print()
        print("=" * 60)
        print("✅ Tree paths built successfully!")
        print()
        
        # Verify
        print("📋 Final hierarchy:")
        print("-" * 60)
        all_users = User.query.order_by(User.tree_path).all()
        for u in all_users:
            parent = User.query.get(u.parent_id) if u.parent_id else None
            parent_email = parent.email if parent else "None"
            print(f"  {u.email:30s} | tree_path={u.tree_path:10s} | level={u.level} | parent={parent_email}")
        print("=" * 60)

if __name__ == "__main__":
    build_tree_paths()

