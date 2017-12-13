# Import flask and template operators
import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from production import ProdConfig
# UPLOAD_FOLDER = '/static/blog/images/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Import a module / component using its blueprint handler variable (mod_auth)


# Define the WSGI application object
is_prod = os.environ.get('IS_HEROKU', None)

app = Flask(__name__)
admin = Admin(app, name='sample', template_mode='bootstrap3')

# Configurations

if not is_prod:
	app.config.from_object('config.DevConfig')
else:
	app.config.from_object(ProdConfig)

# Define the database object which is imported
# by modules and controllers
	
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.session_protection ='Strong'

from app.auth import views, models
from app.blog import views, models
from app.auth import auth as auth_blueprint
from app.blog import blog_mod as blog_blueprint

# Register blueprint(s)
app.register_blueprint(auth_blueprint)
app.register_blueprint(blog_blueprint)

# Build the database:
# This will create the database file using SQLAlchemy
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Blog, db.session))
admin.add_view(ModelView(models.UserComment, db.session))

from app.auth.models import *

db.create_all()