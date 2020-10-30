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
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin123@jeevan.cdhnjohiqccx.ap-south-1.rds.amazonaws.com/WEBBlogdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    MYSQL_HOST = "jeevan.cdhnjohiqccx.ap-south-1.rds.amazonaws.com" #os.environ.get('MYSQL_HOST')
    MYSQL_USER = "admin" #s.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = "admin123" # os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = 'WEBBlogdb'
    MYSQL_CURSORCLASS = 'DictCursor'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # "mysql://root:root123@localhost/Blogwebsitedb"

