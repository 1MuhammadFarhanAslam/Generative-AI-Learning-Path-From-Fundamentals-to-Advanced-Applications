# book_data.py
from book_model import Book

_books: list[Book] = [
    Book(id=1, title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", year_published=1979, genre="Science Fiction"),
    Book(id=2, title="Pride and Prejudice", author="Jane Austen", year_published=1813, genre="Romance"),
    Book(id=3, title="1984", author="George Orwell", year_published=1949, genre="Dystopian"),
    Book(id=4, title="To Kill a Mockingbird", author="Harper Lee", year_published=1960, genre="Fiction")
]

def get_all_books() -> list[Book]:
    return _books

# Practice: Add a function to get a book by its ID
def get_book_by_id(book_id: int) -> Book | None:
    # Iterate through _books and return the book if its ID matches book_id
    # If no book is found, return None
    for book in _books:
        if book.id == book_id:
            return book
    return None