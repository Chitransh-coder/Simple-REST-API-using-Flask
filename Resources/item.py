from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from Model import ItemModel

blp  = Blueprint("item", __name__, description="Item related operations")

@blp.route("/item/<item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    @jwt_required()
    def delete(self, data, item_id):
        claims = get_jwt()
        if not claims["is_admin"]:
            abort(403, message="Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = data["price"]
            item.name = data["name"]
        else:
            item = ItemModel(id=item_id, **data)

        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @jwt_required()
    @blp.response(201, ItemSchema)
    def post(self, data):
        new_item = ItemModel(**data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Internal server error")
        return new_item