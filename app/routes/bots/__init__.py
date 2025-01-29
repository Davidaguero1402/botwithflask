from flask import Blueprint
from .routerbots import bot_routes

bots = Blueprint('bots', __name__)

# Registramos las rutas del bot con el prefijo correspondiente
bots.register_blueprint(bot_routes, url_prefix='/api')