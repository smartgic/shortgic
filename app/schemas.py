"""FastAPI Pydantic schema
"""
from typing import Optional, Any, Dict
from pydantic import BaseModel, HttpUrl, typing


class Link(BaseModel):
    """Link structure validation
    """
    target: HttpUrl
    extras: Optional[typing.Dict[str, Any]] = {}

    # Required because used with SQLAlchemy
    class Config:
        orm_mode = True
