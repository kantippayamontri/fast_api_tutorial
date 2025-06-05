from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[
        int,
        Path(
            title="The ID of the item to get.", description="The ID of the item to get."
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
