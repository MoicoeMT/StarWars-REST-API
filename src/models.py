from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorit', backref='user')

    

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class People(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    birth_year = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    favorites = db.relationship("Favorit", backref="people")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height
        }
        
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    favorites = db.relationship("Favorit" , backref="planets")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain
        }
        
class Favorit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column (db.Integer, db.ForeignKey("user.id"), nullable=False) #user id que debemos pasarlo junto con
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True) # el people id 
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id") , nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }