# main.py

from fastapi import FastAPI
import uvicorn

# Initialize the FastAPI application
app: FastAPI = FastAPI()

# Define the root endpoint
@app.get("/")
def read_root():
    """
    Returns a simple greeting message and data about a role.
    """
    return {"message": "Hello World", "data": {"role": "testing"}}

# Define the /piaic/ endpoint
@app.get("/piaic/")
def read_item():
    """
    Returns a simple greeting message and data about an organization.
    """
    return {"message": "Hello World", "data": {"organization": "piaic"}}

# This block allows you to run the application directly using Uvicorn
# when the script is executed.
if __name__ == "__main__":
    # 'main:app' refers to the 'app' object in the 'main.py' file.
    # host="127.0.0.1" makes it accessible locally.
    # port=8000 sets the port number.
    # reload=True enables hot-reloading on code changes (useful for development).
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
