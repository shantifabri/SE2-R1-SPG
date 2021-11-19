from flask import Blueprint

other_blueprint = Blueprint('other', __name__, static_folder='../static', template_folder='../templates')

from . import routes
