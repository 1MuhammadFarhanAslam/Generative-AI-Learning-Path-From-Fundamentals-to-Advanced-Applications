from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Grab DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
# Check if DATABASE_URL is set
# If not set, raise an error
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set.")
# Print for confirmation (Optional)
print(DATABASE_URL)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()