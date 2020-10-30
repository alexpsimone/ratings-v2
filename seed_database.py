"""Script to seed database."""

#Python standard libraries
import os
import json
from random import choice, randint
from datetime import datetime

# Our files
import crud
import model
import server

# Drop and re-create the database.
os.system('dropdb ratings')
os.system('createdb ratings')

# Connect to the database. 
# Imported from model.py
model.connect_to_db(server.app)     # app is imported from server.py
model.db.create_all()               # populate db; create_all() is a func from SQLAlchemy

# Load data from data/movies.json
with open('data/movies.json') as filename:
    movie_data = json.loads(filename.read()) # reads data into var movie_data

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    release_date = datetime.strptime(movie['release_date'], "%Y-%m-%d")

    movie = crud.create_movie(title, overview, release_date, poster_path) # adds movie to db, import from crud.py

    movies_in_db.append(movie)                                            # adds movie to movies_in_db list

# Generate 10 users, each with 10 ratings.
# Use choice to get a random movie from movies_in_db 
# and use randint to generate a random number between 1–5. 
for n in range(10):
    email=f'user{n}@test.com'
    password='test'

    user = crud.create_user(email, password)

    # Generate random ratings for 10 random movies.
    for m in range(10):
        score = randint(1, 5)
        movie = choice(movies_in_db)

        crud.create_rating(score, movie, user)