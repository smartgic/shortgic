"""Utility functions for common operations.

This module contains reusable helper functions for validation, error handling,
and common operations used across the application.
"""

from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import crud, models
from .config import settings


def validate_link_format(link: str) -> None:
    """Validate short link format.

    Checks if the provided link matches the expected format (correct length
    and alphanumeric characters only).

    Args:
        link: The short link identifier to validate.

    Raises:
        HTTPException: 400 if the link format is invalid.
    """
    if len(link) != settings.link_length or not link.isalnum():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_link_format",
                "message": f"Link must be exactly {settings.link_length} alphanumeric characters",
            },
        )


def get_link_or_404(db: Session, link: str) -> models.Link:
    """Get a link from database or raise 404 if not found.

    Combines link validation and database lookup with proper error handling.
    This consolidates the common pattern used across multiple endpoints.

    Args:
        db: Database session for executing the query.
        link: The short link identifier to retrieve.

    Returns:
        models.Link: The link record from the database.

    Raises:
        HTTPException: 400 if the link format is invalid.
        HTTPException: 404 if the link does not exist in the database.
    """
    validate_link_format(link)

    db_link = crud.get_link(db, link=link)
    if db_link is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "link_not_found",
                "message": "The requested short link does not exist",
            },
        )
    return db_link


def create_error_detail(error_type: str, message: str, **kwargs) -> dict:
    """Create standardized error detail dictionary.

    Provides consistent error formatting across all endpoints.

    Args:
        error_type: Machine-readable error type identifier.
        message: Human-readable error message.
        **kwargs: Additional error details to include.

    Returns:
        dict: Formatted error detail dictionary.
    """
    detail = {"error": error_type, "message": message}
    detail.update(kwargs)
    return detail
