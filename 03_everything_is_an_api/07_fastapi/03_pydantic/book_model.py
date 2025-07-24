# book_model.py
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    year_published: int
    genre: str