from sqlite3 import IntegrityError
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from Model import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema

blp  = Blueprint("store", __name__, description="Store related operations")

@blp.route("/store/<store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, storedata):
        store = StoreModel(**storedata)

        try:
            db.session.add(store)
            db.session.commit()

        except IntegrityError as e:
            abort(400, message="Store already exists")
        except SQLAlchemyError as e:
            abort(500, message="Internal server error")
        return store