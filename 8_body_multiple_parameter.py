from typing import Annotated, Literal

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

"""
Note: passing body -> put, post, delete
"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    tags: list[str] = []
    order_by: Literal["created_at", "updated_at"] = "created_at"


# NOTE: single body
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(ge=10, le=1000)],
    q: str | None = None, #query
    item: Item | None = None, #body
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# NOTE: multiple body
@app.put("/items_multiple/{item_id}")
async def update_multiple_item(
    item_id: Annotated[int, Path()],
    filter_query: Annotated[FilterParams, Body()], #body
    item: Item, #body
    user: User, #body
):
    results = {"item_id": item_id, "item": item, "user": user}
    if filter_query:
        results.update({"filter_query": filter_query})
    return results


# NOTE: singular value in body -> pass single value in body
@app.put("/items_singular_body/{item_id}")
async def update_singular_body(
    item_id: Annotated[int, Path()],
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
):
    """
    for multiple value body -> use pydantic and Body
    for singular value body -> use Body
    """
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# NOTE: mutiple body params and query
@app.put("/items_multiple_body_query/{item_id}")
async def update_multiple_body_query(
    *,
    item_id: Annotated[int, Path()],  # path
    item: Item,  # body
    user: User,  # body
    importance: Annotated[int, Body(gt=50)],
    q: str | None = None,  # query
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# NOTE: embed a single body parameter
@app.put("/items_embed/{item_id}")
async def update_items_embed(
    item_id: Annotated[int, Path()], item: Annotated[Item, Body(embed=True)]
):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items_no_embed/{item_id}")
async def update_items_no_embed(
    item_id: Annotated[int, Path()], item: Annotated[Item, Body(embed=False)]
):
    results = {"item_id": item_id, "item": item}
    return results
