from flask import render_template

from . import other_blueprint


################
#### routes ####
################

@other_blueprint.route('/')
def index():
    return render_template('../templates/index.html')

@other_blueprint.route('/home')
def index():
    return render_template('../templates/index.html')
