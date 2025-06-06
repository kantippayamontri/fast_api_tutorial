from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[
        int,
        Path(
            title="title: The ID of the item to get.",
            description="desc: The ID of the item to get.",
        ),
    ],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    """
    http://localhost:8000/items/123?item-query=a
    """
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result


# NOTE: number validation ( greater than ) or ( less then equal)
@app.get("/items_validate/{item_id}")
async def read_items_validate(
    item_id: Annotated[int, Path(ge=1, le=100)], q: str | None = None
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result


# NOTE: number validation for float -> the same as int
@app.get("/items_float_validate/{item_id}")
async def read_items_float_validate(
    item_id: Annotated[float, Path(ge=1, le=100)],
    size: Annotated[float, Query(gt=1, lt=10.5)] = None,
    q: Annotated[str | None, Query()] = None,
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if size:
        result.update({"size": size})
    return {"item_id": item_id}

"""
ge = greater than or equal to
gt = greater than
le = less than or equal to
lt = less than
"""
