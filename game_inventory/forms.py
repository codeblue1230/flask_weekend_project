from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    firstname = StringField('First Name', validators = [DataRequired()])
    lastname = StringField('Last Name', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class GameForm(FlaskForm):
    name = StringField('Name')
    description = StringField('Description')
    price = DecimalField('Price', places=2)
    system = StringField('System')
    year_made = IntegerField('Year Made')
    genre = StringField('Genre')
    submit_button = SubmitField()