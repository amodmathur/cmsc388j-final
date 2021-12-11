from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from .models import User
class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField('Search')

class PropertySubmitForm(FlaskForm):
    propic = FileField('Profile Picture', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'png'], 'Images Only!')
    ])
    
    PropertyName = StringField("Property Name",validators=[InputRequired(), Length(min=5, max=100)]) 
    PropertyDescription = StringField("Property Description", validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit Property')

class PropertyReviewForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=5, max=500)])
    submit = SubmitField('Enter Comment')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):        
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is None:
            raise ValidationError("That username does not exist in our database.")
