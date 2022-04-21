from time import sleep
from functools import wraps, partial
import response
from src.constant.http_status_code import *

from flask import app,Blueprint,request,jsonify
from src.database import db,Menu,Ingredients
import validators
from src.decarator.decarator import decorator_dublicate
from flasgger import swag_from
menu = Blueprint("menu", __name__, url_prefix="/api/v1/menu")


@menu.post('/add')
@swag_from("./doc/menu/menu.yaml")
def add_menu():
    drink_name = request.json["drink_name"]
    cost = request.json["cost"]
    water = request.json["water"]
    milk = request.json["milk"]
    coffee = request.json["coffee"]

    if Menu.query.filter_by(drink_name=drink_name).first() is not None:
        return jsonify({'error': "Already  add drink name"}), HTTP_409_CONFLICT

    menu = Menu(drink_name=drink_name,cost=cost)
    db.session.add(menu)
    db.session.commit()
    ingredients = Ingredients(water=water, milk=milk, coffee=coffee, menu_id=menu.id)
    db.session.add(ingredients)
    db.session.commit()

    return jsonify({
        "message": "Add success",
        "menu":{
            "drink_name":drink_name,
             "cost":cost
        },
        "ingredients": {
            "water":water,
            "milk":milk,
            "coffee":coffee,
            "menu_id":menu.id
        }
    })
@menu.get("/allmenu")
@swag_from("./doc/menu/allmenu.yaml")
def get_menu():
    # mashmallow eklenecek
    menu = Menu.query.all()
    data = []
    for all_menu in menu:
        new_date = {
                "id": all_menu.id,
                "drink_name": all_menu.drink_name,
                "cost": all_menu.cost
            },
        data.append(new_date)

    return jsonify({"data": data}), HTTP_200_OK

@menu.get("/about/<int:id>")
def about(id):
    menu_about = Ingredients.query.filter_by(menu_id=id).first()
    if not menu_about:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    data = []
    for ingredients in menu_about.menu.ingredients:
        new_data = {
            "water": ingredients.water,
            "milk": ingredients.milk,
            "coffee":ingredients.coffee
        }
        data.append(new_data)
    return jsonify({
        "drink_name":menu_about.menu.drink_name,
        "cost": menu_about.menu.cost,
        "ingredients":data
    }),HTTP_200_OK


@menu.get("/hello2")
def say_hello():
    text = "helloo3"
    return  jsonify({"message": f"{text}"})
