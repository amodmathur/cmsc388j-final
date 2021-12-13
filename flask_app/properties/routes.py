from flask import Blueprint, render_template, url_for, redirect, request, flash
# from flask_login import current_user
# from ..forms import MovieReviewForm,SearchForm
from ..forms import SearchForm, PropertyForm
#from ..models import User, Review
from ..models import Property, User
import io
import base64
#from ..utils import current_time
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)

'''
heroku config:set MONGODB_HOST="mongodb+srv://JDqZGfywQwtyTIGP:JDqZGfywQwtyTIGP@cmsc388-cluster.5kn19.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
'''

from PIL import Image

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# JDqZGfywQwtyTIGP
# create blueprints inside of movies.routes - index, query_results, movie_detail, user_detail
properties = Blueprint('properties', __name__)

@properties.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("properties.property_search", query=form.search_query.data))

    return render_template("index.html", form = form)


@properties.route("/list_property", methods=["GET", "POST"])
@login_required
def list_property():
    form = PropertyForm()
    # image = None
    temp = None
    print("about to validate")
    if form.is_submitted():
        print("submitted")
        prop = Property(
            city=form.city.data,
            description=form.description.data,
            owner=current_user._get_current_object(),
            price=form.price.data,
            image=None,
            name=form.name.data    
        )
        #img = images(form.name.data)
        img = form.image.data
        # print(img)
        # print("TEMP",images(prop.name))

        #filename = secure_filename(img.filename)
        if prop.image.get() is None:
            prop.image.put(img.stream, content_type='images/png')
        else:
            prop.image.replace(img.stream, content_type='images/png')

        #my_image = images(form.name.data)
        
        prop.save()
        return redirect(request.path)

    return render_template("listing.html", form=form)

def images(prop_name):
    prop = Property.objects(name=prop_name).first()
    print('here')
    print(prop)
    bytes_im = io.BytesIO(prop.image.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image


@properties.route("/properties/<username>")
def property_detail(username):
    user = User.objects(username=username).first()
    properties = Property.objects(owner=user)
    property_images = []
    for prop in properties:
        property_images.append(images(prop.name))

    return render_template("property_details.html", username=username, properties=properties, images=property_images,len=len(properties))


@properties.route("/properties-search/<query>")
def property_search(query):
    #properties = Property.objects(city=query)
    temp = Property.objects.all()
    properties = [prop for prop in temp if prop.city.lower()[0] == query.lower()[0]]
    property_images = []
    for prop in properties:
        property_images.append(images(prop.name))
    return render_template("query.html", results=properties, images=property_images, len=len(properties))