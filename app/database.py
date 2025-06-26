"""Database configuration and session management.

This module handles SQLAlchemy database setup, connection management,
and ensures database file creation. Provides the database engine,
session factory, and base model class for the application.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def ensure_database_exists(database_path: str) -> None:
    """Ensure the database file and its parent directory exist.

    Creates the database file and any necessary parent directories if they
    don't already exist. This prevents SQLAlchemy operational errors when
    the database file is missing.

    Args:
        database_path: Path to the SQLite database file to create.

    Returns:
        None: Function performs file system operations only.
    """
    db_path = Path(database_path)

    # Create parent directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create empty database file if it doesn't exist
    if not db_path.exists():
        db_path.touch()


# Import configuration
from .config import settings

# Path to the SQLite3 database
database_path = settings.database_path
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

# Ensure database file exists before creating engine
ensure_database_exists(database_path)

engine = create_engine(
    # Required with SQLite3 because it's not multi-threaded
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
