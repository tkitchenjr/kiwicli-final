from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, session 
from .config import database_config

class Base(DeclarativeBase): pass
def create_connection_string() -> str:
    return database_config()

engine = create_engine(database_config), echo=True
LocalSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  
)


def get_session():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
   