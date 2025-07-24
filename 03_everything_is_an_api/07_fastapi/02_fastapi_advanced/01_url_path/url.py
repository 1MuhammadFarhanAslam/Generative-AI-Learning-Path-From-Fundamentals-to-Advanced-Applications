# url.py (or main.py)

from fastapi import FastAPI, Path, HTTPException, status
from typing import Dict, Optional, List # Ensure all necessary types are imported

# --- 1. FastAPI App Initialization ---
app = FastAPI(
    title="FastAPI Path Parameters Example with Strict String Validation (Spaces Allowed)",
    description="Demonstrates how to define and use path parameters in FastAPI with custom validation.",
    version="1.0.0"
)

# --- 2. Path Operations (Your API Endpoints) ---

# 1. Simple Path Parameter (String) - NOW ALLOWS SPACES
@app.get("/hello/{name}")
async def read_name(
    name: str = Path(
        ...,  # This means the parameter is required
        min_length=2, # Optional: enforce a minimum length for the name
        max_length=50, # Optional: enforce a maximum length
        # Regex updated to allow letters (a-zA-Z) AND spaces ( )
        # ^ : asserts position at the start of the string
        # [a-zA-Z ]+ : matches one or more English alphabetic characters OR spaces
        # $ : asserts position at the end of the string
        regex="^[a-zA-Z ]+$", # <--- THIS IS THE UPDATED REGEX
        title="User's Name",
        description="The name of the user. Must consist of alphabetic characters and spaces only."
    )
) -> Dict[str, str]: # Function returns a dictionary
    """
    Returns a greeting with the provided name from the URL path.
    This endpoint now strictly validates 'name' to be purely alphabetic or include spaces.

    Example Valid URLs:
      - /hello/Alice
      - /hello/John Doe
      - /hello/Maria Sofia

    Example Invalid URLs (will return 422 Unprocessable Entity):
      - /hello/123
      - /hello/Alice1
      - /hello/John_Doe (contains underscore)
      - /hello/1+1
    """
    return {"message": f"Hello, {name}!"}

# 2. Path Parameter with Type Hint (Integer)
@app.get("/items/{item_id}")
async def get_item(item_id: int) -> Dict[str, str]:
    """
    Retrieves an item by its integer ID from the URL path.
    FastAPI automatically validates the type and converts it.
    Example URL: /items/123
    """
    return {"item_id": str(item_id), "description": f"This is item number {item_id}"} # Convert item_id to str for Dict[str,str]

# 3. Multiple Path Parameters with Different Types
@app.get("/users/{user_id}/orders/{order_id}")
async def get_user_order(user_id: int, order_id: str) -> Dict[str, str]:
    """
    Retrieves a specific order for a specific user using multiple path parameters.
    Example URL: /users/456/orders/ABC-789
    """
    return {
        "user_id": str(user_id), # Convert to str for Dict[str,str]
        "order_id": order_id,
        "message": f"Details for order {order_id} of user {user_id}"
    }

# 4. Path Parameter with a Fixed Path Segment (Order Matters!)
# If you have fixed paths that overlap with path parameters, fixed paths must come first.
@app.get("/users/me")
async def read_user_me() -> Dict[str, str]:
    """
    Gets details for the current authenticated user (hypothetical).
    This must be declared BEFORE /users/{user_id}
    Example URL: /users/me
    """
    return {"user_id": "current_user", "message": "This is your profile."}

@app.get("/users/{user_id}")
async def read_user(user_id: int) -> Dict[str, str]:
    """
    Gets details for a specific user by ID.
    Example URL: /users/789
    """
    return {"user_id": str(user_id), "message": f"Details for user {user_id}."} # Convert to str for Dict[str,str]


# --- Run the application ---
if __name__ == "__main__":
    import uvicorn
    # This is the correct way to run Uvicorn with reload when your file is 'url.py'
    uvicorn.run("url:app", host="127.0.0.1", port=8000, reload=True)