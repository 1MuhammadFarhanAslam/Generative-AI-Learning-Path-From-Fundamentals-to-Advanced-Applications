**What are WebSockets?**

  * **Full-duplex communication:** Unlike traditional HTTP, which is a request-response protocol (client asks, server replies, then the connection closes), WebSockets establish a **persistent, open connection**. This means both the client and the server can send messages to each other at any time, independently.
  * **Real-time updates:** This persistent connection is crucial for applications that need instant updates, such as:
      * **Chat applications:** Messages appear instantly for all participants.
      * **Live notifications:** Users get alerts immediately when something new happens.
      * **Online gaming:** Player actions and game state changes are synchronized in real-time.
      * **Collaborative tools:** Multiple users can edit a document simultaneously, seeing changes as they happen.

**Why use WebSockets with FastAPI?**

FastAPI is a modern, fast, and high-performance web framework for building APIs with Python. Its key advantages for WebSockets include:

  * **Asynchronous capabilities:** FastAPI is built on ASGI (Asynchronous Server Gateway Interface), which inherently supports asynchronous programming (`async`/`await`). This makes it well-suited for handling many concurrent WebSocket connections efficiently without blocking the server.
  * **Ease of use:** FastAPI provides a clean and intuitive way to define WebSocket endpoints, similar to how you define regular HTTP endpoints. You simply use `@app.websocket()` decorator.
  * **Type hints:** FastAPI leverages Python type hints, which helps with code completion, data validation, and better code readability when dealing with WebSocket messages.
  * **Integration with existing features:** You can seamlessly integrate WebSocket logic with other FastAPI features like dependency injection, security, and exception handling.

**How to implement WebSockets in FastAPI:**

1.  **Install necessary libraries:** You'll need `fastapi` and an ASGI server like `uvicorn`, and the `websockets` library.
    ```bash
    pip install fastapi "uvicorn[standard]" websockets
    ```
2.  **Define a WebSocket endpoint:** Use the `@app.websocket()` decorator. Your endpoint function will receive a `WebSocket` object.
    ```python
    from fastapi import FastAPI, WebSocket

    app = FastAPI()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept() # Establish the connection
        try:
            while True:
                data = await websocket.receive_text() # Receive messages
                await websocket.send_text(f"Message text was: {data}") # Send messages back
        except WebSocketDisconnect:
            print("Client disconnected")
    ```
3.  **Manage connections (for multiple clients):** For applications like chat, you'll often need to keep track of active connections and broadcast messages to all of them. This typically involves a `ConnectionManager` class.
    ```python
    from typing import List
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect

    app = FastAPI()

    class ConnectionManager:
        def __init__(self):
            self.active_connections: List[WebSocket] = []

        async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)

        def disconnect(self, websocket: WebSocket):
            self.active_connections.remove(websocket)

        async def broadcast(self, message: str):
            for connection in self.active_connections:
                await connection.send_text(message)

    manager = ConnectionManager()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"Client says: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast("A client disconnected.")
    ```

**In summary:**

WebSockets in FastAPI enable you to build robust and efficient real-time applications by providing a persistent, two-way communication channel between your clients and server, leveraging FastAPI's asynchronous capabilities and developer-friendly syntax.