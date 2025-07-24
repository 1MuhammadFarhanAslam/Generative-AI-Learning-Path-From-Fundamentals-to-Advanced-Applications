# models.py
from typing import Optional, List, Generic, TypeVar, Any # Added Generic, TypeVar, Any
from sqlalchemy import Column, Integer, String, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field # Field for better control if needed

from database import Base # Import the Base from your database setup

# --- Generic API Response Model ---
T = TypeVar('T') # Define a type variable for the generic part

class ApiResponse(BaseModel, Generic[T]):
    """
    A generic API response model to wrap common success messages and data.
    'detail' will hold the actual response data (e.g., an Item, a list of Items).
    """
    message: str
    detail: T

# --- Pydantic Schemas (for request/response validation) ---

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True # Renamed from orm_mode to from_attributes for Pydantic V2+


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True # Renamed from orm_mode to from_attributes for Pydantic V2+


# --- SQLAlchemy ORM Models (No changes needed here for response format) ---

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    tax: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price={self.price})>"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (UniqueConstraint('username', name='_username_uc'),)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_active={self.is_active})>"