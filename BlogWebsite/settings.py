import os

base_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.urandom(25)

DEBUG = False

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root123'
MYSQL_DB = 'blogwebsite'
MYSQL_CURSORCLASS = 'DictCursor'



# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "db.sqlite3")
