from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
# from ..forms import MovieReviewForm,SearchForm
from ..forms import SearchForm
#from ..models import User, Review
#from ..utils import current_time


# create blueprints inside of movies.routes - index, query_results, movie_detail, user_detail
properties = Blueprint('properties', __name__)

@properties.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    # if form.validate_on_submit():
    #     return redirect(url_for("movies.query_results", query=form.search_query.data))

    return render_template("index.html")

