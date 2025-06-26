"""FastAPI application entrypoint.

This module contains the main FastAPI application with all API endpoints
for the ShortGic URL shortener service.
"""

from contextlib import asynccontextmanager
from typing import Annotated, Any, Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, schemas, utils
from .database import SessionLocal, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI application lifespan events.

    Handles startup and shutdown events for the application.
    On startup, creates the database schema.

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Control back to the application during its lifetime.
    """
    # Startup: Create the database schema
    create_tables()
    yield
    # Shutdown: Add cleanup logic here if needed


app = FastAPI(
    title="ShortGic URL Shortener",
    description=(
        "A minimalist and lightweight URL shortener using FastAPI and SQLAlchemy"
    ),
    version="1.0.0",
    contact={
        "name": "SmartGic",
        "url": "https://github.com/smartgic/shortgic",
    },
    lifespan=lifespan,
)


def get_db():
    """Create and manage database session dependency.

    Creates a new SQLAlchemy SessionLocal that will be used in a single request,
    and then closes it once the request is finished. This ensures proper
    database connection management and prevents connection leaks.

    Yields:
        Session: SQLAlchemy database session for the current request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias for database dependency
DbDependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def root() -> Dict[str, Any]:
    """Get application information and welcome message.

    Returns basic information about the ShortGic URL shortener service,
    including a welcome message and project details.

    Returns:
        Dict[str, Any]: Application information containing welcome message,
            description, and project website URL.
    """
    payload = {
        "hello": {
            "msg": "welcome on shortgic",
            "what": "a minimalist and lightweight URL shortener",
            "website": "https://github.com/smartgic/shortgic",
        }
    }
    return payload


@app.post("/", response_model=schemas.LinkResponse, status_code=201)
def create_link(link: schemas.Link, db: DbDependency) -> schemas.LinkResponse:
    """Create a new shortened link from a target URL.

    Generates a cryptographically secure short link for the provided target URL.
    Prevents duplicate URLs by checking if the target already exists in the database.

    Args:
        link: Link schema containing the target URL and optional extras.
        db: Database session dependency for database operations.

    Returns:
        LinkResponse: Response containing the generated short link identifier.

    Raises:
        HTTPException: 400 if the URL has already been shortened, with details
            about the existing short link.
        HTTPException: 500 if database operation fails.
    """
    # Check if the target already exists
    db_link = crud.get_link_by_target(db=db, target=link.target)
    if db_link:
        raise HTTPException(
            status_code=400,
            detail=utils.create_error_detail(
                "duplicate_url",
                "This URL has already been shortened",
                existing_link=db_link.link,
            ),
        )

    response = crud.create_link(db=db, link=link)
    return {"link": response.link}


@app.get("/{link}", status_code=302)
def get_link(link: str, db: DbDependency) -> RedirectResponse:
    """Redirect to the target URL associated with the short link.

    Validates the link format and redirects the user to the original target URL.
    This is the main functionality of the URL shortener service.

    Args:
        link: The short link identifier to resolve.
        db: Database session dependency for database operations.

    Returns:
        RedirectResponse: HTTP 302 redirect to the target URL.

    Raises:
        HTTPException: 400 if the link format is invalid (wrong length or
            contains non-alphanumeric characters).
        HTTPException: 404 if the short link does not exist in the database.
    """
    db_link = utils.get_link_or_404(db, link)
    return RedirectResponse(url=db_link.target, status_code=302)


@app.get("/{link}/info", response_model=schemas.Link)
def get_link_info(link: str, db: DbDependency) -> schemas.Link:
    """Get detailed information about a short link without redirecting.

    Returns the target URL and any associated metadata for the given short link.
    Useful for previewing links or API integrations that need link details.

    Args:
        link: The short link identifier to get information for.
        db: Database session dependency for database operations.

    Returns:
        Link: Complete link information including target URL and extras.

    Raises:
        HTTPException: 400 if the link format is invalid (wrong length or
            contains non-alphanumeric characters).
        HTTPException: 404 if the short link does not exist in the database.
    """
    return utils.get_link_or_404(db, link)


@app.delete("/{link}", status_code=204)
def delete_link(link: str, db: DbDependency) -> None:
    """Permanently delete a short link from the database.

    Removes the short link and all associated data from the database.
    This operation cannot be undone.

    Args:
        link: The short link identifier to delete.
        db: Database session dependency for database operations.

    Returns:
        None: No content returned on successful deletion (HTTP 204).

    Raises:
        HTTPException: 400 if the link format is invalid (wrong length or
            contains non-alphanumeric characters).
        HTTPException: 404 if the short link does not exist in the database.
        HTTPException: 500 if database operation fails.
    """
    utils.get_link_or_404(db, link)
    crud.delete_link(db=db, link=link)
    return None
