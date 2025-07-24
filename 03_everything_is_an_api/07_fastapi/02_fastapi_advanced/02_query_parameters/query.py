# query.py

from fastapi import FastAPI, Query, HTTPException, status # Changed Path to Query
from typing import Dict, Optional, List

# --- 1. FastAPI App Initialization ---
app = FastAPI(
    title="FastAPI Query Parameters Example with Validation",
    description="Demonstrates how to define and use query parameters in FastAPI with custom validation.",
    version="1.0.0"
)

# --- 2. Path Operations (Your API Endpoints) ---

# 1. Simple Query Parameter (String) - NOW ALLOWS SPACES
@app.get("/hello/") # Path changed: no {name} in URL
async def read_name(
    name: str = Query( # Changed Path to Query
        ...,  # This means the parameter is required
        min_length=2, # Optional: enforce a minimum length for the name
        max_length=50, # Optional: enforce a maximum length
        # Regex updated to allow letters (a-zA-Z) AND spaces ( )
        regex="^[a-zA-Z ]+$",
        title="User's Name",
        description="The name of the user. Must consist of alphabetic characters and spaces only."
    )
) -> Dict[str, str]:
    """
    Returns a greeting with the provided name from the URL query.
    This endpoint now strictly validates 'name' to be purely alphabetic or include spaces.

    Example Valid URLs:
      - /hello/?name=Alice
      - /hello/?name=John%20Doe (Note: spaces must be URL-encoded as %20)
      - /hello/?name=Maria%20Sofia

    Example Invalid URLs (will return 422 Unprocessable Entity):
      - /hello/?name=123
      - /hello/?name=Alice1
      - /hello/?name=John_Doe
      - /hello/?name=1+1
    """
    return {"message": f"Hello, {name}!"}

# 2. Query Parameter with Type Hint (Integer)
@app.get("/items/") # Path changed: no {item_id} in URL
async def get_item(
    item_id: int = Query( # Changed Path to Query
        ..., # Required query parameter
        title="Item ID",
        description="The unique identifier of the item."
    )
) -> Dict[str, str]:
    """
    Retrieves an item by its integer ID from the URL query.
    FastAPI automatically validates the type and converts it.
    Example URL: /items/?item_id=123
    """
    return {"item_id": str(item_id), "description": f"This is item number {item_id}"}

# 3. Multiple Query Parameters with Different Types
@app.get("/users/orders/") # Path changed: no {user_id}/{order_id} in URL
async def get_user_order(
    user_id: int = Query( # Changed Path to Query
        ..., # Required query parameter
        title="User ID",
        description="The unique identifier of the user."
    ),
    order_id: str = Query( # Changed Path to Query
        ..., # Required query parameter
        title="Order ID",
        description="The unique identifier of the order."
    )
) -> Dict[str, str]:
    """
    Retrieves a specific order for a specific user using multiple query parameters.
    Example URL: /users/orders/?user_id=456&order_id=ABC-789
    """
    return {
        "user_id": str(user_id),
        "order_id": order_id,
        "message": f"Details for order {order_id} of user {user_id}"
    }

# 4. Fixed Path Segment (remains unchanged as it has no parameters)
@app.get("/users/me")
async def read_user_me() -> Dict[str, str]:
    """
    Gets details for the current authenticated user (hypothetical).
    Example URL: /users/me
    """
    return {"user_id": "current_user", "message": "This is your profile."}

# 5. Query Parameter for User ID
@app.get("/users/") # Path changed: no {user_id} in URL
async def read_user(
    user_id: int = Query( # Changed Path to Query
        ..., # Required query parameter
        title="User ID",
        description="The unique identifier of the user."
    )
) -> Dict[str, str]:
    """
    Gets details for a specific user by ID from the URL query.
    Example URL: /users/?user_id=789
    """
    return {"user_id": str(user_id), "message": f"Details for user {user_id}."}


# --- Run the application ---
if __name__ == "__main__":
    import uvicorn
    # This is the correct way to run Uvicorn with reload when your file is 'url.py'
    uvicorn.run("query:app", host="127.0.0.1", port=8000, reload=True)