"""Seed file to make sample data for users db."""

from app import app
from models import User, Post, db

# Create all tables
db.drop_all()
db.create_all()

spencer = User(first_name='Spencer', last_name='Taira')
ashley = User(first_name='Ashley', last_name='Mathew')

db.session.add_all([spencer, ashley])
db.session.commit()


post1 = Post(title="Post 1", content="I am post one", user_id=1)
post2 = Post(title="Post 2", content="I am post two", user_id=2)

db.session.add_all([post1, post2])
db.session.commit()
