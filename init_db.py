#!/usr/bin/env python
"""
Initialize the Athena database.
Run this script to create the database and apply migrations.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import init_db, engine
from database.models import User
from alembic.config import Config
from alembic import command

def initialize_database():
    """Initialize the database and run migrations."""
    print("Initializing Athena database...")
    
    # Create all tables
    init_db()
    
    # Run Alembic migrations
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Database migrations applied successfully!")
    except Exception as e:
        print(f"Note: Migrations setup but not critical for initial use: {e}")
    
    # Verify database is ready
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if 'users' in tables:
        print(f"Database ready with tables: {', '.join(tables)}")
        return True
    else:
        print("Error: Users table not created!")
        return False

if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)