"""Blogly application."""

from nturl2path import url2pathname
from unicodedata import name
from flask import Flask, render_template, request, session, redirect, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "password"

connect_db(app)
db.create_all()

@app.get('/')
def home_page():
    """ Redirects to list of users"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """ Lists all users """

    users = User.query.order_by(User.last_name, User.first_name).all()
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
    image_url = image_url if image_url != "" else None

    user = User(first_name = first_name, last_name = last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect ('/users')

@app.get('/users/<int:user_id>')
def show_user_profile(user_id):
    """Shows the users profile, options to edit info and delete profile"""

    user = User.query.get_or_404(user_id)

    return render_template('user_profile.html', user=user)

@app.get('/users/<int:user_id>/edit')
def edit_user_profile(user_id):
    """ Shows edit profile page and allows users to edit info"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_profile.html', user=user)

@app.post('/users/<int:user_id>/edit')
def update_user_profile(user_id):
    """ Updates sql table with edits """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ deletes record referencing primary key (id) """
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    flash("User has been deleted!")
    return redirect('/users')