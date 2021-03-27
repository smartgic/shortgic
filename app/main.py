"""FastAPI application entrypoint
"""
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.responses import JSONResponse

# Create the database schema
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Database dependency
    Our dependency will create a new SQLAlchemy SessionLocal that will be used
    in a single request, and then close it once the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=schemas.Link)
def create_link(link: schemas.Link, db: Session = Depends(get_db)):
    """Create the link
    """
    # Check if the target already exists
    db_link = crud.get_link_by_target(db=db, target=link.target)
    if db_link:
        raise HTTPException(status_code=400, detail="link already registered")

    response = crud.create_link(db=db, link=link)
    payload = {'link': response.link}
    return JSONResponse(content=payload)


@app.get("/{link_id}", response_model=schemas.Link)
def get_link(link_id: str, db: Session = Depends(get_db)):
    """Retrieve the link information
    """
    db_link = crud.get_link(db, link_id=link_id)
    if db_link is None:
        raise HTTPException(status_code=404, detail="link not found")
    return db_link
