from flask import app,Blueprint,request,jsonify
from src.database import Menu,Ingredients,Report,db
from src.constant.http_status_code import *
from functools import wraps, partial
from werkzeug.utils import secure_filename
import os
from src.model.model import coffee_schemas,coffee_schema
from flasgger import swag_from


def enought_decorator(function):
    @wraps(function)
    def decorator_ingredients(*args,**kwargs):
        _ = function(*args,**kwargs)
        try:
            for item in Menu.query.filter_by(drink_name=request.json["drink_name"]).first().ingredients:

                if item.water < request.json["water"]:
                    return jsonify({"message":f"Sorry there is not enough water {item.water}"})
                elif item.milk < request.json["milk"]:
                    return jsonify({"message":f"Sorry there is not enough milk {item.milk}"})
                elif item.coffee < request.json["coffee"]:
                    return jsonify({"message":f"Sorry there is not enough coffee: {item.coffee}"})

            if Menu.query.filter_by(id=kwargs["id"]).first().cost > request.json["cost"]:
                return jsonify({"message":f"Sorry that's not enough money. Money refunded. Cost: {Menu.query.filter_by(id=id).first().cost}"})
        except:
            pass
        return _

    return decorator_ingredients


def decorator_dublicate(function):
    @wraps(function)
    def dublicate_control_decorator(*args,**kwargs):
        _ = function(*args,**kwargs)
        drink_name = request.json["drink_name"]
        for name in Menu.query.all():
            if drink_name == name.drink_name:
                print("-5")
                return jsonify({"message":"burdaa"})
        return _

    return dublicate_control_decorator

def decorator_image(function):
    @wraps(function)
    def allowed_file(*args,**kwargs):
        if "file" not in request.files:
            return jsonify({"message": "Not found files"}), HTTP_404_NOT_FOUND
        elif request.files["file"].filename == "":
            return  jsonify({"message": "İmage nor found"}),HTTP_404_NOT_FOUND
        else:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.environ.get("UPLOAD_FOLDER"), filename))
            #print('upload_image filename: ' + filename)
            #return  jsonify({"message":"Image successfully uploaded and displayed below", "filename":filename })
        return function(*args,**kwargs)

    return allowed_file