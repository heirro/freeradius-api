from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import get_database_url

engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=200,
    max_overflow=100,
    pool_timeout=600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()