#!/usr/bin/env python3
"""
Database management script
"""
import sys
import os
from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade, downgrade, stamp
from src.database import db
from src.config import Config
from src.models import *  # Import all models

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Flask-Migrate
migrate_obj = Migrate(app, db)


def init_db():
    """Initialize database with migrations"""
    print("Initializing database migrations...")
    with app.app_context():
        init()
    print("✅ Migrations initialized!")


def create_migration(message="Auto-generated migration"):
    """Create a new migration"""
    print(f"Creating migration: {message}")
    with app.app_context():
        migrate(message=message)
    print("✅ Migration created!")


def apply_migrations():
    """Apply all pending migrations"""
    print("Applying migrations...")
    with app.app_context():
        upgrade()
    print("✅ Migrations applied!")


def rollback_migration():
    """Rollback last migration"""
    print("Rolling back last migration...")
    with app.app_context():
        downgrade()
    print("✅ Migration rolled back!")


def reset_db():
    """Reset database (drop all tables and recreate)"""
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Are you sure? Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("❌ Aborted!")
        return
    
    print("Dropping all tables...")
    with app.app_context():
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
    print("✅ Database reset complete!")


def seed_db():
    """Seed database with initial data"""
    print("Seeding database...")
    with app.app_context():
        # Import seed function
        from migrations.versions.seed_002 import upgrade as seed_upgrade
        seed_upgrade()
    print("✅ Database seeded!")


def show_help():
    """Show help message"""
    print("""
Database Management Commands:

  init          Initialize migrations
  migrate       Create a new migration
  upgrade       Apply all pending migrations
  downgrade     Rollback last migration
  reset         Reset database (drop all and recreate)
  seed          Seed database with initial data
  help          Show this help message

Examples:
  python manage.py init
  python manage.py migrate "Add user table"
  python manage.py upgrade
  python manage.py downgrade
  python manage.py reset
  python manage.py seed
""")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_db()
    elif command == 'migrate':
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto-generated migration"
        create_migration(message)
    elif command == 'upgrade':
        apply_migrations()
    elif command == 'downgrade':
        rollback_migration()
    elif command == 'reset':
        reset_db()
    elif command == 'seed':
        seed_db()
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)

