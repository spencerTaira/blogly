"""Blogly application."""

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