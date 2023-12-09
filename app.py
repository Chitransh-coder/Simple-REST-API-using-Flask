from flask import Flask, request
from db import items, stores
from uuid import uuid4

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores" : list(stores.values())}

@app.post("/store")
def create_store():
    data = request.get_json()
    snid = uuid4().hex
    new_store = {
        **data, "id" : snid
    }
    stores[snid] = new_store
    return new_store, 201

@app.post("/item")
def create_item_in_store():
    data = request.get_json()
    if data["store_id"] not in stores:
        return {"message" : "Store not found"}, 404
    inid = uuid4().hex
    new_item = {
        **data, "id" : inid
    }
    items[inid] = new_item
    return new_item, 201

@app.get("/store/<store_id>")
def get_store(store_id):
    if store_id in stores:
        return stores[store_id]
    else:
        return {"message" : "Store not found"}, 404

@app.get("/item/<item_id>")
def get_items_in_store(item_id):
    if item_id in items:
        return items[item_id]
    else:
        return {"message" : "Item not found"}, 404