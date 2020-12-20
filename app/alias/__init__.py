# app/api/__init__.py

from flask import Blueprint

alias = Blueprint('alias', __name__)

from . import views
