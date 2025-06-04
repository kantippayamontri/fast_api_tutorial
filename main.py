from enum import Enum
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
    return {
        "Hello": "World"
    }  # You can return a dict, list, singular values as str, int, etc.


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# NOTE: path converter
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/items/{item_id}")
def read_item(
    item_id: int, q: Union[str, None] = None
):  # item_id and q is a parameter pass with url
    # http://127.0.0.1:8000/items/foo?q=somequery
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(
    item_id: int, item: Item
):  # item_id = parameter pass with url , item is a request body pass with json body
    return {
        "item_id": item_id,
        "item_name": item.name,
        "item_price": item.price,
        "item_offer": item.is_offer,
    }


class ModelName(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "this is alexnet ...",
        }

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Deep Learning FTW!"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    /files/{file_path:path}
    In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.
    """
    return {"file": file_path}

#NOTE: query parameter

