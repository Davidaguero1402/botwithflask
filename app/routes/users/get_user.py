from flask import Blueprint, jsonify


user_get = Blueprint('user_get', __name__)

@user_get.route('/<int:id>', methods=['GET'])
def get_user(id):
    from app.models.users import Usuarios
    user = Usuarios.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())