from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session 
from .config import database_config

class Base(DeclarativeBase): pass

def create_connection_string() -> str:
    return database_config()

def engine():
    engine = create_engine(database_config(), echo=False)

SessionLocal = sessionmaker(
    bind=engine(),
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

def get_session() -> Session:
    return SessionLocal()