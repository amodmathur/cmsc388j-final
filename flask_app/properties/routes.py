from flask import Blueprint, render_template, url_for, redirect, request, flash
# from flask_login import current_user
# from ..forms import MovieReviewForm,SearchForm
from ..forms import SearchForm, PropertyForm
#from ..models import User, Review
from ..models import Property, User
#from ..utils import current_time
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

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

    if form.validate_on_submit():
        prop = Property(
            city=form.city.data,
            description=form.description.data,
            owner=current_user._get_current_object(),
            price=form.price.data,
            image=form.image.data.put(form.image.data.stream, content_type=f'images/{secure_filename(form.image.data)[-3]}'),
            name=form.name.data    
        )
        prop.save()
        #flash('Your Property has been listed!')
        return redirect(request.path)
    
    return render_template("listing.html", form=form)


@properties.route("/properties/<username>")
def property_detail(username):
    user = User.objects(username=username).first()
    properties = Property.objects(owner=user)

    return render_template("property_details.html", username=username, properties=properties)


@properties.route("/properties-search/<query>")
def property_search(query):
    #properties = Property.objects(city=query)
    temp = Property.objects.all()
    properties = [prop for prop in temp if prop.city.lower()[0] == query.lower()[0]]
    return render_template("query.html", results=properties)