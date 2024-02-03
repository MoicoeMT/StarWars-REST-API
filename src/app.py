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
from models import db, User, People, Favorit, Planets
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

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all() #trae todos los usuarios de la base de datos
    return jsonify({'users': [user.serialize() for user in users]})

@app.route('/users/favorite/<int:user_id>', methods=['GET'])
def get_all_favorites(user_id):
    users = Favorit.query.filter_by(user_id = user_id)
    return jsonify({'user': [favorite.serialize() for favorite in users]})

# EVERYTHING FOR PEOPLE ////////////////////////////////////////
    # TRAE TODOS LOS PERSONAJES DE LA BASE
@app.route('/people', methods=['GET'])
def get_people():
    resp = People.query.all()
    return jsonify({'people': [people.serialize() for people in resp]})

# TRAE LOS PERSONAJES POR ID DE LA BASE
@app.route('/people/<int:people_id>', methods=['GET'])
def get_PeopleById(people_id):
    resp = People.query.filter_by(id = people_id).one_or_none()
    if resp is None:
        return "People is not found"
    return jsonify({'people': [resp.serialize()]}),201

# # AGREGA A FAVORITOS
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorite(people_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = User.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return jsonify({'error': 'Usuario No encontrado'}),404
        resp = People.query.filter_by(id = people_id).one_or_none()
        if resp is None:
            return jsonify({'error': 'No encontrado'}),404
        
        new_favorit=Favorit(user_id=user_id, people_id=people_id)
        db.session.add(new_favorit)
        try:
            db.session.commit()
            return "favorite Created"
        except Exception as error:
            db.session.rollback()
            print("//////////////////////", error)
            return "An error ocurred"

# EVERYTHING FOR PLANETS ////////////////////////////////////////

#TRAE TODOS LOS PLANETAS
@app.route('/planets', methods=['GET'])
def get_planets():
    resp = Planets.query.all()
    return jsonify({'planets': [planets.serialize() for planets in resp]})

# TRAE LOS PLANETAS POR ID
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_by_id(planets_id):
    resp = Planets.query.filter_by(id = planets_id).one_or_none()
    # if resp is None:
    #     return "Planet is not found"
    return jsonify({'planets': [resp.serialize()]}), 201

# AGREGA A FAVORITOS
@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def add_planets_to_favorite(planets_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = User.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return jsonify({'error': 'Usuario No encontrado'}),404
        resp = Planets.query.filter_by(id = planets_id).one_or_none()
        if resp is None:
            return jsonify({'error': 'No encontrado'}),404
        
        new_favorit=Favorit(user_id=user_id, planet_id=planets_id)
        db.session.add(new_favorit)
        try:
            db.session.commit()
            return "favorite Created"
        except Exception as error:
            db.session.rollback()
            print("//////////////////////", error)
            return "An error ocurred", 404
        
#  METODOS DELETE POR ID

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet_from_favorite(planet_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = User.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return 'user is not found', 404
       
        resp = Favorit.query.filter_by(user_id = user_id, planet_id = planet_id).all()
        if not resp:
            return 'planet is not found', 404
        
        for resp_unit in resp:
            db.session.delete(resp_unit)
        try:
            db.session.commit()
            return "Favorit is Deleted", 200
        except Exception as error:
            return "an error as ocurred", 404
        
        
        
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_from_favorite(people_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = User.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return 'user is not found', 404
       
        resp = Favorit.query.filter_by(user_id = user_id, people_id = people_id).all()
        if not resp:
            return 'people is not found', 404
        
        for resp_unit in resp:
            db.session.delete(resp_unit)
        try:
            db.session.commit()
            return "Favorit is Deleted", 200
        except Exception as error:
            return "an error as ocurred", 404       

        
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
