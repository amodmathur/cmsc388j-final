
   
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
import base64
#import PIL
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    imdb_id = db.StringField(required=True, min_length=9, max_length=9)
    movie_title = db.StringField(required=True, min_length=1, max_length=100)


class Property(db.Document,UserMixin):
    owner = db.ReferenceField(User, required=True)
    city = db.StringField(required=True, min_length=1, max_length=50)
    description = db.StringField(required=True, min_length=1, max_length=500)
    image = db.FileField()
    price = db.IntField(required=True)
    name = db.StringField(required=True, min_length=1, max_length=50)