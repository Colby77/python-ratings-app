"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    Movie.query.delete()

    f = open('seed_data/u.item', 'r')

    for row in f:
        row = row.rstrip()
        date_format = '%d-%b-%Y'
        row = row.split('|')
        movie_id = row[0]
        title = row[1]
        released_at = row[2]
        imdb_url = row[4]

        # movie_id, title, released_at, imdb_url = row.split('|')
        title = title.split()
        title.pop()
        title = ' '.join(title)
        # print(title)
        # print(imdb_url)
        released_at = datetime.strptime(released_at, date_format)

        movie = Movie(movie_id=movie_id,
                    title=title,
                    released_at=released_at,
                    imdb_url=imdb_url)

        db.session.add(movie)
    
    db.session.commit()
    f.close()
    print('DB Movies seeded!')


def load_ratings():
    """Load ratings from u.data into database."""
    Rating.query.delete()

    f = open('seed_data/u.data', 'r')
    
    for row in f:
        row = row.rstrip()
        row = row.split()
        user_id = row[0]
        movie_id = row[1]
        score = row[2]
        timestamp = row[3]

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score
                        )

        db.session.add(rating)

    db.session.commit()
    f.close()
    print('DB Ratings seeded!')


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])
    print(max_id)
    # new_id = max_id + 1

    # Set the value for the next user_id to be max_id + 1
    # query = f"SELECT setval('users_user_id_seq', {new_id}, true)"
    # query = f"ALTER SEQUENCE users_user_id_seq RESTART WITH {new_id};"
    query = "SELECT setval('users_user_id_seq', :new_id);"
    db.session.execute(query, {'new_id': max_id + 1})
    # db.session.execute(query)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    Rating.query.delete()
    User.query.delete()
    Movie.query.delete()

    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
