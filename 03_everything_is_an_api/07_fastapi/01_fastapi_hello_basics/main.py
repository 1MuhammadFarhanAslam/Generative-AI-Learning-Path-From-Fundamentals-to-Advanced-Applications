# main.py

from fastapi import FastAPI, HTTPException, status, Depends
from typing import List, Union # Union for flexibility in response types
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database import create_db_and_tables, get_db
from models import Item, ItemCreate, ItemUpdate, ItemResponse, User, UserCreate, UserResponse, ApiResponse # Import ApiResponse

# --- 1. FastAPI App Initialization ---
app = FastAPI(
    title="FastAPI with Neon DB (API Developer: Muhammad Farhan Aslam)",
    description="A simple API demonstrating FastAPI with Neon PostgreSQL.",
    version="1.0.0",
)

# --- 2. Event Handlers for Database Setup ---
@app.on_event("startup")
def on_startup():
    """Create database tables on application startup."""
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created (or already exist).")


# --- 3. Path Operations (Your API Endpoints) ---

@app.get("/", response_model=ApiResponse[dict]) # Use ApiResponse for root endpoint too
async def read_root():
    """Returns a simple greeting wrapped in the standard response format."""
    return {"message": "Welcome to the FastAPI with Neon DB Demo API!", "detail": {"status": "online"}}

# Item Endpoints
@app.post("/items/", response_model=ApiResponse[ItemResponse], status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    session: Session = Depends(get_db)
):
    """
    Creates a new item in the database and returns it in the standard response format.
    """
    db_item = Item(**item.dict())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return {"message": "Item created successfully.", "detail": db_item} # Wrapped response

@app.get("/items/", response_model=ApiResponse[List[ItemResponse]])
async def read_items(
    session: Session = Depends(get_db)
):
    """Retrieves a list of all items in the standard response format."""
    result = session.execute(select(Item))
    items = result.scalars().all()
    return {"message": "Items retrieved successfully.", "detail": items} # Wrapped response

@app.get("/items/{item_id}", response_model=ApiResponse[ItemResponse], summary="Get a single item by ID")
async def read_item(
    item_id: int,
    session: Session = Depends(get_db)
):
    """
    Retrieves a single item from the database based on its ID in the standard response format.
    """
    result = session.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found."
        )
    return {"message": "Item retrieved successfully.", "detail": item} # Wrapped response

@app.put("/items/{item_id}", response_model=ApiResponse[ItemResponse])
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    session: Session = Depends(get_db)
):
    """Updates an existing item and returns it in the standard response format."""
    result = session.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalars().first()

    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item_data = item_update.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return {"message": f"Item {item_id} updated successfully.", "detail": db_item} # Wrapped response

# For DELETE, detail will be an empty object, or a simple confirmation.
# The user's example had the *created* item in detail. For delete, an empty dict is usually sufficient.
@app.delete("/items/{item_id}", response_model=ApiResponse[dict], status_code=status.HTTP_200_OK) # Changed to 200 OK
async def delete_item(
    item_id: int,
    session: Session = Depends(get_db)
):
    """Deletes an item by ID and confirms in the standard response format."""
    result = session.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    session.delete(item)
    session.commit()
    return {"message": f"Item {item_id} deleted successfully.", "detail": {}} # Empty dict as detail for deletion

# User Endpoints
@app.post("/users/", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_db)
):
    """Creates a new user and returns it in the standard response format."""
    result = session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with username '{user.username}' already exists."
        )

    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "User created successfully.", "detail": db_user} # Wrapped response

@app.get("/users/", response_model=ApiResponse[List[UserResponse]])
async def read_users(
    session: Session = Depends(get_db)
):
    """Retrieves a list of all users in the standard response format."""
    result = session.execute(select(User))
    users = result.scalars().all()
    return {"message": "Users retrieved successfully.", "detail": users} # Wrapped response

@app.get("/users/{user_id}", response_model=ApiResponse[UserResponse])
async def read_user(
    user_id: int,
    session: Session = Depends(get_db)
):
    """Retrieves a single user by ID in the standard response format."""
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    return {"message": "User retrieved successfully.", "detail": user} # Wrapped response

# --- 4. Custom Error Handling (Optional) ---
# We can also wrap HTTPExceptions in this format if desired,
# but FastAPI's default HTTPException handling is often sufficient and standardized.
# For now, keeping the default HTTPException response for consistency with common FastAPI patterns.
# If you wanted to standardize errors too:
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#    return JSONResponse(
#        status_code=exc.status_code,
#        content={"message": "Error occurred", "detail": exc.detail},
#    )

# For direct execution (e.g., if you run `python main.py` instead of `uvicorn main:app`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)