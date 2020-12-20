# app/api/__init__.py

from flask import Blueprint

apikey = Blueprint('apikey', __name__)

from . import views
