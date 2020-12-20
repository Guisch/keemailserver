# app/models.py

import secrets
import string
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_secret(length, alphabet=(string.ascii_letters + string.digits)):
    return ''.join(secrets.choice(alphabet) for i in range(length))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User: {self.email}>'


class ApiKey(db.Model):
    __tablename__ = 'apikeys'
    id = db.Column(db.Integer, primary_key=True)
    key_hash = db.Column(db.String(255), index=True, unique=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def key(self):
        """
        Set key to a hashed key and return it
        """
        secret = generate_secret(50)
        self.key_hash = generate_password_hash(secret)
        return secret

    def verify_key(self, key):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.key_hash, key)

    def __repr__(self):
        return f'<ApiKey: {self.name}>'


class Alias(db.Model):
    __tablename__ = 'aliases'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), index=True, unique=True)
    destination = db.Column(db.String(255))
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    used_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Alias: {self.name}>'
