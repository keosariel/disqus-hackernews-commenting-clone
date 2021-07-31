from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

basedir = os.path.dirname(os.path.abspath(__file__))

def create_db():
    db.create_all()

def create_app(name):
    app = Flask(name, static_folder=None)
    
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    # Register Bluprints
    from app.posts import post
    from app.votes import vote
    app.register_blueprint(post)
    app.register_blueprint(vote)
    
    return app, None

from app import models