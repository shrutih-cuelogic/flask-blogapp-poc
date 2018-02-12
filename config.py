import os
# basedir = os.path.abspath(os.path.dirname(__file__))


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Auth:
    CLIENT_ID = ('833108435253-hs7dmgaerscr01tqr75d14rmu81li6rc.apps.googleusercontent.com')
    CLIENT_SECRET = 'MSJ4Q_YrBCE4qcWZgv8G-Aoq'
    REDIRECT_URI = 'http://localhost:8090/oauth2callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.insert',
        'https://www.googleapis.com/auth/gmail.labels',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.settings.sharing',
        'https://www.googleapis.com/auth/gmail.settings.basic'
    ]


class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    # Use this for docker running
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin123@flaskapp-postgres:5432/postgres'
    SECRET_KEY = 'b240ac48e41e84a4278d195092289a8bdb08556b22f6760d'
    SQLALCHEMY_TRACK_MODIFICATIONS =True
    # FIXTURE_DIRS = (
    #    'app/auth/fixtures/',
    #    'app/blog/fixtures/'
    # )

class TestConfig(Config):
    """docstring for TestConfig"""
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin123@localhost:5432/postgres'
    # Use this for docker running
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin123@flaskapp-postgres:5432/postgres'
    SECRET_KEY = 'b240ac48e41e84a4278d195092289a8bdb08556b22f6760d'
    SQLALCHEMY_TRACK_MODIFICATIONS =False