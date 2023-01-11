from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(Integer, primary_key=True)
    planet_name = db.Column(String(50))
    climate = db.Column(String(30))
    population = db.Column(Integer, nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.planet_name

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet_name
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    birth_date = db.Column(String(70), nullable=True)
    gender = db.Column(String(10), nullable=False)
    affilliation = db.Column(String(250), nullable=False)
    planet_id = db.Column(Integer, ForeignKey('planet.id'))

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "affilliation": self.affilliation
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite planet'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))
    planet_id = db.Column(Integer, ForeignKey('planet.id'))

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite people'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))
    people_id = db.Column(Integer, ForeignKey('people.id'))

    def __repr__(self):
        return '<FavoritePeople %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id": self.people_id
        }