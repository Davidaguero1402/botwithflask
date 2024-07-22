import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import config
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.routes import home
from app.routes.ejemplo import ejemplo
from app.routes.index import index
from app.models.testmodel import TestModel

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

config_name = os.getenv('FLASK_ENV')
if config_name not in ['development', 'production']:
    config_name = 'development'

print(f"Esta es la configuracion {config_name}")
app = Flask(__name__)
f = config.factory(config_name)
app.config.from_object(f)
f.init_app(app)
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(home, url_prefix='/api/v1')
app.register_blueprint(ejemplo, url_prefix='/ejemplo')
app.register_blueprint(index, url_prefix='/')

test = TestModel.query.first()


if __name__ == '__main__':
    app.run()
