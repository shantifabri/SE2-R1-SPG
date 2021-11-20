from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, FloatField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import NumberInput

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    role = SelectField('Role',choices=[('F', 'Farmer'), ('S', 'Shop Manager'), ('A', 'Admin')])

class ProductRequestForm(FlaskForm):
    email = StringField('Client Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    quantity = IntegerField('Quantity', widget=NumberInput(min=1, step=1), validators=[InputRequired()])

class ClientInsertForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    phone = StringField('Phone', validators=[InputRequired(), Length(min=5, max=15)])

class ProductInsertForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)])
    price = FloatField('Price', validators=[InputRequired()], widget=NumberInput(min=0.01))
    qty_available = IntegerField('Quantity', widget=NumberInput(min=1, step=1), validators=[InputRequired()])
