import random
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()

#
# @app.get("/items/")
# async def read_items(q: str | None = None):
#     """
#     FastAPI will know that the value of q is not required because of the default value = None.
#     Having str | None will allow your editor to give you better support and detect errors.
#     """
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3)]):
    """
    q has not default value -> q is required
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# NOTE: additional validation
@app.get("/items_query_validate/")
async def read_item_query_validate(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixquery$")
    ] = None,  # pattern = regular expression
):
    """
    you can send query q with max length 50 characters
    """
    if q:
        return {"q": q}
    return {"q": "success but no query"}


@app.get("/items_query_fixed_default/")
async def read_item_query_fix_default(
    q: Annotated[str, Query(min_length=3)] = "this is fixed default value",
):
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
    q: str | None = Query(default=None, max_length=50),
):
    """
    old way use Query() to validate query parameters
    new way use Annotated to validate query parameters

    NOTE: for new way you can not pass default value in Query()
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# NOTE: query parameter list/ multiple value
# you can pass the same query varibale multiple time
@app.get("/items_query_list/")
async def read_query_list(q: Annotated[list[str] | None, Query()] = ["foo", "bar"]):
    """
    http://localhost:8000/items_query_list/?q=a
    http://localhost:8000/items_query_list/?q=a&q=b
    http://localhost:8000/items_query_list/?q=a&q=b&q=c

    # you can pass q parameter multiple time -> type of q need to be list
    """
    return {"q": q}


@app.get("/items_query_list_no_type/")
async def read_query_list_no_type(
    q: Annotated[
        list, Query(title="query string", description="Query string description...")
    ] = [],
):
    """
    note:
        In Query we pass title and description -> you can see in swagger UI
    http://localhost:8000/items_query_list_no_type/?q=1
    http://localhost:8000/items_query_list_no_type/?q=1&q=kan
    http://localhost:8000/items_query_list_no_type/?q=1&q=kan&q=hahaha
    """
    return {"q": q}


# NOTE: alias parameter
"""
Imaging you want the parameter to be `item-query` but is not a valid python variable name.
the closest would be `item_query` but it is not the same.
"""


@app.get("/items_alias/")
async def read_item_alias(q: Annotated[str | None, Query(alias="item-query")]):
    """
    http://localhost:8000/items_alias/?item-query=kan
    note:
        you can see in swagger UI the parameter is `item-query`
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# NOTE: deprecated parameter
"""
if you don't like the parameter and you will remove it in the future, you can mark it as deprecated.
"""


@app.get("/items_deprecated/")
async def read_item_deprecated(q: Annotated[str | None, Query(deprecated=True)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# NOTE: hidden query
"""
if you don't want to show the query parameter in swagger UI, you can use `include_in_schema=False`
"""


@app.get("/item_hidden_query/")
async def read_item_hidden_query(
    q: Annotated[str | None, Query(include_in_schema=False)],
):
    """
    in swagger UI you can not see the query parameter `q`
    cuz you set `include_in_schema=False`
    """
    if q:
        return {"q": q}
    else:
        return {"q": "no query"}


# NOTE: custom validation
"""
you can use a custom validator function that is applied after the normal validation
(e.g. after validating that the value is a str).

Note:
    Pydantic also has BeforeValidator and others. 🤓

Note:
    These custom validators are for things that can be checked with only the same data provided in the request.
    If you need to check external data (e.g. a database) you should use a custom dependency in the later section.
"""
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(( "isbn-", "imdb-" )):
        raise ValueError("Invalid ID.")
    return id


@app.get("/item_custom_validation/")
async def read_item_custom_validation(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

