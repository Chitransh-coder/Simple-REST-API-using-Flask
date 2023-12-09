from flask import Flask, request
from flask_smorest import abort
from db import items, stores
from uuid import uuid4

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores" : list(stores.values())}

@app.post("/store")
def create_store():
    data = request.get_json()
    if "name" not in data:
        abort(400, message="Ensure \"name\" is provided")
    for s in stores.values():
        if s["name"] == data["name"]:
            abort(409, message="Store already exists")
    snid = uuid4().hex
    new_store = {
        **data, "id" : snid
    }
    stores[snid] = new_store
    return new_store, 201


@app.get("/store/<store_id>")
def get_store(store_id):
    if store_id in stores:
        return stores[store_id]
    else:
        abort(404, message="Store not found")


@app.delete("/store/<store_id>")
def delete_store(store_id):
    if store_id in stores:
        del stores[store_id]
        return {"message" : "Store deleted"}
    else:
        abort(404, message="Store not found")

@app.get("/item")
def get_items():
    return {"items" : list(items.values())}

@app.post("/item")
def create_item_in_store():
    data = request.get_json()
    if "name" not in data or "price" not in data or "store_id" not in data:
        abort(400, message="Ensure \"name\", \"price\", and \"store_id\" are provided")
    if data["store_id"] not in stores:
        abort (404, message="Store not found")
    for i in items.values():
        if i["name"] == data["name"] and i["store_id"] == data["store_id"]:
            abort(409, message="Item already exists in store")
    inid = uuid4().hex
    new_item = {
        **data, "id" : inid
    }
    items[inid] = new_item
    return new_item, 201

@app.get("/item/<item_id>")
def get_items_in_store(item_id):
    if item_id in items:
        return items[item_id]
    else:
        abort(404, message="Item not found")


@app.delete("/item/<item_id>")
def delete_item(item_id):
    data = request.get_json()
    if "name" not in data or "price" not in data or "store_id" not in data:
        abort(400, message="Ensure \"name\", \"price\", and \"store_id\" are provided")
    if item_id in items:
        del items[item_id]
        return {"message" : "Item deleted"}
    else:
        abort(404, message="Item not found")

@app.put("/item/<item_id>")
def update_item(item_id):
    data = request.get_json()
    if "name" not in data or "price" not in data or "store_id" not in data:
        abort(400, message="Ensure \"name\", \"price\", and \"store_id\" are provided")
    if item_id in items:
        items[item_id] = data
        return {"message" : "Item updated"}
    else:
        abort(404, message="Item not found")