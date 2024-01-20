from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField, ValidationError, PasswordField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Email

class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])

    email = StringField('Email', validators=[InputRequired()])

    first_name = StringField('First Name', validators=[InputRequired()])

    last_name = StringField('Last Name', validators=[InputRequired()])

class LogInForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])

class fbForm(FlaskForm):

    title = StringField('title', validators=[InputRequired()])

    content = StringField('content', validators=[InputRequired()])




