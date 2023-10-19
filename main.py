from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senac2021@localhost:3306/todo'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class PetShopAnimal(db.Model):
   __tablename__ = "pet_shop_animal"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   age = db.Column(db.number(20))
   service = db.column(db.String(100))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, name, age, service):
       self.name = name
       self.age = age
       self.service = service

   def __repr__(self):
       return f"{self.id}"

class PetShopAnimalSchema(ma.Schema):
   class Meta(ma.Schema.Meta):
       model = PetShopAnimal
       sqla_session = db.session
   id = fields.Number(dump_only=True)
   name = fields.String(required=True)
   age = fields.Number(required=True)

@app.route('/api/v1/pet-shop-animal', methods=['POST'])
def create_todo():
   data = request.get_json()
   pet_shop_animal_schema = PetShopAnimalSchema()
   pet_shope_animal =  pet_shop_animal_schema.load(data)
   result =  pet_shop_animal_schema.dump(pet_shope_animal.create())
   return make_response(jsonify({"pet_shop_animal": result}), 200)

@app.route('/api/v1/pet-shop-animal', methods=['GET'])
def index():
   get_pet_shop_animal = PetShopAnimal.query.all()
   pet_shop_animal_schema =  PetShopAnimalSchema(many=True)
   all_animals = pet_shop_animal_schema.dump(get_pet_shop_animal)
   return make_response(jsonify({"animais": all_animals}))

@app.route('/api/v1/pet-shop-animal/<id>', methods=['GET'])
def get_pet_shop_animal_by_id(id):
   get_pet_shop_animal = PetShopAnimal.query.get(id)
   pet_shop_animal_schema = PetShopAnimalSchema()
   all_animals = pet_shop_animal_schema.dump(get_pet_shop_animal)
   return make_response(jsonify({"Animais": all_animals}))

@app.route('/api/v1/todo/<id>', methods=['PUT'])
def update_pet_shop_animal_by_id(id):
   data = request.get_json()
   get_pet_shop_animal = PetShopAnimal.query.get(id)
   if data.get('id'):
        get_pet_shop_animal.id = data['id']
   if data.get('name'):
        get_pet_shop_animal.name = data['name']
   if data.get('age'):
       get_pet_shop_animal.age = data['age']
   if data.get('service'):
       get_pet_shop_animal.service = data['service']
   db.session.add(get_pet_shop_animal)
   db.session.commit()
   pet_shop_animal = PetShopAnimalSchema(only=['id', 'name', 'age', 'service'])
   animals = pet_shop_animal.dump(get_pet_shop_animal)

   return make_response(jsonify({"Animais": animals}))

@app.route('/api/v1/todo/<id>', methods=['DELETE'])
def delete_todo_by_id(id):
   get_pet_shop_animal = PetShopAnimal.query.get(id)
   db.session.delete(get_pet_shop_animal)
   db.session.commit()
   return make_response("", 204)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

