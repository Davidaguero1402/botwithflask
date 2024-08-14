from flask import Blueprint, jsonify

get_users = Blueprint('get_users', __name__)

@get_users.route('/users', methods=['GET'])
def get_user():
    return jsonify({"message": "Todos los usuarios"})
