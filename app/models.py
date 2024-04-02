from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

gyms = db.Table('gyms',
    db.Column("trainer_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("gym_id", db.Integer, db.ForeignKey('gym.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    gyms = db.relationship('Gym', secondary=gyms, backref="users", lazy="dynamic")
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Gym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    hours = db.Column(db.String, nullable=False)
    # phone = db.Column(db.String, nullable=False)
    photo_reference = db.Column(db.String, nullable=False)
    gyms = db.relationship('Gym', secondary=gyms, backref="gem", lazy="dynamic")

    def __init__(self, name, address, hours, phone, photo_reference):
        self.name = name
        self.address = address
        self.hours = hours
        self.phone = phone
        self.photo_reference = photo_reference

    def save(self):
        db.session.add(self)
        db.session.commit()