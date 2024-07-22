from flask import jsonify, Blueprint

ejemplo = Blueprint('ejemplo', __name__)

@ejemplo.route('/', methods=['GET'])
def index():
    resp = jsonify("OK esta funcionando en el modo de produccion, en la ruta de ejempo")
    resp.status_code = 200
    return resp