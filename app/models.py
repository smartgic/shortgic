"""SQLAlchemy models
"""
from sqlalchemy import Column, String, Text, Integer, JSON
from .database import Base


class Link(Base):
    """SQLAlchemy definition for links table"""

    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    link = Column(String(20), unique=True, index=True, nullable=False)
    target = Column(Text, index=True, nullable=False)
    extras = Column(JSON, nullable=True)
