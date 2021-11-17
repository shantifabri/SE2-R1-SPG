from flask import Blueprint
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

other_blueprint = Blueprint('other', __name__, static_folder='../static', template_folder='../templates')

# from . import routes
# @other_blueprint.route('/')
# def index():
#     return render_template('index.html')
        

