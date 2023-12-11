from flask import request
from flask_smorest import abort, Blueprint
from db import items, stores
from uuid import uuid4
from flask.views import MethodView

from schemas import StoreSchema

blp  = Blueprint("store", __name__, description="Store related operations")

@blp.route("/store/<store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        if store_id in stores:
            return stores[store_id]
        else:
            abort(404, message="Store not found")
    
    def delete(self, store_id):
        if store_id in stores:
            del stores[store_id]
            return {"message" : "Store deleted"}
        else:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"stores" : list(stores.values())}
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        for s in stores.values():
            if s["name"] == data["name"]:
                abort(409, message="Store already exists")
        snid = uuid4().hex
        new_store = {
        **data, "id" : snid
    }
        stores[snid] = new_store
        return new_store, 201