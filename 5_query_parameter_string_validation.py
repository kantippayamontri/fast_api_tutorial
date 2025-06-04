from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: str | None = None):
    """
    FastAPI will know that the value of q is not required because of the default value = None.
    Having str | None will allow your editor to give you better support and detect errors.
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# NOTE: additional validation
@app.get("/items_query_validate/")
async def read_item_query_validate(
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    """
    you can send query q with max length 50 characters
    """
    if q:
        return {"q": q}
    return {"q": "success but no query"}


"""
how to use Annotated to help validate query parameters

Annotate has 2 parameters
1. type -> actual type
    q: Annotated[str | None] = None -> q: str | None = None
2. validation -> validation
    q: Annotated[str | None, Query(max_length=50)] = None -> q: str | None = None, with max length of q 50 characters

#NOTE:
    Here we are using Query() because this is a query parameter. 
    Later we will see others like Path(), Body(), Header(), and Cookie(), that also accept the same arguments as Query().
"""

# NOTE: additional validation(old ways)
@app.get("/items_query_validate_old/")
async def read_item_query_validate_old(
    q: str | None = Query(default=None, )
):
    ...

