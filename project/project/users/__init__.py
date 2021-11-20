from flask import Blueprint

users_blueprint = Blueprint('users', __name__, static_folder='../static' , template_folder='../templates')

from . import routes