from flask import Blueprint, render_template, request

from user_login_system.models import User

main = Blueprint('main', __name__)


# This is the home route
@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html")


# This is the route to about page with all the users info i.e. non-deleted but approved and unapproved both
@main.route('/about')
def about():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.username != 'admin').paginate(per_page=5, page=page)
    admins = User.query.filter(User.username == 'admin')
    return render_template("about.html", title='About', users=users, admins=admins)
