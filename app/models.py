import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Exercices(db.Model) :
    id = db.Column('user_id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(100))
    text = db.Column('text', db.Text)
    entree = db.Column('entree', db.Text)
    sortie = db.Column('sortie', db.Text)
    solution = db.Column('solution', db.String(500))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    password = db.Column('password', db.String(10))
    registered_on = db.Column('registered_on', db.DateTime, default=datetime.datetime.now)
    level = db.Column('level', db.Integer, default=1)
    codes = db.relationship('Codes')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_level(self):
        return self.level

    def __repr__(self):
        return '<User %r>' % (self.username)

class Startstop(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    status = db.Column('status', db.Integer)

class Codes(db.Model):
    __tablename__ = 'codes'
    id = db.Column('code_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'))
    sent_on = db.Column('sent_on', db.DateTime, default=datetime.datetime.now)
    code = db.Column('solution', db.Text)