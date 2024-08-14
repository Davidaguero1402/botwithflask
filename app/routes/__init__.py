# app/routes/__init__.py
from flask import Blueprint
from .home import home
from .users import users

def register_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(users, url_prefix='/users')


