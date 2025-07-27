from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn

app: FastAPI = FastAPI(title="FastAPI App with docker compose.", description="A FastAPI app demonstrating all CRUD operations with docker compose.", version="1.0.0")

# In-memory "database"
fake_db: Dict[int, dict] = {}

# Pydantic model for input/output
class Item(BaseModel):
    name: str
    description: str
    price: float
    in_stock: bool = True


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint returning a welcome message.
    """
    return {"message": "Welcome to the FastAPI App with docker compose!"}


@app.post("/items/{item_id}", tags=["Create"])
def create_item(item_id: int, item: Item):
    """
    Create a new item in the fake DB.
    """
    if item_id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists.")
    fake_db[item_id] = item.dict()
    return {"message": "Item created successfully", "item": fake_db[item_id]}


@app.get("/items/{item_id}", tags=["Read"])
def read_item(item_id: int):
    """
    Read an item from the fake DB.
    """
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found.")
    return {"item": fake_db[item_id]}


@app.put("/items/{item_id}", tags=["Update"])
def update_item(item_id: int, item: Item):
    """
    Update an existing item in the fake DB.
    """
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found.")
    fake_db[item_id] = item.dict()
    return {"message": "Item updated successfully", "item": fake_db[item_id]}


@app.delete("/items/{item_id}", tags=["Delete"])
def delete_item(item_id: int):
    """
    Delete an item from the fake DB.
    """
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found.")
    del fake_db[item_id]
    return {"message": "Item deleted successfully"}


# This block is primarily for local development outside of Docker.
# When running in Docker, the CMD in the Dockerfile will handle execution.
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)

