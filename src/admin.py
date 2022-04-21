from flask import app,Blueprint,request,jsonify
from src.database import User
from src.database import Report
from flask_jwt_extended import create_access_token ,create_refresh_token ,jwt_required ,get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from src.constant.http_status_code import *
from src.model.report_model import report_schema
from flasgger import swag_from



admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


@admin.post("/login")
@swag_from("./doc/user/login.yaml")
def login():
    name = request.json["name"]
    password =  request.json["password"]
    pwd_hash = generate_password_hash(password)

    admin = User.query.filter_by(name=name).first()
    if admin:
        is_pass_correct = check_password_hash(admin.password,password)
        print(is_pass_correct)
        if is_pass_correct:
            access = create_access_token(admin.id)

            return jsonify(
                {
                    "access" : access,
                    "username" : admin.name,
                }
            ),HTTP_200_OK

        else:
            return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED

@admin.get("/me")
@jwt_required()
@swag_from("./doc/user/me.yaml")
def me():
    user_id = get_jwt_identity()
    print(user_id)
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "username" : user.name,
    }),HTTP_200_OK


@admin.get("/report")
@jwt_required()
@swag_from("./doc/user/report.yaml")
def report():

    reports = Report.query.all()
    data = []
    for item in reports:
        new_link = report_schema.dump(item)
        data.append(new_link)

    return jsonify({"message":"Succes Report","data": data}),HTTP_200_OK



