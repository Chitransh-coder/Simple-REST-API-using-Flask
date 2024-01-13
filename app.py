from flask import Flask
import os
from db import db
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from Resources.item import blp as itemblp
from Resources.store import blp as storeblp
from Resources.tags import blp as tagblp
from Resources.user import blp as userblp

def create_app(db_uri=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.24.2"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["JWT_SECRET_KEY"] = "OP"

    db.init_app(app)
    JWTManager(app)


    with app.app_context():
        db.create_all()

    api = Api(app)

    api.register_blueprint(itemblp)
    api.register_blueprint(storeblp)
    api.register_blueprint(tagblp)
    api.register_blueprint(userblp)

    return app