import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from app.routes import home
from app.routes import register_blueprints
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
login_manager = LoginManager()

def create_app() -> None:
    config_name = os.getenv('FLASK_ENV')
    app = Flask(__name__)
    f = config.factory(config_name if config_name else 'development')
    app.config.from_object(f)
    f.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
#Algo que es bastante importante y que debemos tener en cuenta es que el debemos crear las tablas
#en nuestra base de datos, las siguientes lineas hacen tal cosa. 
#pero ademas debemos agregar estos comandos

#flask db migrate -m "Initial migration."
#flask db upgrade 
#con esos comandos podemos crear o actualizar nuestra base de datos posgres
# Importa los modelos para que sean registrados
    with app.app_context():
       from app.models import Usuarios, Bots, Bancos, Estrategias, Exchanges, Operaciones, Activos

# Con las siguientes lineas podemos crear las rutas que 
# necesitamos en nuestra aplicacion 
# register blueprint es funcion que nos ayuda a crear esto 
# home en este caso es el controlador que usararemos 
# (Lo definimos en la carpeta routes)
# Url_prefix recibe como argumento la ruta que queremos crear.
#  y por la que el usuarioentrara a nuestra aplicacion 
#   app.register_blueprint(home,url_prefix='/')

    #Esta funcion añadiria todas las rutas a mi aplicacion
    register_blueprints(app)

    @app.shell_context_processor    
    def ctx():
        return {
            "app": app,
            'db' : db
            }
    
    return app
