from flask import jsonify, Blueprint, current_app
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import timedelta

home = Blueprint('home', __name__)
basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))
modo = os.getenv('FLASK_ENV', 'development')

def jsonify_config(config):
    """Convert the configuration dictionary to a JSON-serializable format."""
    serializable_config = {}
    for key, value in config.items():
        if isinstance(value, timedelta):
            # Convert timedelta to a string representation
            serializable_config[key] = str(value)
        elif isinstance(value, (list, dict, str, int, float, bool, type(None))):
            # Directly serializable types
            serializable_config[key] = value
        else:
            # Other types, if necessary, can be converted to string or other representation
            serializable_config[key] = str(value)
    return serializable_config

@home.route('/', methods=['GET'])
def index():
    config = jsonify_config(current_app.config)
    response = {
        "message": f"OK, esta funcionando en el modo de: {modo}",
        "config": config
    }
    return jsonify(response)
