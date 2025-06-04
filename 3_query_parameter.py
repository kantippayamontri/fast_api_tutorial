from fastapi import FastAPI

app = FastAPI()

fake_items_db = list(
    {
        "id": i,
        "name": f"Item {i}",
        "description": f"Description for item {i}",
        "price": round(10 + i * 0.5, 2),
        "is_available": i % 3 != 0,
        "category": ["electronics", "clothing", "food", "books", "toys"][i % 5],
        "rating": round(3 + (i % 5) * 0.5, 1),
        "created_at": f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
    }
    for i in range(0, 100)
)


# NOTE: query parameters
@app.get("/items/")
async def read_item(
    skip: int = 0, limit: int = 10
):  # skip and limit are query parameters
    # return fake_items_db
    """
    http://localhost:8000/items/?skip=30 ( pass only skip )
    http://localhost:8000/items/?limit=20 ( pass only limit )
    http://localhost:8000/items/?skip=10&limit=1000 ( pass both skip and limit )
    """
    return list(
        item
        for item in fake_items_db
        if item["id"] >= skip and item["id"] < skip + limit
    )


# NOTE: optional parameters
@app.get("/items/{item_id}")
async def read_items(
    item_id: int, q: str | None = None, short: bool = False
):  # q and short is optional parameter
    """
    you can declare optional query parameters, by setting their default to None
    and you can pass boolean value in query parameter

    http://localhost:8000/items/20?short=True&&q=hahahaha
    http://localhost:8000/items/20?short=False&&q=hahahaha
    http://localhost:8000/items/20?short=False
    http://localhost:8000/items/20?q=False%20naja%20eiei
    """
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return {"item": item}


# NOTE: multipath and query parameter
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: int, q: str | None = None, short: bool = False
):
    """
    http://localhost:8000/users/99/items/50
    http://localhost:8000/users/99/items/50?q=this%20is%20query%20parameter
    """
    item = {"item_id": item_id, "own_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# NOTE: required query parameter
@app.get("/item_query/{item_id}")
async def read_user_query_item(item_id: int, needy: str):
    """
    ✅ http://localhost:8000/item_query/55?needy=asdfadsf #you pass needy
    ❌ http://localhost:8000/item_query/55 # you need to pass needy query parameter
    """
    item = filter(
        lambda item: item["id"] == item_id, fake_items_db
    )  # get filter iterator
    item = list(item)[0]  # convert to list and get first element
    return {"item": item, "needy": needy}


if __name__ == "__main__":
    item = filter(lambda item: item["id"] == 12, fake_items_db)
    item = list(item)[0]
    # item = item[0]
    print(item)
