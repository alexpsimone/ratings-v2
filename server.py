"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

# Configure an instance of Flask, called app.
app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Route to the homepage."""

    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.return_movies()

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def display_movie(movie_id):
    """Display a movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    """View all users."""

    users = crud.return_users()

    return render_template('all_users.html', users=users)

@app.route("/users", methods=["POST"])
def process_new_user():
    """Create a new user account."""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash("You can't create an account using an existing profile's email. Try again.")
    else:
        crud.create_user(email, password)
        flash("Your account was successfully created!")
    
    return redirect('/')


@app.route('/users/<user_id>')
def display_user(user_id):
    """Display a user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route("/login", methods=["POST"])
def login_user():
    """Log in a user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user  = crud.get_user_by_email(email)

    if user.password == password:
        session['current_user'] = user.user_id
        flash("Logged in!")
        print(session)
    else:
        flash("Password incorrect!")

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app) ## func from model.py
    app.run(host='0.0.0.0', debug=True)
