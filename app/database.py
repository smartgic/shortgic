"""SQLAlchemy database URL and engine
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to the SQLite3 database
database_path = os.getenv("SHORTGIC_DB_PATH", "./shortgic.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

engine = create_engine(
    # Required with SQLite3 because it's not multi-threaded
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
