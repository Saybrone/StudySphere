from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL (PostgreSQL, MySQL, SQLite, etc.)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
# pool_pre_ping=True -> Automatically test connections before using them (prevents stale connections)
# pool_recycle=300   -> Recycles connections after 300 seconds to avoid "MySQL server has gone away"
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

# Session factory
# autocommit=False -> Transactions must be explicitly committed
# autoflush=False  -> SQLAlchemy won't auto-send data to DB until commit
# bind=engine      -> Attach session to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
# All models will inherit from this Base
Base = declarative_base()
