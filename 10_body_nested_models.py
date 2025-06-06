from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []  # NOTE: list fields -> you can add anything in list


class ItemFixedString(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []  # list fields -> you can add only string in list
    """
    NOTE:
        This will make tags be a list, although it doesn't declare the type of the elements of the list.
    """


class ItemSet(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[int] = set()  # list fields -> you can add only string in list


class Image(BaseModel):
    url: str
    name: str


class ItemModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()  # list fields -> you can add only string in list
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: Annotated[int, Path()], item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items_fix_string/{item_id}")
async def update_item_fix_string(item_id: Annotated[int, Path()], item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# NOTE: set type -> declare set instead of list in ItemSet
@app.put("/items_set/{item_id}")
async def update_item_set(item_id: Annotated[int, Path()], item: ItemSet):
    """
    Request body

    {
        "name": "string",
        "description": "string",
        "price": 0,
        "tax": 0,
        "tags": [1,2,3,1,1,3]
    }

    Response body

    {
    "item_id": 123,
    "item": {
        "name": "string",
        "description": "string",
        "price": 0,
        "tax": 0,
        "tags": [
                    1,
                    2,
                    3
                ]
        }
    }

    """
    results = {"item_id": item_id, "item": item}
    return results


# NOTE: Nested model
@app.put("/items_model/{item_id}")
async def update_item_model(item_id: Annotated[int, Path()], item: ItemModel):
    """
    request body

    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2,
        "tags": ["rock", "metal", "bar"],
        "image": {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        }
    }

    """
    results = {"item_id": item_id, "item": item}
    return results

#NOTE: special type and validation

"""
Apart from normal singular types like str, int, float, etc. you can use more complex singular types that inherit from str.

To see all the options you have, checkout Pydantic's Type Overview. You will see some examples in the next chapter.

link: https://docs.pydantic.dev/latest/concepts/types/
"""
