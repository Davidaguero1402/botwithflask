from flask import request, jsonify, Blueprint

post_users = Blueprint('post_users', __name__)

@post_users.route('/', methods=['POST'])
def create_user():
    #Importacion retrasada para evitar la importacion circular
    from app import db
    from app.models.users import Usuarios
    data = request.get_json()

    # Validación simple de los datos recibidos
    if not data or not data.get('nombre') or not data.get('email'):
        return jsonify({"message": "Datos incompletos"}), 400

    # Verificar si el usuario ya existe
    existing_user = Usuarios.query.filter_by(email=data.get('email')).first()
    if existing_user:
        return jsonify({"message": "El usuario ya existe"}), 409

    # Crear el nuevo usuario
    new_user = Usuarios(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        email=data.get('email'),
        balance=data.get('balance', 0.0),
        role=data.get('role', '')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado con éxito", "user": new_user.to_dict()}), 201
