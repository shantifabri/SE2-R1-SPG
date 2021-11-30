from flask import Flask, session, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app

def initialize_extensions(app):
    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Flask-Login configuration
    from project.models import User

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        # session["name"] = user.name
        # session["surname"] = user.surname
        # session["email"] = user.email
        # session["role"] = user.role
        session["logged"] = True
        return user


def register_blueprints(app):
    from project.other import other_blueprint
    from project.users import users_blueprint

    app.register_blueprint(other_blueprint)
    app.register_blueprint(users_blueprint)




