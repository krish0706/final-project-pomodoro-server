from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/about")
def about():
    return render_template('about.html')