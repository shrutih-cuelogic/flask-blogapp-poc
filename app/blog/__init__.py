from flask import Blueprint
blog_mod = Blueprint('blog_mod', __name__)

from . import models, views, forms