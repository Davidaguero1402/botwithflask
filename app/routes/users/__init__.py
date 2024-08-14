from flask import Blueprint
from .post_users import post_users
from .get_user import user_get

users = Blueprint('users', __name__)

users.register_blueprint(user_get, url_prefix='/')
users.register_blueprint(post_users, url_prefix='/')
