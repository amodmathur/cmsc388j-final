# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

app = Flask(__name__)
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/final-project'
app.config['SECRET_KEY'] = b'\xfe\xff\x11\x9cT\x11\x82)\x07\x8c\xa8\x1f\x03_\xb9\x92'

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

from . import routes