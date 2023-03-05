"""FastAPI Pydantic schema
"""
from typing import Optional, Any, Dict
from pydantic import BaseModel, HttpUrl


class Link(BaseModel):
    """Link structure validation"""

    target: HttpUrl
    extras: Optional[Dict[str, Any]] = {}

    # Required because used with SQLAlchemy
    class Config:
        orm_mode = True


class LinkResponse(BaseModel):
    """Link structure response"""

    link: str
