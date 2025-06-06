from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    tags: list[str] = []
    order_by: Literal["created_at", "updated_at"] = "created_at"

class TestFilter(BaseModel):
    # model_config = {"extra": "forbid"}
    test: int = Field(12, gt=0, le=100)


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    """
    for using pydantic models as query parameters, we need to install fastapi version 0.115.0 and above
    """
    return filter_query

#NOTE: Forbid Extra Query Parameters
@app.get("/items_forbid/")
async def read_items_forbid(test_query: Annotated[TestFilter, Query()]):
    """
    in the case that don't want user to send the extra query parameters, we can use the model_config = {"extra": "forbid"}

    for TestFilter you can only send `test` query parameter
    if you send other query parameters -> you will get error

    http://localhost:8000/items_forbid/?test=13 -> ✅
    http://localhost:8000/items_forbid/?test=13&q=this is query -> ❌
    """
    return test_query
