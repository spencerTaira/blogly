"""Blogly application."""

from nturl2path import url2pathname
from unicodedata import name
from flask import Flask, render_template, request, session, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def home_page():
    """ Redirects to list of users"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """ Lists all users """

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """ Shows input form for new user"""

    return render_template('new_user_form.html')

@app.post('/users/new')
def add_new_user():
    """ Process adding a new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name = first_name, last_name = last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect ('/users')

@app.get('/users/<user_id>')
def show_user_profile(user_id):
    """Shows the users profile, options to edit info and delete profile"""

    user = User.query.get_or_404(user_id)

    return render_template('user_profile.html', user=user)