from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from Model import TagModel, StoreModel, ItemModel
from schemas import TagSchema, ItemAndTagSchema

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

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTag(MethodView):
    @blp.response(200, ItemAndTagSchema)
    def post(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        if tag in item.tags:
            abort(400, message="Tag already linked to item")

        try:
            item.tags.append(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e.__dict__['orig']))

        return {"msg": "Tag linked to item", "tag": tag, "item": item}

    @blp.response(200, ItemAndTagSchema)
    def delete(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        if tag not in item.tags:
            abort(400, message="Tag not linked to item")

        try:
            item.tags.remove(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e.__dict__['orig']))

        return {"msg": "Tag unlinked from item", "tag": tag, "item": item}

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag

    @blp.response(202, TagSchema)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e.__dict__['orig']))

        return tag