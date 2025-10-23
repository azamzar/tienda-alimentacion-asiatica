"""
Script to create an admin user in the database
Run this script to create the first admin user or additional admin users
"""
import sys
from pathlib import Path
from getpass import getpass

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parents[1]))

from app.config.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository


def create_admin_user():
    """
    Interactive script to create an admin user
    """
    print("=" * 60)
    print("CREATE ADMIN USER")
    print("=" * 60)
    print()

    db = SessionLocal()
    user_repo = UserRepository(db)

    try:
        # Get user input
        print("Enter admin user details:")
        print("-" * 60)

        email = input("Email: ").strip()
        if not email:
            print("Error: Email is required")
            return

        # Check if user already exists
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            print(f"\nError: User with email '{email}' already exists!")
            print(f"Role: {existing_user.role.value}")
            print(f"Active: {existing_user.is_active}")
            return

        full_name = input("Full Name (optional): ").strip() or None

        # Get password with confirmation
        password = getpass("Password (min 8 characters): ")
        if len(password) < 8:
            print("Error: Password must be at least 8 characters long")
            return

        password_confirm = getpass("Confirm Password: ")
        if password != password_confirm:
            print("Error: Passwords do not match")
            return

        print()
        print("-" * 60)
        print("Creating admin user...")

        # Create admin user
        hashed_password = get_password_hash(password)
        admin_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=UserRole.ADMIN,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print()
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"Admin user created successfully!")
        print(f"  ID: {admin_user.id}")
        print(f"  Email: {admin_user.email}")
        print(f"  Full Name: {admin_user.full_name or 'N/A'}")
        print(f"  Role: {admin_user.role.value}")
        print(f"  Active: {admin_user.is_active}")
        print(f"  Created: {admin_user.created_at}")
        print()
        print("You can now login with these credentials.")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        db.rollback()
    except Exception as e:
        print(f"\nError creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_admin_user_noninteractive(email: str, password: str, full_name: str = None):
    """
    Non-interactive function to create an admin user (useful for automation)

    Args:
        email: Admin email
        password: Admin password (plain text, will be hashed)
        full_name: Optional full name

    Returns:
        User object if successful, None if failed
    """
    db = SessionLocal()
    user_repo = UserRepository(db)

    try:
        # Check if user already exists
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            print(f"Error: User with email '{email}' already exists!")
            return None

        # Validate password length
        if len(password) < 8:
            print("Error: Password must be at least 8 characters long")
            return None

        # Create admin user
        hashed_password = get_password_hash(password)
        admin_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=UserRole.ADMIN,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"Admin user '{email}' created successfully!")
        return admin_user

    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    # Check if running in non-interactive mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage:")
            print("  Interactive mode:  python create_admin.py")
            print("  Non-interactive:   python create_admin.py <email> <password> [full_name]")
            print()
            print("Examples:")
            print("  python create_admin.py")
            print("  python create_admin.py admin@example.com MySecurePass123 'Admin User'")
            sys.exit(0)

        # Non-interactive mode
        if len(sys.argv) < 3:
            print("Error: Email and password are required in non-interactive mode")
            print("Usage: python create_admin.py <email> <password> [full_name]")
            sys.exit(1)

        email = sys.argv[1]
        password = sys.argv[2]
        full_name = sys.argv[3] if len(sys.argv) > 3 else None

        create_admin_user_noninteractive(email, password, full_name)
    else:
        # Interactive mode
        create_admin_user()
