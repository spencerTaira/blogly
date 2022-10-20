"""Models for Blogly."""

from time import timezone
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_PROFILE_PIC = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Class """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,  # remove spaces when passing a value through
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_PROFILE_PIC)

    # def __init__(self):
    #     self.full_name = self.get_full_name()
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    # .posts to navigate to posts because of backref


class Post(db.Model):
    """Post Class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String(300),
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship('User', backref='posts')
