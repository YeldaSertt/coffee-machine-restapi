from marshmallow import Schema, fields

class ReportSchema(Schema):

     drink_name = fields.String()
     payment = fields.Integer()
     water = fields.Integer()
     coffee = fields.Integer()
     milk = fields.Integer()

     def __repr__(self):

         return  f'Report : \n' \
               f'coffee-name : {self.drink_name} \n' \
               f'payment : {self.payment} \n' \
               f'water : {self.water} \n' \
               f'coffee : {self.coffee} \n' \
               f'milk : {self.milk} \n' \
               ''

report_schema = ReportSchema()
report_schemas = ReportSchema(many=True)