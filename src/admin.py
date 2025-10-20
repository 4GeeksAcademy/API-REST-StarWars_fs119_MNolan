import os
from flask_admin import Admin
from models import db, User, Characters, FavouriteCharacters, Planet, FavouritePlanets, Starship, FavouriteStarships
from flask_admin.contrib.sqla import ModelView

class UsersModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id','email', 'password', 'is_active', 'char_favourites', 'plan_favourites', 'star_favourites' ]

class CharactersModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id', 'name', 'height', 'weight', 'affiliations','favourites_by' ]

class FavouriteCharactersModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id', 'users_id', 'users', 'character_id', 'people' ]

class PlanetModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id', 'name', 'extension', 'population', 'locations', 'climate', 'species', 'affiliations', 'favourites_by' ]

class FavouritePlanetsModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id', 'users_id', 'users', 'planet_id', 'planets' ]

class StarshipModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id', 'name', 'model', 'dimensions', 'velocity', 'hiperspace', 'affiliations', 'favourites_by' ]

class FavouriteStarshipsModelView(ModelView):
    column_auto_select_related = True #Cargar las relaciones
    column_list = ['id', 'users_id', 'users', 'starship_id', 'starships' ]



def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UsersModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(FavouriteCharactersModelView(FavouriteCharacters, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(FavouritePlanetsModelView(FavouritePlanets, db.session))
    admin.add_view(StarshipModelView(Starship, db.session))
    admin.add_view(FavouriteStarshipsModelView(FavouriteStarships, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(YourClassModelView(YourModelName, db.session))