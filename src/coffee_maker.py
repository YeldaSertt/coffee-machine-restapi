
from flask import app,Blueprint,request,jsonify
from src.database import Menu,Ingredients,Report,db
from src.constant.http_status_code import *
from functools import wraps, partial
from src.model.model import coffee_schemas,coffee_schema
from flasgger import swag_from
from src.decarator.decarator import enought_decorator

coffeemaker = Blueprint("coffeemaker", __name__, url_prefix="/api/v1/coffeemaker")

@coffeemaker.post("/make-coffee/<int:id>")
@enought_decorator
@swag_from("./doc/coffemake/coffeemake.yaml")
def make(id):

    if Menu.query.filter_by(id=id).first() is None:
        return jsonify({
            "message": f"Not found {request.json['drink_name']}"
        }),HTTP_404_NOT_FOUND

    report =  Report(coffee_id=id,drink_name=request.json["drink_name"],payment=0,water=request.json["water"],coffee=request.json["coffee"],milk=request.json["milk"])
    db.session.add(report)
    db.session.commit()

    new_post = Menu.query.filter_by(id=id).first()
    data = coffee_schema.dump(new_post)
    return jsonify(data,{"message":"Great ! Wait for payment 💸"}),HTTP_200_OK

@coffeemaker.post("/coffee-cost/<int:id>")
@enought_decorator
def cost(id):

    cost = request.json["cost"]
    query_report = Report.query.filter_by(coffee_id=id).first()
    query_report.payment = cost
    db.session.add(query_report)
    db.session.commit()

    query_ = Menu.query.filter_by(id=id).first()
    data = coffee_schema.dump(query_)

    if query_.cost < cost:
        new_cost = cost - query_.cost
        return jsonify(data, {"message": f" We don't forget to buy {new_cost} for your change.e ☕. Enjoy!"}), HTTP_200_OK

    return jsonify(data,{"message":f"Here is your {query_.drink_name} ☕. Enjoy!"}),HTTP_200_OK





