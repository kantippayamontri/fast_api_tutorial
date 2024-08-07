from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel  # standard python types

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"} # You can return a dict, list, singular values as str, int, etc.

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None): # item_id and q is a parameter pass with url
    # http://127.0.0.1:8000/items/foo?q=somequery
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item): # item_id = parameter pass with url , item is a request body pass with json body
    return { "item_id": item_id, "item_name": item.name, "item_price":item.price, "item_offer":item.is_offer}

