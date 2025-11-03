#!/usr/bin/env python3
"""
Professional Role Restructuring Migration
Synchronizes role hierarchy across the entire system
"""
import sys
sys.path.insert(0, '/var/www/MarketEdgePros/backend')

from src.database import db
from src.models.role import Role
from src.models.user import User
from src.app import create_app

def restructure_roles():
    """
    Restructure roles to professional hierarchy:
    1. super_admin (Super Admin) - hierarchy 1
    2. admin (Admin) - hierarchy 2
    3. master (Master) - hierarchy 3
    4. affiliate (Affiliate) - hierarchy 4
    5. trader (Trader) - hierarchy 5
    """
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("PROFESSIONAL ROLE RESTRUCTURING MIGRATION")
        print("=" * 70)
        
        # Step 1: Rename current 'admin' (which is actually Master) to 'master'
        print("\n[STEP 1] Renaming 'admin' role to 'master'...")
        current_admin = Role.query.filter_by(name='admin').first()
        if current_admin:
            print(f"  Found: {current_admin.name} ({current_admin.label})")
            # Update users first
            users_updated = User.query.filter_by(role='admin').update({'role': 'master'})
            print(f"  Updated {users_updated} users from 'admin' to 'master'")
            # Update role
            current_admin.name = 'master'
            current_admin.label = 'Master'
            current_admin.hierarchy = 3
            print(f"  ✅ Role renamed: admin → master (hierarchy 3)")
        else:
            print("  ⚠️  No 'admin' role found")
        
        db.session.commit()
        
        # Step 2: Check if 'supermaster' exists and handle it
        print("\n[STEP 2] Handling 'supermaster' role...")
        supermaster = Role.query.filter_by(name='supermaster').first()
        if supermaster:
            print(f"  Found: {supermaster.name} ({supermaster.label})")
            # Update all supermaster users to super_admin
            users_updated = User.query.filter_by(role='supermaster').update({'role': 'super_admin'})
            print(f"  Migrated {users_updated} users from 'supermaster' to 'super_admin'")
            # Delete supermaster role
            db.session.delete(supermaster)
            print(f"  ✅ Removed 'supermaster' role")
        else:
            print("  ℹ️  No 'supermaster' role found")
        
        db.session.commit()
        
        # Step 3: Create new 'admin' role (hierarchy 2)
        print("\n[STEP 3] Creating new 'admin' role...")
        existing_admin = Role.query.filter_by(name='admin').first()
        if not existing_admin:
            new_admin = Role(
                name='admin',
                label='Admin',
                label_he='אדמין',
                color='bg-blue-100 text-blue-800',
                icon='⚡',
                hierarchy=2,
                permissions={
                    'can_create_users': True,
                    'can_create_without_verification': False,
                    'can_manage_commissions': False,
                    'can_view_all_users': False,
                    'can_delete_users': False,
                    'can_manage_programs': False,
                    'can_manage_payments': False,
                    'can_manage_roles': False
                }
            )
            db.session.add(new_admin)
            print(f"  ✅ Created 'admin' role (hierarchy 2)")
        else:
            print(f"  ℹ️  'admin' role already exists")
        
        db.session.commit()
        
        # Step 4: Update hierarchy for all roles
        print("\n[STEP 4] Updating hierarchy for all roles...")
        role_hierarchy = {
            'super_admin': 1,
            'admin': 2,
            'master': 3,
            'affiliate': 4,
            'trader': 5
        }
        
        for role_name, hierarchy in role_hierarchy.items():
            role = Role.query.filter_by(name=role_name).first()
            if role:
                old_hierarchy = role.hierarchy
                role.hierarchy = hierarchy
                print(f"  {role_name}: {old_hierarchy} → {hierarchy}")
        
        db.session.commit()
        print("  ✅ All hierarchies updated")
        
        # Step 5: Verify final state
        print("\n" + "=" * 70)
        print("FINAL ROLE STRUCTURE")
        print("=" * 70)
        
        all_roles = Role.query.order_by(Role.hierarchy).all()
        for role in all_roles:
            user_count = User.query.filter_by(role=role.name).count()
            print(f"\n{role.hierarchy}. {role.label} ({role.name})")
            print(f"   Users: {user_count}")
            print(f"   Color: {role.color}")
            print(f"   Icon: {role.icon}")
        
        print("\n" + "=" * 70)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        # Step 6: Show user distribution
        print("\nUSER DISTRIBUTION:")
        for role in all_roles:
            users = User.query.filter_by(role=role.name).all()
            if users:
                print(f"\n{role.label} ({role.name}):")
                for user in users:
                    print(f"  - {user.email}")

if __name__ == '__main__':
    try:
        restructure_roles()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

