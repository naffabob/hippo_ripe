import os

basedir = os.path.abspath(os.path.dirname(__file__))

# добавить путь к bgpq3

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '', '../provider.db')
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '111www'
