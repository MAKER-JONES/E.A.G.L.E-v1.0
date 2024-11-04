from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String, nullable = False)
    cadets_last = db.Column(db.Text, nullable = False, unique= False)
    cadets_first = db.Column(db.Text, nullable = False, unique = False)
    cadets_id = db.Column(db.String, nullable = False)

class Cadet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    flight_name = db.Column(db.String, nullable=False)
    student_id = db.Column(db.String, nullable=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_type = db.Column(db.String, nullable=False) # mb, pt, uni
    cadet_id = db.Column(db.String, nullable=False)
    score_value = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable = False)
#reset db for score change
"""
In terminal to create database type:

from models import app, db
app.app_context().push()
db.create_all()

"""
