"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

spencer = User(first_name='Spencer', last_name='Taira')
ashley = User(first_name='Ashley', last_name='Mathew')

db.session.add(spencer)
db.session.add(ashley)

db.session.commit()