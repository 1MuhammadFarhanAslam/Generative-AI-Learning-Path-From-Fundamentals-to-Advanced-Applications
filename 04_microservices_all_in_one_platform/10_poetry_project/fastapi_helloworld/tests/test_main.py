# test_main.py

# Import the FastAPI application instance from your main application file.
# This assumes your main.py is located in src/fastapi_helloworld/main.py
# and your project structure is set up for a 'src' layout.
from src.fastapi_helloworld.main import app
from fastapi.testclient import TestClient

# Create a TestClient instance for your FastAPI application.
# The TestClient allows you to make requests to your application
# directly in Python, without needing to run a separate server.
client = TestClient(app=app)

# Define a test function for the root endpoint ("/").
# Pytest automatically discovers functions starting with 'test_'.
def test_read_root():
    """
    Tests the root endpoint to ensure it returns the expected status code and JSON response.
    """
    # Make a GET request to the root endpoint.
    response = client.get("/")

    # Assert that the HTTP status code of the response is 200 (OK).
    assert response.status_code == 200

    # Assert that the JSON content of the response matches the expected dictionary.
    assert response.json() == {"message": "Hello World", "data": {"role": "testing"}}

# You could add more test functions for other endpoints, e.g.:
# def test_read_piaic():
#     response = client.get("/piaic/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World", "data": {"organization": "piaic"}}
