# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from datetime import datetime
from app import db, lm
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
# # Define a base model for other database tables to inherit
# class Base(db.Model):

#     __abstract__  = True

#     id            = db.Column(db.Integer, primary_key=True)
#     date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
#     date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
#                                            onupdate=db.func.current_timestamp())

# Define a User model
class User(db.Model, UserMixin):

    __tablename__ = 'auth_user'

    id = db.Column(db.Integer,
        primary_key=True, 
        autoincrement=True
    )
    name = db.Column(db.String(128),
        nullable=False
    )
    username  = db.Column(db.String(128),
        nullable=False
    )
    email = db.Column(db.String(128),
        nullable=False,
        unique=True
    )
    password = db.Column(db.String(192),
        nullable=False
    )
    password_hash = db.Column(db.String(192),
        nullable=False
    )
    address = db.Column(db.String(192),
        nullable=True
    )
    contact = db.Column(db.Integer,
        nullable=True
    )
    gender = db.Column(db.String(50),
        nullable=True
    )
    blogs = db.relationship('Blog',
        backref='author',
        cascade="all,delete",
        lazy='dynamic'
    )
    user_comments = db.relationship('UserComment',
        backref='commenter',
        cascade="all,delete",
        lazy='dynamic'
    )
    tokens = db.Column(db.Text)

    def __str__(self):
        return '<User %r>' % (self.username)

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
