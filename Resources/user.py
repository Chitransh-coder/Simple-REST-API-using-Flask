from sqlite3 import IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from Model import UserModel
from schemas import UserSchema

blp = Blueprint("users", "users", url_prefix="/users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, userData):
        user = UserModel(
            username=userData["username"],
            password=pbkdf2_sha256.hash(userData["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="User with that username already exists")
        except:
            abort(500, "Something went wrong")
        return {"message": "User created successfully"}, 201

@blp.route("/user/<int:id>")
class UserModel(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
        user = UserModel.query.get_or_404(id)
        if not user:
            abort(404, message="User not found")
        return user

    @blp.response(200, UserSchema)
    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200