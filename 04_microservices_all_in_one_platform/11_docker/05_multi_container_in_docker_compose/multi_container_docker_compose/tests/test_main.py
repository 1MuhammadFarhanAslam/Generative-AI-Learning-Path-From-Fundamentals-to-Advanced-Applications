from fastapi.testclient import TestClient
from src.fastapi_project.main import app, books, Book


def test_root():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Library!"}

def test_get_books():
    client = TestClient(app)
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book():
    client = TestClient(app)
    response = client.post("/books", json={"id": 1, "title": "Book Title", "author": "Author Name", "year": 2023})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Book Title", "author": "Author Name", "year": 2023}

def test_get_books_1_when_empty():
    books.clear()  # make sure it's empty
    client = TestClient(app)
    response = client.get("/books_1")
    assert response.status_code == 200
    assert response.json() == {"message": "No books available"}


def test_get_books_1_with_books():
    books.clear()
    client = TestClient(app)
    # Add one book manually
    books.append({
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "year": 2023
    })
    response = client.get("/books_1")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Book Title", "author": "Author Name", "year": 2023}
    ]

def test_get_books_by_id():
    books.clear()

    books.append(Book(id=1, title="Book Title", author="Author Name", year=2023))
    client = TestClient(app)
    # Add one book manually
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Book Title", "author": "Author Name", "year": 2023}


def test_get_books_by_id_not_found():
    books.clear()
    client = TestClient(app)
    response = client.get("/books/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_delete_book():
    books.clear()
    client = TestClient(app)
    books.append(Book(id=1, title="Book Title", author="Author Name", year=2023))

    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted"}


def test_delete_book_not_found():
    books.clear()
    client = TestClient(app)
    response = client.delete("/books/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}