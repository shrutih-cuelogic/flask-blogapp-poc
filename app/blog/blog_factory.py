import factory
from factory import alchemy, Sequence
from . import app,db,auth
from ..blog_mod.models import Blog
from app.auth.auth_factory import UserFactory


class BlogFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Blog
        sqlalchemy_session = db.session

    title = Sequence(lambda n: 'Blog{0}'.format(n))
    user = factory.SubFactory(UserFactory)
