import os
basedir = os.path.abspath(os.path.dirname(__file__))


# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Config(object):

    SECRET_KEY = 'b240ac48e41e84a4278d195092289a8bdb08556b22f6760d'
    SQLALCHEMY_TRACK_MODIFICATIONS =True
    
class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #'postgresql://shruti:shruti@localhost/flaskblog'
    SECRET_KEY = 'b240ac48e41e84a4278d195092289a8bdb08556b22f6760d'
    SQLALCHEMY_TRACK_MODIFICATIONS =True