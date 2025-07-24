# database.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from typing import Generator
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("CONNECTION_STRING")

if not DATABASE_URL:
    raise ValueError("CONNECTION_STRING environment variable not set.")

# Create the SQLAlchemy engine for asynchronous operations
# Use `psycopg` for async support, replace with `asyncpg` if preferred
engine : Engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, connect_args={"sslmode": "require"})


Base = declarative_base()

def get_engine() -> Engine:
    """Returns the database engine."""
    return engine

def create_db_and_tables():
    """Creates all database tables defined by SQLAlchemy metadata."""
    Base.metadata.create_all(get_engine())

dbmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generates a new database session for each request."""
    db = dbmaker()
    try:
        yield db
    finally:
        db.close()