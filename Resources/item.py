from flask_smorest import abort, Blueprint
from flask.views import MethodView
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

    def delete(self, data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Delete not implemented")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, item_id):
        item = ItemModel.query.get(item_id)
        item.name = data["name"]
        item.price = data["price"]
        if item:
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                abort(500, message="Internal server error")
        else:
            item = ItemModel(id=item_id,**data)
            db.session.add(item)
            db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        new_item = ItemModel(**data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Internal server error")
        return new_item