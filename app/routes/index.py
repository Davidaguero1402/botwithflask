from flask import jsonify, Blueprint

index = Blueprint('index', __name__)

@index.route('/', methods=['GET'])
def index_view():
    resp = jsonify("OK esta funcionando en el modo de produccion, en la ruta index")
    resp.status_code = 200
    return resp