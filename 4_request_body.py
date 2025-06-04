from fastapi import FastAPI
from pydantic import BaseModel

"""
request body = data that send from client to server(API)
response body = data the send from server(API) to client

we will use pydantic model to define the data type of request body

To send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.
Sending a body with a GET request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.
As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using GET, and proxies in the middle might not support it.
"""

"""
summary:
    if we send request body, we should use post(more common), put, delete or patch method
"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    """
    use pydantic == request body
    fastapi will recognize the request body is pydantic class
    """
    return item

# NOTE: request body + path + query parameters
@app.put("/items/{item_id}")
async def update_item(item_id:int, item: Item, q:str | None = None):
    """
    item_id = path parameter
    item = request body
    q = query parameter
    """
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


"""
FastAPI will know that the value of q is not required because of the default value = None.
The str | None (Python 3.10+) or Union in Union[str, None] (Python 3.8+) is not used by FastAPI to determine that the value is not required, it will know it's not required because it has a default value of = None.
But adding the type annotations will allow your editor to give you better support and detect errors.

summary:
    not required parameter == default value = None
    not required parameter != | None
"""
