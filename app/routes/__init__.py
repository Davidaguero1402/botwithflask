# app/routes/__init__.py
from flask import Blueprint
from .home import home
from .users import users
from .bots import bot_routes

def register_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(bot_routes, url_prefix='/bots')


