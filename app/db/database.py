from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

Base = declarative_base()

LocalSession = sessionmaker(
    bind = engine, 
    autoflush= False,
    autocommit = False
)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()