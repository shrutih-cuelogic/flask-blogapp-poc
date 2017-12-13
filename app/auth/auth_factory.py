import factory
from factory import alchemy, Sequence
from . import app,db,auth
from ..auth.models import User
from app.blog.blog_factory import BlogFactory


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    name = Sequence(lambda n: 'User{0}'.format(n))
    blogs = RelatedFactory(BlogFactory, 'user')