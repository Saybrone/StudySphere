from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


# -------------------------
# Note Model (User's Notes)
# -------------------------
class Note(Base):
    __tablename__ = "notes"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key -> links each note to a user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Note title (required)
    title = Column(String(255), nullable=False)

    # Note content/body (required)
    content = Column(Text, nullable=False)

    # Optional file path (uploaded file)
    file_path = Column(String(255), nullable=True)

    # Auto timestamp for creation
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Auto timestamp for updating
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User model
    # back_populates="notes" connects it to User.notes
    user = relationship("User", back_populates="notes")


# -------------------------
# User Model
# -------------------------
class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Username must be unique
    username = Column(String, unique=True, index=True)

    # Email must be unique
    email = Column(String, unique=True, index=True)

    # Password (hashed)
    password = Column(String)

    # Relationship: a user can have many notes
    # cascade="all, delete" ensures deleting a user deletes their notes
    notes = relationship("Note", back_populates="user", cascade="all, delete")
