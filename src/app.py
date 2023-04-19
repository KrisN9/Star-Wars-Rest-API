"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])  #se obtiene a todos los 'people'
def all_people():
    peoples=People.query.all()
    data=[people.serialize() for people in peoples]

    return jsonify(data), 200


@app.route('/people/<int:people_id>', methods=['GET']) # se obtiene 'people' por id 
def get_people(people_id):
    peoples= People.query.filter_by(id=people_id).first()
    if peoples : 
        return jsonify(peoples.serialize()),200
    
    return jsonify({"msg": "Doesn´t exist"})    


@app.route('/planet', methods=['GET'])     #se obtiene a todos los 'planet'
def all_planet():
    planets=Planet.query.all()
    data=[planet.serialize() for planet in planets]

    return jsonify(data), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])    # se obtiene 'planet' por id 
def get_planet(planet_id):
    planets= Planet.query.filter_by(id=planet_id).first()
    if planets : 
        return jsonify(planets.serialize()),200
    
    return jsonify({"msg": "Doesn´t exist"})

@app.route('/user', methods=['GET'])     #se obtiene todos los usuarios 
def all_user():
     users=User.query.all()
     data=[user.serialize() for user in users]

     return jsonify(data), 200

@app.route('/user/favorite/<int:user_id>', methods=['GET'])  #Listar todos los favoritos que pertenecen al usuario actual (modificar).
def favorite_user(user_id):                                             
    favorites= Favorite.query.all(id=user_id)
    data = [favorite.serialize() for favorite in favorites]
    return jsonify(data),200

@app.route('/favorite_planet', methods=['POST']) #añadir un nuevo 'planet' favorito (modificar).
def add_favorite_planet():

    data = request.json
    favoriteplanet = FavoritePlanet.query.filter_by(user_id=data['user_id'], planet_id=data['planet_id'])
    if favoriteplanet:
        return jsonify(data), 200

    return jsonify({"msg": "Your favorite cannot be added, wrong details"}), 400

@app.route('/favorite_people', methods=['POST']) #añadir un nuevo 'people' favorito (modificar).
def add_favorite_people():

    data = request.json
    favoritepeople = FavoritePeople.query.filter_by(user_id=data['user_id'], people_id=data['people_id'])
    if favoritepeople:
        return jsonify(data), 200

    return jsonify({"msg": "Your favorite cannot be added, wrong details"}), 400


@app.route('/delete_favorite_planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])      #emilinar 'planet' favorito del usuario actual (modificar).
def delete_favorite_planet(user_id, planet_id):
    try:
        removeFavoritePlanet=FavoritePlanet(id=planet_id)
        db.session.delete(removeFavorite)
        db.session.commit()
    except:
        return jsonify({"message": "Error"}),400

    return jsonify({"Favorite removed"})


@app.route('/delete_favorite_people/<int:user_id>/<int:people_id>', methods=['DELETE'])      #emilinar 'people' favorito del usuario actual (modificar).
def delete_favorite_people(user_id, people_id):
    try:
        removeFavoritePeople=FavoritePeople(id=people_id)
        db.session.delete(removeFavorite)
        db.session.commit()
    except:
        return jsonify({"message": "Error"}),400

    return jsonify({"Favorite removed"})


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
