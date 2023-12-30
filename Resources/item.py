from flask import request
from flask_smorest import abort, Blueprint
from uuid import uuid4
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from Model import Itemdb

blp  = Blueprint("item", __name__, description="Item related operations")

@blp.route("/item/<item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if item_id in items:
            return items[item_id]
        else:
            abort(404, message="Item not found")

    def delete(self, data, item_id):
        if item_id in items:
            del items[item_id]
            return {"message" : "Item deleted"}
        else:
            abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, item_id):
        if item_id in items:
            items[item_id] = data
            return {"message" : "Item updated"}
        else:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        new_item = Itemdb(**data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Internal server error")
        return new_item