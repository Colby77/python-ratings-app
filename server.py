"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/users')
def user_list():
    '''Shows the list of users'''
    
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/movies')
def movie_list():

    movies = Movie.query.order_by(Movie.title).all()

    return render_template('movie_list.html', movies=movies)


@app.route('/login', methods=['GET'])
def login_page():

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # print(email)
    # print(password)

    user = User.query.filter_by(email=email).first()
    # print(user.user_id, user.password)

    if user:
        if user.password == password:
            session['user'] = user.user_id
            flash('Logged in successfully', 'success')
            # print(session)
            return redirect(f'/users/{user.user_id}')
        else:
            flash('Password incorrect', 'error')
            return redirect('/login')
    else:
        flash('User not found', 'error')
        return redirect('/login')


@app.route('/logout')
def logout():

    del session['user']
    flash('Logged out', 'success')
    # print(session)
    return redirect('/')


@app.route('/register', methods=['GET'])
def register_page():

    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    
    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zipcode']

    user = User.query.filter_by(email=email).first()
    
    if user:
        flash('Account already exists', 'error')
        return redirect('/register')
    else:
        user = User(
                    email=email,
                    password=password,
                    age=age,
                    zipcode=zipcode
                    )
        flash('Account created', 'success')
        print(user)

        db.session.add(user)
        db.session.commit()

        session['user'] = user.user_id

    return redirect(f'/users/{user.user_id}')


@app.route('/users/<int:id>')
def show_user(id):
    
    user = User.query.get(id)
    # print(user)
    ratings = Rating.query.filter_by(user_id=user.user_id)
    print(ratings)

    return render_template('user_page.html',user=user, ratings=ratings)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
