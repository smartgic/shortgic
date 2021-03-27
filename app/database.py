"""SQLAlchemy database URL and engine
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to the SQLite3 database
SQLALCHEMY_DATABASE_URL = "sqlite:///./shortgic.db"

engine = create_engine(
    # Required with SQLite3 because it's not multi-threaded
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
