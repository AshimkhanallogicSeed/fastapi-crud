from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory "database"
items_db = []

# Create
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items_db.append(item)
    return item

# Read all
@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    return items_db[skip: skip + limit]

# Read by ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    for idx, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            items_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[idx]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
