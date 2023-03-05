"""FastAPI CRUD file
"""
from sqlalchemy.orm import Session
from . import models, schemas
from random import sample
from string import ascii_letters, digits


def get_link(db: Session, link: str):
    """Retrieve link information by link ID"""
    return db.query(models.Link).filter(models.Link.link == link).first()


def get_link_by_target(db: Session, target: str):
    """Retrieve link information by target name"""
    return db.query(models.Link).filter(models.Link.target == target).first()


def create_link(db: Session, link: schemas.Link):
    """Create the link"""
    # Generates random string of 5 chars with letters, digits and uppercase
    chars = ascii_letters + digits
    shortened = "".join(sample(chars, 5)).upper()

    # SQLAlchemy magic :)
    db_link = models.Link(link=shortened, target=link.target, extras=link.extras)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def delete_link(db: Session, link: str):
    """Delete the link"""
    # SQLAlchemy magic :)
    db_link = db.query(models.Link).filter(models.Link.link == link).first()
    db.delete(db_link)
    db.commit()
    return {}
