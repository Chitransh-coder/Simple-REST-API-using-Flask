from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from Model import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("Tags", "tags", description="Tags related endpoints")

@blp.route("/store/<int:store_id>/tag")
class Tag_in_Store(MethodView):

    @blp.response(200,TagSchema(many=True))
    def get_tags(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()


    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, new_tag, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id and TagModel.name == new_tag["name"]).first():
            abort(400, message="Tag already exists")
        tag = TagModel(**new_tag, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e.__dict__['orig']))

        return tag

    @blp.route("/<int:tag_id>")
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag