from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

"""
we can further validate inside for pydantic model with `Field`

`Field` has the same options as `Query`, `Path` and `Body`
`Field` use to validate the attribute of the model

Note:
    `Field` is used to validate the attribute of the model -> import from pydantic
    `Query`, `Path` and `Body` is used to validate the parameter of the function -> import from fastapi
"""


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=20
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body()]):
    results = {"item_id": item_id, "item": item}
    return results
