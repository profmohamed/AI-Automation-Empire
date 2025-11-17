#!/usr/bin/env python3
"""
Create admin user script
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash


def create_admin(email: str, username: str, password: str, full_name: str = None):
    """Create admin user"""
    db = SessionLocal()

    try:
        # Check if admin exists
        existing = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing:
            print(f"❌ User with email {email} or username {username} already exists")
            return False

        # Create admin user
        admin = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            full_name=full_name or "Admin User",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(f"✅ Admin user created successfully!")
        print(f"   Email: {email}")
        print(f"   Username: {username}")
        print(f"   Role: {admin.role}")

        return True

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False

    finally:
        db.close()


if __name__ == "__main__":
    import getpass

    print("🔧 Admin User Creation")
    print("=" * 50)

    email = input("Email: ")
    username = input("Username: ")
    full_name = input("Full Name (optional): ")
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirm Password: ")

    if password != password_confirm:
        print("❌ Passwords don't match!")
        sys.exit(1)

    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        sys.exit(1)

    create_admin(email, username, password, full_name or None)
