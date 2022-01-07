"""Models and database functions for Ratings project."""

# import Flask
# import SQLAlchemy as db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation, relationship

from secret import user, password, host, port, db_name

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

# use 'python -i model.py' to start model.py with interpreter, then
# db.create_all()

db = SQLAlchemy()


url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    # user_rel = relationship('Rating')

    def __repr__(self):
        '''More helpful information when printed'''
        return f'<User user_id={self.user_id} email={self.email}>'

# Put your Movie and Rating model classes here.


class Movie(db.Model):
    '''Movies of ratings website.'''

    __tablename__ = 'movies'

    # movie_rel = relationship('Movie')

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url =db.Column(db.String(200), nullable=False)


class Rating(db.Model):
    '''Ratings of ratings website'''

    __tablename__ = 'ratings'

   
    user_rel = relationship('User')
    movie_rel = relationship('Movie')

 
    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False) #need to make foreign key!
    movie_id = db.Column(db.Integer, ForeignKey('movies.movie_id'), nullable=False) # need to make foreign key!
    score = db.Column(db.Integer, nullable=False)
    


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ratings'
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")