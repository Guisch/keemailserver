# app/__init__.py

import pymysql
# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# LoginManager
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .apikey import apikey as apikey_blueprint
    app.register_blueprint(apikey_blueprint)

    from .alias import alias as alias_blueprint
    app.register_blueprint(alias_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
