"""Add Supermaster user

Revision ID: 003
Revises: 002
Create Date: 2025-10-23

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '003a'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    """Add Supermaster user to the database"""
    # Create a connection to execute raw SQL
    conn = op.get_bind()
    
    # Check if user already exists
    result = conn.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": "supermaster@marketedgepros.com"}
    )
    
    if result.fetchone() is None:
        # Hash the password
        hashed_password = generate_password_hash('9449')
        
        # Insert the new Supermaster user
        conn.execute(
            sa.text("""
                INSERT INTO users (
                    email, 
                    password_hash, 
                    first_name, 
                    last_name, 
                    role, 
                    is_verified, 
                    is_active,
                    created_at,
                    updated_at
                ) VALUES (
                    :email,
                    :password_hash,
                    :first_name,
                    :last_name,
                    :role,
                    :is_verified,
                    :is_active,
                    :created_at,
                    :updated_at
                )
            """),
            {
                "email": "supermaster@marketedgepros.com",
                "password_hash": hashed_password,
                "first_name": "Super",
                "last_name": "Master",
                "role": "supermaster",
                "is_verified": True,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        print("✅ Supermaster user created successfully!")
    else:
        print("ℹ️  Supermaster user already exists, skipping...")


def downgrade():
    """Remove Supermaster user from the database"""
    conn = op.get_bind()
    
    conn.execute(
        sa.text("DELETE FROM users WHERE email = :email"),
        {"email": "supermaster@marketedgepros.com"}
    )
    print("✅ Supermaster user removed successfully!")

