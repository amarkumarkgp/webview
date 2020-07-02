import os

base_dir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "db.sqlite3")
