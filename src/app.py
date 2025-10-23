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
from models import db, User, Characters, FavouriteCharacters, Planet, FavouritePlanets, Starship, FavouriteStarships
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

@app.route('/users', methods=['GET']) #GET all users
def get_all_users():
    users = User.query.all() #SELECT * FROM 'user';
    #print(users) #[Usuario mrnolan88@gmail.com, Usuario HELVIDSALA@GMAIL.COM, Usuario jorge@gmail.com, Usuario laura@msn.com, Usuario lauradds@msn.com]
    users_serialized = [] #creamos un objeto user_serialized
    for user in users:  
        users_serialized.append(user.serialize()) #aplicamos ciclo for para devolver todos los usuarios
   # user1 = users[0].serialize()
    #print(user1) # <- Esto SI es un diccionario y se puede convertir a JSON
    
    response_body = {
        'msg': "Hello, this is your GET /user response ",
        'users': users_serialized
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
   
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
   
    return jsonify({'user': user.serialize()}), 200

@app.route('/user', methods=['POST']) #POST user
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'El campo email es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'El campo password es obligatorio'}), 400
    print(body)

    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    print(new_user)
    print(type(new_user))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'Usuario regiatrado', 'user': new_user.serialize()}), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    body = request.get_jason(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    user.nick = body.get('name', user.nick)
    user.email = body.get('email', user.email)
    user.password = body.get('password', user.password)
    user.is_active = body.get('is_active', user.is_active)
    

    db.session.commit()
    return jsonify({'msg': f'El usuario {user_id} ha sido actualizado con exito', 'user': user.serialize()}), 200


@app.routes('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'El usuario ha sido eliminado con exito'}), 200




@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())

    response_body = {
        'msg': "Hello this is your GET /characters response",
        'characters': characters_serialized
    }
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
   
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'El personaje con id {character_id} no existe'}), 404
   
    return jsonify({'character': character.serialize()}), 200

@app.route('/character', methods=['POST']) 
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'El campo name es obligatorio'}), 400
    print(body)

    new_character = Characters()
    new_character.name = body.get('name')
    print(new_character)
    print(type(new_character))
    new_character.height = body.get('height') 
    new_character.weight = body.get('weight') 
    new_character.affiliations = body.get('affiliations') 
    
    db.session.add(new_character)
    db.session.commit()

    return jsonify({'msg': 'personaje regiatrado', 'personaje': new_character.serialize()}), 200


@app.route('/character/<int:character _id>', methods=['PUT'])
def update_character(character_id):
    body = request.get_jason(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'El personaje con id {character_id} no existe'}), 404
    character.name = body.get('name', character.name)
    character.height = body.get('height', character.height)
    character.weight = body.get('weight', character.weight)
    character.affiliations = body.get('affiliations', character.affiliations)

    db.session.commit()
    return jsonify({'msg': f'El personaje {character_id} ha sido actualizado con exito', 'character': character.serialize()}), 200


@app.routes('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'El personaje con id {character_id} no existe'}), 404
    
    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': 'El personaje ha sido eliminado con exito'}), 200




@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
   
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'El planeta con id {planet_id} no existe'}), 404
   
    return jsonify({'planet': planet.serialize()}), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())

    response_body = {
        'msg': "Hello this is your GET /planets response",
        'planets': planets_serialized
    }
    return jsonify(response_body), 200


@app.route('/planet', methods=['POST']) 
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'El campo name es obligatorio'}), 400
    print(body)

    new_planet = Planet()
    new_planet.name = body['name']
    print(new_planet)
    print(type(new_planet))
    new_planet.extension = body.get('extension') 
    new_planet.population = body.get('population') 
    new_planet.locations = body.get('locations') 
    new_planet.climate = body.get('climate') 
    new_planet.species = body.get('species') 
    new_planet.affiliations = body.get('affiliations') 
    
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'msg': 'Planeta regiatrado', 'planeta': new_planet.serialize()}), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_jason(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'El planeta con id {planet_id} no existe'}), 404
    planet.name = body.get('name', planet.name)
    planet.extension = body.get('extension', planet.extension)
    planet.population = body.get('population', planet.population)
    planet.locations = body.get('locations', planet.locations)
    planet.climate = body.get('climate', planet.climate)
    planet.species = body.get('species', planet.species)
    planet.affiliations = body.get('affiliations', planet.affiliations)

    db.session.commit()
    return jsonify({'msg': f'El planeta {planet_id} ha sido actualizado con exito', 'planet': planet.serialize()}), 200


@app.routes('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'El planeta con id {planet_id} no existe'}), 404
    
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'El planeta ha sido eliminado con exito'}), 200



@app.route('/starships', methods=['GET'])
def get_all_starsips():
    starships = Starship.query.all()
    starships_serialized =[]
    for starship in starships:
        starships_serialized.append(starship.serialize())

    response_body = {
        'msg': "Hello this is your GET /starships response",
        'starships': starships_serialized
    }    
    return jsonify(response_body), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):

    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': f'La starship con id {starship_id} no existe'}), 404

    return jsonify({'starship': starship.serialize()}), 200


@app.route('/starship', methods=['POST']) 
def add_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'El campo name es obligatorio'}), 400
    print(body)

    new_starship = Starship()
    new_starship.name = body['name']
    
    new_starship.model = body.get('model') 
    new_starship.dimensions = body.get('dimensions') 
    new_starship.velocity = body.get('velocity') 
    new_starship.hiperspace = body.get('hiperspace') 
    new_starship.affiliations = body.get('affiliations') 
    
    db.session.add(new_starship)
    db.session.commit()

    return jsonify({'msg': 'Nave regiatrada', 'starship': new_starship.serialize()}), 200


@app.route('/starship/<int:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    body = request.get_jason(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': f'La nave con id {starship_id} no existe'}), 404
    starship.name = body.get('name', starship.name)
    starship.model = body.get('model', starship.model)
    starship.dimensions = body.get('dimensions', starship.dimensions)
    starship.velocity = body.get('velocity', starship.velocity)
    starship.hiperspace = body.get('hiperspace', starship.hiperspace)
    starship.affiliations = body.get('affiliations', starship.affiliations)

    db.session.commit()
    return jsonify({'msg': f'La nave {starship_id} ha sido actualizado con exito', 'starship': starship.serialize()}), 200


@app.routes('/starship/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': f'La nave con id {starship_id} no existe'}), 404
    
    db.session.delete(starship)
    db.session.commit()
    return jsonify({'msg': 'La nave ha sido eliminado con exito'}), 200




@app.route('/user_fav_char/<int:user_id>', methods = ['GET']) # GET Favourite Character By user
def get_fav_char(user_id):
    user = User.query.get(user_id)
    print(user) # Si el query no encuentra el usuario devuelve None
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    characters_favoritos = user.char_favourites  #<- Esto es una lista de registro en la lista FavouriteCharacters
    favourite_characters_serialized = []
    for registro in characters_favoritos:
        character = registro.people.serialize()
        favourite_characters_serialized.append(character)
    #print(characters_favoritos)
    #print(characters_favoritos[0].people.serialize())
    return jsonify({'msg': 'Todo salio bien', \
                    'favourite characters': favourite_characters_serialized,\
                    'user': user.serialize()}), 200


@app.route('/user_fav_char/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_fav_char(user_id, character_id):
       
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
   
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'El character con id {character_id} no existe'}), 404

    existing_fav_char = FavouriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first() 
    if existing_fav_char:
        return jsonify({'msg':'El personaje ya esta en favoritos' }), 400
    
    new_fav_char = FavouriteCharacters(user_id = user_id, character_id = character_id)
    
    db.session.add(new_fav_char)
    db.session.commit()

    return jsonify({'msg': 'Nuevo character favorito regiatrado', 
                    'user': user.serialize(), 
                    'character': character.serialize()}), 200


@app.route('/user_fav_char/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def delete_fav_char(user_id, character_id):
    favourite = FavouriteCharacters.query.filter_by(user_id = user_id, character_id = character_id).first()
    if favourite is None:
        return jsonify({'msg': 'Este personaje no pertenece a favoritos'}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({'msg': 'Personaje eliminado de favoritos'}), 200




@app.route('/user_fav_plan/<int:user_id>', methods=['GET']) # GET Favourite Planet By user
def get_fav_plan(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    planetas_favoritos = user.plan_favourites
    favourite_planets_serialized = []
    for registro in planetas_favoritos:
        planeta = registro.planets.serialize()
        favourite_planets_serialized.append(planeta)

    return jsonify({'msg': 'Todo salio bien', \
                    'favourite planets': favourite_planets_serialized, \
                        'user': user.serialize()}), 200


@app.route('/user_fav_plan/<int:user_id>/planets/<int:planet_id>', methods=['POST'])
def add_fav_plan(user_id, planet_id):
       
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
   
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'El planeta con id {planet_id} no existe'}), 404

    existing_fav_plan = FavouritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first() 
    if existing_fav_plan:
        return jsonify({'msg':'El planeta ya esta en favoritos' }), 400
    
    new_fav_plan = FavouritePlanets(user_id = user_id, planet_id = planet_id)
    
    db.session.add(new_fav_plan)
    db.session.commit()

    return jsonify({'msg': 'Nuevo planeta favorito regiatrado', 
                    'user': user.serialize(), 
                    'planet': planet.serialize()}), 200

@app.route('/user_fav_plan/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_plan(user_id, planet_id):
    favourite = FavouritePlanets.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if favourite is None:
        return jsonify({'msg': 'Este planeta no pertenece a favoritos'}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({'msg': 'Planeta eliminado de favoritos'}), 200




@app.route('/user_fav_star/<int:user_id>', methods=['GET']) # GET Favourite Starship By user
def get_fav_star(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    naves_favoritas = user.star_favourites
    favourite_starships_serialized = []
    for registro in naves_favoritas:
        nave = registro.starships.serialize()
        favourite_starships_serialized.append(nave)

    return jsonify({'msg': 'Todo salio bien', \
                    'favourite starships': favourite_starships_serialized, \
                        'user': user.serialize()}), 200


@app.route('/user_fav_star/<int:user_id>/starship/<int:starship_id>', methods=['POST'])
def add_fav_star(user_id, starship_id):
       
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
   
    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': f'La nave con id {starship_id} no existe'}), 404

    existing_fav_star = FavouriteStarships.query.filter_by(user_id=user_id, starship_id=starship_id).first() 
    if existing_fav_star:
        return jsonify({'msg':'Esta nave ya esta en favoritos' }), 400
    
    new_fav_star = FavouriteStarships(user_id = user_id, starship_id = starship_id)
    
    db.session.add(new_fav_star)
    db.session.commit()

    return jsonify({'msg': 'Nueva nave favorita regiatrado', 
                    'user': user.serialize(), 
                    'starship': starship.serialize()}), 200


@app.route('/user_fav_star/<int:user_id>/starship/<int:starship_id>', methods=['DELETE'])
def delete_fav_star(user_id, starship_id):
    favourite = FavouriteStarships.query.filter_by(user_id = user_id, starship_id = starship_id).first()
    if favourite is None:
        return jsonify({'msg': 'Esta nave no pertenece a favoritos'}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({'msg': 'Nave eliminada de favoritos'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
