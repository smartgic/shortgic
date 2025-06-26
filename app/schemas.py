"""Pydantic schemas for request/response validation.

This module defines all Pydantic models used for API request validation,
response serialization, and data transfer objects. Includes input validation
with configurable limits and standardized error response formats.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .config import settings


class Link(BaseModel):
    """Schema for link creation and information requests.

    Validates input for creating new short links, including URL validation
    and optional metadata. Enforces configurable URL length limits.

    Attributes:
        target: The target URL to be shortened (validated as proper URL).
        extras: Optional dictionary for additional metadata or tracking information.
    """

    target: HttpUrl = Field(
        ..., max_length=settings.max_url_length, description="Target URL to shorten"
    )
    extras: Optional[Dict[str, Any]] = Field(
        default={}, description="Additional metadata for the link"
    )

    # Pydantic V2 configuration
    model_config = ConfigDict(from_attributes=True)


class LinkResponse(BaseModel):
    """Schema for successful link creation responses.

    Returns the generated short link identifier after successful creation.

    Attributes:
        link: The generated short link identifier (alphanumeric string).
    """

    link: str = Field(..., description="Generated short link identifier")


class ErrorResponse(BaseModel):
    """Schema for standardized API error responses.

    Provides consistent error formatting across all API endpoints with
    structured error information for better client handling.

    Attributes:
        error: Machine-readable error type identifier.
        message: Human-readable error description.
        details: Optional additional error context or debugging information.
    """

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error details"
    )


class SuccessResponse(BaseModel):
    """Schema for standardized API success responses.

    Provides consistent success formatting for operations that don't return
    specific data but need to confirm successful completion.

    Attributes:
        success: Boolean indicating operation success (always True for this schema).
        message: Human-readable success confirmation message.
        data: Optional response data for operations that return additional information.
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
