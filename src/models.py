from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#Para usar reset_migrations si da fallo $pipenv run migrate abrir bash: $ bash  /workspaces/API-REST-StarWars_fs119_MNolan/docs/assets/reset_migrations.bash

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(90), unique=True, nullable=False )
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    char_favourites: Mapped[list['FavouriteCharacters']
                      ] = relationship(back_populates ='users')
    plan_favourites: Mapped[list['FavouritePlanets']] = relationship(back_populates='users')
    star_favourites: Mapped[list['FavouriteStarships']] = relationship(back_populates='users')

    def __repr__(self):
        return f'Usuario {self.nick}'
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            #Nunca serializar el password
            "password": self.password, #Ahora serializo el password como prueba
            "is active": self.is_active,
            
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=True )
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    affiliations: Mapped[str] = mapped_column(String(20), nullable=True)
    favourites_by: Mapped[list['FavouriteCharacters']] = relationship(back_populates='people')

    def __repr__(self):
        return f'Personaje {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "affiliations": self.affiliations,
                        
        }


class FavouriteCharacters(db.Model):
    __tablename__ = 'favourite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates='char_favourites')
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    people: Mapped['Characters'] = relationship(back_populates='favourites_by')

    def __repr__(self):
        return f'Al {self.users} le gusta el {self.people}'

class Planet(db.Model):
    __tablename__= 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    extension: Mapped[float] = mapped_column(Float, nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    locations: Mapped[str] = mapped_column(String, nullable=True)
    climate: Mapped[str] = mapped_column(String(60), nullable=True)
    species: Mapped[str] = mapped_column(String(80), nullable=True)
    affiliations: Mapped[str] = mapped_column(String(3000), nullable=True)
    favourites_by: Mapped[list['FavouritePlanets']] = relationship(back_populates='planets')

    def __repr__(self):
        return f'Planet {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "extension": self.extension,
            "population": self.population,
            "locations": self.locations,
            "climate": self.climate,
            "species": self.species,
            "affiliations": self.affiliations,
            
        }

class FavouritePlanets(db.Model):
    __tablename__= 'favourite_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates='plan_favourites')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    planets: Mapped['Planet'] = relationship(back_populates='favourites_by')

    def __repr__(self):
        return f'Al {self.users} le gusta el {self.planets}'

class Starship(db.Model):
    __tablename__= 'starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False )
    model: Mapped[str] = mapped_column(String(80), nullable=True)
    dimensions: Mapped[float] = mapped_column(Float, nullable=True)
    velocity: Mapped[float] = mapped_column(Float, nullable=True)
    hiperspace: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    affiliations: Mapped[str] = mapped_column(String(20), nullable=True)
    favourites_by: Mapped[list['FavouriteStarships']] = relationship(back_populates='starships')

    def __repr__(self):
        return f'Starship {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "dimensions": self.dimensions,
            "velocity": self.velocity,
            "hiperspace": self.hiperspace,
            "affiliations": self.affiliations,
            
        }

class FavouriteStarships(db.Model):
    __tablename__= 'favourite_starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates='star_favourites')
    starship_id: Mapped[int] = mapped_column(ForeignKey('starship.id'))
    starships: Mapped['Starship'] = relationship(back_populates='favourites_by')

    def __repr__(self):
        return f'Al {self.users} le gusta la {self.starships}'