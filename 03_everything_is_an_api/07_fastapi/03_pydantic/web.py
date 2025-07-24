# book_web.py
from fastapi import FastAPI
from book_model import Book
from fastapi import FastAPI, HTTPException
from book_data import get_all_books, get_book_by_id

app = FastAPI()

# Endpoint to get all books
@app.get("/books")
def list_books() -> list[Book]:
    return get_all_books()

# Practice: Add an endpoint to get a single book by its ID
@app.get("/books/{book_id}")
def get_single_book(book_id: int) -> Book:
    book = get_book_by_id(book_id)
    if book is None:
        # If the book is not found, raise an HTTP 404 Not Found error
        raise HTTPException(status_code=404, detail="Book not found")
    return book

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web:app", host="127.0.0.1", port=8000, reload=True)