from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, FloatField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import NumberInput

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

class ProductRequestForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    quantity = IntegerField('quantity', widget=NumberInput(min=1, step=1), validators=[InputRequired()])

class ClientInsertForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=1, max=20)])
    surname = StringField('surname', validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    phone = StringField('phone', validators=[InputRequired(), Length(min=5, max=15)])

class ProductInsertForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=1, max=20)])
    price = FloatField('price', validators=[InputRequired()], widget=NumberInput(min=0.01))
    qty_available = IntegerField('quantity', widget=NumberInput(min=1, step=1), validators=[InputRequired()])
