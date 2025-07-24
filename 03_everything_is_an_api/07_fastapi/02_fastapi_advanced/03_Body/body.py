# body.py

from fastapi import FastAPI, Body
from typing import Dict

app = FastAPI(
    title="FastAPI Body Parameter Demo",
    description="Demonstrates using `FastAPI.Body` with `embed=True`, string validation, "
                "and correctly formatted `examples` for Swagger UI.",
    version="1.0.0"
)

@app.post("/greet/")
def greet(
    # 'who' is the name of the key expected in the JSON request body.
    # 'embed=True' means the value for 'who' should be nested inside a JSON object.
    # Expected Request Body: {"who": "Alice"}
    who: str = Body(
        ..., # This makes 'who' a required body parameter
        embed=True, # Expects the value for 'who' to be nested like {"who": "value"}
        title="Name to Greet",
        description="The name of the person to greet. Must consist only of alphabetic characters and spaces.",
        min_length=2, # Enforce a minimum length of 2 characters
        max_length=50, # Enforce a maximum length of 50 characters
        regex="^[a-zA-Z ]+$", # Strict content check: only allows English letters (a-z, A-Z) and spaces

        # --- Corrected 'examples' parameter for Swagger UI ---
        # 'examples' must be a LIST of dictionaries.
        # Each dictionary represents a single example that will appear in the Swagger UI dropdown.
        # The 'value' key within each example dictionary must contain the ENTIRE JSON body
        # that the endpoint expects.
    )
) -> Dict[str, str]:
    """
    Greets the person specified in the request body.

    The request body must be a JSON object like: `{"who": "YourName"}`.
    The 'YourName' value will be strictly validated against length and content rules.

    Returns:
        A JSON object with a greeting message.
    """
    return {"message": f"Hello, {who}!"}

# --- Run the application ---
if __name__ == "__main__":
    import uvicorn
    # Make sure 'body:app' matches your Python file name (e.g., body.py)
    # If your file is main.py, change this to "main:app"
    uvicorn.run("body:app", host="127.0.0.1", port=8000, reload=True)