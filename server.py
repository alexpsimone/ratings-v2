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

if __name__ == '__main__':
    connect_to_db(app) ## func from model.py
    app.run(host='0.0.0.0', debug=True)
