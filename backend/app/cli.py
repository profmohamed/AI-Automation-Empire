"""
Command-line interface for AI Automation Empire
"""
import sys
import argparse
from loguru import logger


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI Automation Empire - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start API server
    api_parser = subparsers.add_parser("start-api", help="Start the API server")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    api_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    api_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    # Start Celery worker
    worker_parser = subparsers.add_parser("start-worker", help="Start Celery worker")
    worker_parser.add_argument("--concurrency", type=int, default=4, help="Number of worker processes")

    # Create admin user
    admin_parser = subparsers.add_parser("create-admin", help="Create admin user")
    admin_parser.add_argument("--email", required=True, help="Admin email")
    admin_parser.add_argument("--username", required=True, help="Admin username")
    admin_parser.add_argument("--password", required=True, help="Admin password")

    # Database migration
    db_parser = subparsers.add_parser("db", help="Database commands")
    db_subparsers = db_parser.add_subparsers(dest="db_command")
    db_subparsers.add_parser("init", help="Initialize database")
    db_subparsers.add_parser("migrate", help="Run migrations")
    db_subparsers.add_parser("upgrade", help="Upgrade database")

    # Version
    subparsers.add_parser("version", help="Show version")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Handle commands
    if args.command == "start-api":
        start_api(args.host, args.port, args.reload)
    elif args.command == "start-worker":
        start_worker(args.concurrency)
    elif args.command == "create-admin":
        create_admin(args.email, args.username, args.password)
    elif args.command == "db":
        handle_db_command(args.db_command)
    elif args.command == "version":
        show_version()


def start_api(host: str, port: int, reload: bool):
    """Start the API server"""
    import uvicorn
    from app.main import app

    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
    )


def start_worker(concurrency: int):
    """Start Celery worker"""
    import subprocess

    logger.info(f"Starting Celery worker with concurrency={concurrency}")
    subprocess.run([
        "celery", "-A", "app.workers.celery_app", "worker",
        "--loglevel=info",
        f"--concurrency={concurrency}",
    ])


def create_admin(email: str, username: str, password: str):
    """Create admin user"""
    from app.db.base import SessionLocal
    from app.models.user import User, UserRole
    from app.core.security import get_password_hash

    db = SessionLocal()

    try:
        # Check if user exists
        existing = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing:
            logger.error(f"User with email {email} or username {username} already exists")
            sys.exit(1)

        # Create admin user
        admin = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )

        db.add(admin)
        db.commit()

        logger.success(f"Admin user created: {email}")

    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        sys.exit(1)
    finally:
        db.close()


def handle_db_command(command: str):
    """Handle database commands"""
    import subprocess

    if command == "init":
        logger.info("Initializing database...")
        from app.db.base import Base, engine
        Base.metadata.create_all(bind=engine)
        logger.success("Database initialized")

    elif command == "migrate":
        logger.info("Creating migration...")
        subprocess.run(["alembic", "revision", "--autogenerate"])

    elif command == "upgrade":
        logger.info("Upgrading database...")
        subprocess.run(["alembic", "upgrade", "head"])
        logger.success("Database upgraded")


def show_version():
    """Show version information"""
    print("AI Automation Empire v1.0.0")
    print("The Ultimate Web Scraping & Automation Platform")
    print("https://github.com/profmohamed/AI-Automation-Empire")


if __name__ == "__main__":
    main()
