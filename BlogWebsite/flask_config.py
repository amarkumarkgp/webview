"""Flask config."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = os.urandom(25)
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = 'upload_files'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root123'
    MYSQL_DB = 'blogwebsite'
    MYSQL_CURSORCLASS = 'DictCursor'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = 'blogwebsitedb'
    MYSQL_CURSORCLASS = 'DictCursor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
