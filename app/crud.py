"""Database CRUD operations for the ShortGic URL shortener.

This module contains all database operations including creating, reading,
updating, and deleting short links. All functions include proper error
handling and use cryptographically secure random generation.
"""

import secrets
import string
from typing import Optional, Union

from fastapi import HTTPException
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from . import models, schemas
from .config import settings


def get_link(db: Session, link: str) -> Optional[models.Link]:
    """Retrieve a short link record by its identifier.

    Searches the database for a link record matching the provided short link identifier.

    Args:
        db: Database session for executing the query.
        link: The short link identifier to search for.

    Returns:
        Optional[models.Link]: The link record if found, None otherwise.
    """
    return db.query(models.Link).filter(models.Link.link == link).first()


def get_link_by_target(
    db: Session, target: Union[str, HttpUrl]
) -> Optional[models.Link]:
    """Retrieve a short link record by its target URL.

    Searches the database for a link record with the specified target URL.
    Useful for preventing duplicate URLs from being shortened.

    Args:
        db: Database session for executing the query.
        target: The target URL to search for (string or HttpUrl).

    Returns:
        Optional[models.Link]: The link record if found, None otherwise.
    """
    # Convert HttpUrl to string if needed
    target_str = str(target) if hasattr(target, "__str__") else target
    return db.query(models.Link).filter(models.Link.target == target_str).first()


def generate_unique_link(db: Session) -> str:
    """Generate a unique short link identifier.

    Generates cryptographically secure random identifiers and ensures uniqueness
    by checking against existing links in the database. Uses efficient EXISTS
    query for better performance. Retries up to 10 times to handle collisions.

    Args:
        db: Database session for checking uniqueness.

    Returns:
        str: A unique short link identifier.

    Raises:
        HTTPException: 500 if unable to generate unique link after 10 attempts.
    """
    chars = string.ascii_letters + string.digits
    max_attempts = 10

    for _ in range(max_attempts):
        shortened = "".join(
            secrets.choice(chars) for _ in range(settings.link_length)
        ).upper()
        # Use EXISTS query for better performance
        exists = (
            db.query(models.Link.id)
            .filter(models.Link.link == shortened)
            .first()
            is not None
        )
        if not exists:
            return shortened

    raise HTTPException(status_code=500, detail="Unable to generate unique link")


def create_link(db: Session, link: schemas.Link) -> models.Link:
    """Create a new short link record in the database.

    Generates a cryptographically secure unique identifier and stores the link
    information in the database. Ensures link uniqueness and handles collisions.

    Args:
        db: Database session for executing the transaction.
        link: Link schema containing target URL and optional extras.

    Returns:
        models.Link: The newly created link record with generated identifier.

    Raises:
        HTTPException: 500 if database transaction fails or unique link generation fails.
    """
    # Generate unique short link identifier
    shortened = generate_unique_link(db)

    # Convert HttpUrl to string for database storage
    target_str = str(link.target)

    try:
        db_link = models.Link(link=shortened, target=target_str, extras=link.extras)
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        return db_link
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create link")


def delete_link(db: Session, link: str) -> Optional[models.Link]:
    """Delete a short link record from the database.

    Removes the specified link record from the database permanently.
    This operation cannot be undone.

    Args:
        db: Database session for executing the transaction.
        link: The short link identifier to delete.

    Returns:
        Optional[models.Link]: The deleted link record if it existed, None if not found.

    Raises:
        HTTPException: 500 if database transaction fails, with automatic rollback.
    """
    db_link = db.query(models.Link).filter(models.Link.link == link).first()
    if not db_link:
        return None

    try:
        db.delete(db_link)
        db.commit()
        return db_link
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete link")
