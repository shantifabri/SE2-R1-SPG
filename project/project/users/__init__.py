from flask import Blueprint, render_template
users_blueprint = Blueprint('users', __name__, static_folder='../static' , template_folder='../templates')


from . import routes