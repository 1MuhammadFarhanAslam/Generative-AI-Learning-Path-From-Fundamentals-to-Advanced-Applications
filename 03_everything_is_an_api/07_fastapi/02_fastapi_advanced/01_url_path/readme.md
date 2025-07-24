## Accessing and Testing the API

This section guides you on how to run your FastAPI application and interact with its endpoints.

### 1\. Run the API Server (Uvicorn)

First, start your FastAPI application using Uvicorn. Navigate to your project directory in the terminal and execute:

```bash
python url.py
# OR, if your main file is named main.py and you prefer the standard way:
# uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see output indicating the server is running, typically at `http://127.0.0.1:8000`.

### 2\. Explore API Documentation (Swagger UI / ReDoc)

FastAPI automatically generates interactive API documentation. This is the easiest way to see all available endpoints, their expected inputs, and example responses, and to even send requests directly from your browser.

  * **Swagger UI:** Open your browser and go to `http://127.0.0.1:8000/docs`
  * **ReDoc:** Open your browser and go to `http://127.0.0.1:8000/redoc`

### 3\. Send Requests to the API

You can interact with the API using various tools:

#### A. Command Line Tools

**HTTPie (Recommended for readable output):**
If you have `HTTPie` installed (`pip install httpie`), it provides a user-friendly way to send HTTP requests.

  * **GET Request (e.g., retrieve an item):**
    ```bash
    http http://localhost:8000/items/1
    ```
  * **POST Request (e.g., create an item):**
    ```bash
    http POST http://localhost:8000/items/ name="New Gadget" price:=29.99
    ```
  * **PUT Request (e.g., update an item):**
    ```bash
    http PUT http://localhost:8000/items/1 name="Updated Gadget Pro" price:=35.00
    ```
  * **DELETE Request (e.g., delete an item):**
    ```bash
    http DELETE http://localhost:8000/items/1
    ```

**cURL (Universal Command-Line Tool):**
`cURL` is pre-installed on most systems and is a powerful way to send requests.

  * **GET Request:**
    ```bash
    curl http://localhost:8000/items/1
    ```
  * **POST Request:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "New Gadget", "price": 29.99}' http://localhost:8000/items/
    ```
  * **PUT Request:**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Gadget Pro", "price": 35.00}' http://localhost:8000/items/1
    ```
  * **DELETE Request:**
    ```bash
    curl -X DELETE http://localhost:8000/items/1
    ```

#### B. Graphical User Interface (GUI) Tools

Tools like **Postman** or **Insomnia** provide a visual interface to build and send API requests. Download and install your preferred tool, then simply enter the endpoint URLs and configure the headers/body as needed.

#### C. Programmatically (Python)

You can send requests directly from your Python code using the `requests` library (`pip install requests`).

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# GET Example
response = requests.get(f"{BASE_URL}/items/1")
print("GET Response:", response.json())

# POST Example
new_item_data = {"name": "Smart Plug", "description": "Wi-Fi controlled power outlet", "price": 19.99}
response = requests.post(f"{BASE_URL}/items/", json=new_item_data)
print("POST Response:", response.json())

# PUT Example
updated_item_data = {"name": "Smart Plug v2", "price": 24.99}
response = requests.put(f"{BASE_URL}/items/1", json=updated_item_data)
print("PUT Response:", response.json())

# DELETE Example
response = requests.delete(f"{BASE_URL}/items/1")
print("DELETE Response:", response.json())
```