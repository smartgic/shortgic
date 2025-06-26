"""SQLAlchemy database models for the ShortGic URL shortener.

This module defines the database schema and ORM models used for storing
short link data. All models inherit from the declarative base and include
proper indexing for optimal query performance.
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Index
from .database import Base


class Link(Base):
    """SQLAlchemy model for the links table.

    Represents a short link record in the database, storing the relationship
    between short link identifiers and their target URLs, along with optional
    metadata. Includes optimized indexes for fast lookups.

    Attributes:
        id: Primary key auto-increment integer.
        link: Unique short link identifier (indexed for fast lookups).
        target: The target URL that the short link redirects to (indexed).
        extras: Optional JSON field for additional metadata or tracking data.
    """

    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    link = Column(String(20), unique=True, index=True, nullable=False)
    target = Column(Text, index=True, nullable=False)
    extras = Column(JSON, nullable=True)

    # Composite index for efficient duplicate checking
    __table_args__ = (
        Index('ix_target_hash', 'target'),  # Optimized target lookup
    )
