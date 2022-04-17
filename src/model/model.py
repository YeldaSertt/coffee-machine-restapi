from marshmallow import Schema, fields

class CoffeeSchema(Schema):
     id = fields.Integer()
     drink_name = fields.String()
     cost = fields.Integer()

     def __repr__(self):
         return f"id : {self.id} drinkname : {self.drink_name} cost : {self.cost}"

coffee_schema = CoffeeSchema()
coffee_schemas = CoffeeSchema(many=True)

