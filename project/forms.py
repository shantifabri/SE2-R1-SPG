from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=1, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    name = StringField('name', validators=[InputRequired(), Length(min=1, max=20)])
    surname = StringField('surname', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    role = SelectField('role',choices=[('F', 'Farmer'), ('S', 'Shop Manager'), ('A', 'Admin')])