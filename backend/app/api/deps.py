from typing import Generator
from sqlalchemy.orm import Session

from app.config.database import SessionLocal


def get_db() -> Generator:
    """
    Dependency function that yields a database session.
    The session is automatically closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
