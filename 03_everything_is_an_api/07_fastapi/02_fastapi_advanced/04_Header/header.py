# header.py

from fastapi import FastAPI, Header, HTTPException, status
from typing import Optional, Dict

app = FastAPI(
    title="FastAPI Header Parameter Demo",
    description="Demonstrates using `FastAPI.Header` for accessing HTTP request headers.",
    version="1.0.0"
)

@app.get("/")
async def read_root() -> Dict[str, str]:
    """A simple root endpoint."""
    return {"message": "Welcome to the Header Parameter Demo!"}

@app.get("/items/")
async def read_items(
    # 1. Required Header: 'x-request-id' must be present in the request
    # FastAPI automatically converts 'x-request-id' to 'x_request_id' for the Python variable
    x_request_id: str = Header(
        ...,  # '...' makes it a required header
        title="Request ID",
        description="A unique ID for this request.",
        example="unique-trace-12345"
    ),
    # 2. Optional Header: 'user-agent' is optional (default value is None)
    # FastAPI automatically converts 'user-agent' to 'user_agent'
    user_agent: Optional[str] = Header(
        None,  # 'None' makes it an optional header
        title="User-Agent String",
        description="The User-Agent header from the client.",
        example="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    ),
    # 3. Header with Renaming (aliasing): If you want a different Python variable name
    # than the actual header name, or if the header name isn't auto-convertible (less common).
    # Here, 'x-api-key' is mapped to 'api_key_header'
    x_api_key: Optional[str] = Header(
        None,
        alias="X-API-Key", # Explicitly state the header name if it differs or for clarity
        title="API Key",
        description="Optional API key for authentication/authorization.",
        example="supersecretkey123"
    )
) -> Dict[str, str]:
    """
    Retrieves items and demonstrates accessing various HTTP headers.
    """
    response_data = {
        "message": "Headers received successfully!",
        "x_request_id": x_request_id,
        "user_agent": user_agent if user_agent else "Not provided",
        "api_key_header": x_api_key if x_api_key else "Not provided"
    }

    # Example of simple header validation within the endpoint
    if x_request_id == "invalid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Request-Id provided."
        )

    return response_data

# --- Run the application ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("header:app", host="127.0.0.1", port=8000, reload=True)