## Accessing and Testing the API

This section guides you on how to run your FastAPI application and interact with its endpoints, which now primarily use **query parameters** for variable inputs.

### 1\. Run the API Server (Uvicorn)

First, start your FastAPI application using Uvicorn. Navigate to your project directory in the terminal and execute:

```bash
python url.py
# OR, if your main file is named main.py and you prefer the standard way:
# uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see output indicating the server is running, typically at `http://127.0.0.1:8000`.

### 2\. Explore API Documentation (Swagger UI / ReDoc)

FastAPI automatically generates interactive API documentation. This is the easiest way to see all available endpoints, their expected inputs (now as query parameters), and example responses, and to even send requests directly from your browser.

  * **Swagger UI:** Open your browser and go to `http://127.0.0.1:8000/docs`
  * **ReDoc:** Open your browser and go to `http://127.0.0.1:8000/redoc`

### 3\. Send Requests to the API

You can interact with the API using various tools. Remember that for query parameters, values are appended to the URL after a question mark (`?`), and multiple parameters are separated by an ampersand (`&`). Spaces or special characters in values must be URL-encoded (e.g., space becomes `%20`).

#### A. Command Line Tools

**HTTPie (Recommended for readable output):**
If you have `HTTPie` installed (`pip install httpie`), it provides a user-friendly way to send HTTP requests.

  * **GET `/hello/` (with `name` query parameter):**
    ```bash
    http http://localhost:8000/hello/ name=="Alice"
    # For names with spaces:
    http http://localhost:8000/hello/ name=="John Doe"
    ```
  * **GET `/items/` (with `item_id` query parameter):**
    ```bash
    http http://localhost:8000/items/ item_id==1
    ```
  * **GET `/users/orders/` (with `user_id` and `order_id` query parameters):**
    ```bash
    http http://localhost:8000/users/orders/ user_id==456 order_id=="ABC-789"
    ```
  * **GET `/users/` (with `user_id` query parameter):**
    ```bash
    http http://localhost:8000/users/ user_id==789
    ```

**cURL (Universal Command-Line Tool):**
`cURL` is pre-installed on most systems and is a powerful way to send requests. You'll need to manually URL-encode query parameter values if they contain special characters like spaces.

  * **GET `/hello/`:**
    ```bash
    curl "http://localhost:8000/hello/?name=Alice"
    curl "http://localhost:8000/hello/?name=John%20Doe" # Note %20 for space
    ```
  * **GET `/items/`:**
    ```bash
    curl "http://localhost:8000/items/?item_id=1"
    ```
  * **GET `/users/orders/`:**
    ```bash
    curl "http://localhost:8000/users/orders/?user_id=456&order_id=ABC-789"
    ```
  * **GET `/users/`:**
    ```bash
    curl "http://localhost:8000/users/?user_id=789"
    ```

#### B. Graphical User Interface (GUI) Tools

Tools like **Postman** or **Insomnia** provide a visual interface to build and send API requests. Download and install your preferred tool, then simply enter the endpoint URLs (including the query parameters in the URL bar) and configure the headers/body as needed.

#### C. Programmatically (Python)

You can send requests directly from your Python code using the `requests` library (`pip install requests`).

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# GET /hello/ Example
response = requests.get(f"{BASE_URL}/hello/", params={"name": "Alice"})
print("GET /hello/ Response:", response.json())

# GET /items/ Example
response = requests.get(f"{BASE_URL}/items/", params={"item_id": 1})
print("GET /items/ Response:", response.json())

# GET /users/orders/ Example
response = requests.get(f"{BASE_URL}/users/orders/", params={"user_id": 456, "order_id": "ABC-789"})
print("GET /users/orders/ Response:", response.json())

# GET /users/ Example
response = requests.get(f"{BASE_URL}/users/", params={"user_id": 789})
print("GET /users/ Response:", response.json())

# Example for the fixed path without query params
response = requests.get(f"{BASE_URL}/users/me")
print("GET /users/me Response:", response.json())
```