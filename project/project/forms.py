from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, FloatField, SearchField, FileField, HiddenField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import NumberInput
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    company = StringField('Company', validators=[InputRequired(), Length(min=1, max=80)])
    role = SelectField('Role',choices=[('F', 'Farmer'), ('S', 'Shop Manager'), ('A', 'Admin')])

class AddToCartForm(FlaskForm):
    quantity = FloatField('Quantity (Kg):', widget=NumberInput(min=0.1, step=0.1), validators=[InputRequired()], render_kw={"class":"form-control","placeholder":"1.2 Kg"})

class ProductRequestForm(FlaskForm):
    email = StringField('Client Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    quantity = FloatField('Quantity (Kg):', widget=NumberInput(min=0.1, step=0.1), validators=[InputRequired()], render_kw={"class":"form-control","placeholder":"1.2 Kg"})

class ClientInsertForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])

class ProductInsertForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)], render_kw={"class":"form-control"})
    price = FloatField('Price', validators=[InputRequired()], widget=NumberInput(min=0.01, step=0.01), render_kw={"class":"form-control"})
    description = StringField('Description', validators=[InputRequired()], render_kw={"class":"form-control", "rows":"4"}, widget=TextArea())
    qty_available = IntegerField('Quantity (Kg):', widget=NumberInput(min=0.1, step=0.1), validators=[InputRequired()], render_kw={"class":"form-control","placeholder":"1.2 Kg"})
    image = FileField('Image', render_kw={"class":"upload"})

class ProductEditForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=20)], render_kw={"class":"form-control"})
    price = FloatField('Price', validators=[InputRequired()], widget=NumberInput(min=0.01, step=0.01), render_kw={"class":"form-control"})
    description = StringField('Description', validators=[InputRequired()], render_kw={"class":"form-control", "rows":"4"}, widget=TextArea())
    qty_available = IntegerField('Quantity (Kg):', widget=NumberInput(min=0.1, step=0.1), validators=[InputRequired()], render_kw={"class":"form-control","placeholder":"1.2 Kg"})

class CheckOutForm(FlaskForm):
    delivery_address = StringField('Delivery Address', validators=[Length(min=0, max=100)], render_kw={"placeholder": "Baker Street 13"})
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    date = StringField('Date', validators=[InputRequired()], render_kw={"class":"form-control","id":"pick-date","placeholder":"Pick a date"})

class CheckOutClientForm(FlaskForm):
    delivery_address = StringField('Delivery Address', validators=[Length(min=0, max=100)], render_kw={"placeholder": "Baker Street 13"})
    email = StringField('Email', validators=[Email(message="Invalid Email"), Length(min=6, max=30)])
    date = StringField('Date', validators=[InputRequired()], render_kw={"class":"form-control","id":"pick-date","placeholder":"Pick a date"})

class TopUpForm(FlaskForm):
    email = HiddenField('Email')
    amount = FloatField('', validators=[InputRequired()], widget=NumberInput(min=0.01, step=0.01), render_kw={"style":"text-align:center; width:50%; justify-content:between; display:inline-block", "placeholder":"€1,000.00", "value":""})
    #style="display:inline-block;" value="" data-type="currency" placeholder="$1,000.00"
    

class TopUpSearch(FlaskForm):
    search = SearchField('', render_kw={'class':'form-control','style':'width: 50%; display:inline-block','placeholder':'Search by email', 'aria-label':"Search"})
    # class="form-control form-inline mr-sm-2" style="width: 50%; display: inline-block"
