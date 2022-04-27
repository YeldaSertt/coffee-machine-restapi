from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
import os
from src.menu import menu
from src.coffee_maker import coffeemaker
from src.admin import  admin
from flask_marshmallow import Marshmallow
from src.database import db
from src.confing.swagger import swagger_config,template
from .report import *
from flasgger import Swagger




def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER"),
            SWAGGER={
                'title': "Coffe-Machine API",
                'uiversion': 3
            }

        )
    else:
        app.config.from_mapping(test_config)

    Swagger(app, config=swagger_config, template=template)

    app.register_blueprint(menu)
    app.register_blueprint(coffeemaker)
    app.register_blueprint(admin)

    app.db = app
    db.init_app(app)
    Marshmallow(app)
    JWTManager(app)

    @app.route("/hello")
    def say_hello():
        text = "helloo2"
        return jsonify({"message": f"{text}"})

    return app



