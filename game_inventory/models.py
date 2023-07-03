from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import uuid
import secrets


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String, unique = True, default = '')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    game = db.relationship('Game', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name, last_name):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = self.set_password(password)
        self.token = self.set_token()

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)

    def set_token(self):
        return secrets.token_hex(24)
        
    def __repr__(self):
        return f"{self.username} has been added."
    

class Game(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=5, scale=2))
    system = db.Column(db.String(50), nullable = True)
    year_made = db.Column(db.Integer, nullable = True)
    genre = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, system, year_made, genre, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.system = system
        self.year_made = year_made
        self.genre = genre
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    

class GameSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'system', 'year_made', 'genre']

game_schema = GameSchema()
games_schema = GameSchema(many = True)