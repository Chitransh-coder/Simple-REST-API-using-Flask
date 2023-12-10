from flask import request
from flask_smorest import abort, Blueprint
from db import items, stores
from uuid import uuid4
from flask.views import MethodView

blp  = Blueprint("item", __name__, description="Item related operations")

@blp.route("/item/<item_id>")
class Item(MethodView):
    def get(self, item_id):
        if item_id in items:
            return items[item_id]
        else:
            abort(404, message="Item not found")
    
    def delete(self, item_id):
        data = request.get_json()
        if "name" not in data or "price" not in data or "store_id" not in data:
            abort(400, message="Ensure \"name\", \"price\", and \"store_id\" are provided")
        if item_id in items:
            del items[item_id]
            return {"message" : "Item deleted"}
        else:
            abort(404, message="Item not found")

    def put(self, item_id):
        data = request.get_json()
        if "name" not in data or "price" not in data or "store_id" not in data:
            abort(400, message="Ensure \"name\", \"price\", and \"store_id\" are provided")
        if item_id in items:
            items[item_id] = data
            return {"message" : "Item updated"}
        else:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items" : list(items.values())}
    def post(self):
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