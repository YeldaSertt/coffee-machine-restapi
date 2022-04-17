from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Menu(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    drink_name = db.Column(db.String(80),nullable=False)
    cost = db.Column(db.Integer,nullable=False)
    ingredients = db.relationship('Ingredients', backref="menu")

    def __repr__(self):
        return f'Menu =>> {self.drink_name} ,{self.cost}, {self.ingredients}'


class Ingredients(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    water = db.Column(db.Integer,nullable=False)
    coffee = db.Column(db.Integer, nullable=False)
    milk = db.Column(db.Integer, nullable=False)
    menu_id = db.Column(db.Integer,db.ForeignKey("menu.id"))


    def __repr__(self):
        return f'Ingredients =>> {self.coffee},{self.water},{self.milk},{self.menu_id}'

class User(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(80),nullable=False)
    password = db.Column(db.Text(),nullable=False)
    report = db.relationship('Report', backref="report")

    def __repr__(self):
        return f'User =>> {self.name}'

class Report(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    coffee_id = db.Column(db.String,nullable=False)
    drink_name = db.Column(db.String,nullable=False)
    payment = db.Column(db.Integer, nullable=True)
    water = db.Column(db.Integer,nullable=False)
    coffee = db.Column(db.Integer, nullable=False)
    milk = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Report ==>> ' \
               f'coffee-id : {self.coffee_id} ,' \
               f'coffee-name : {self.drink_name} ,' \
               f'payment : {self.payment} ,' \
               f'water : {self.water} ,' \
               f'coffee : {self.coffee} ,' \
               f'milk : {self.milk} ' \
               ')'
