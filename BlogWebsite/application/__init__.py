import os
from flask import Flask

# developer define imports
from .routes import server
from .extensions import db
# from dbConnection import get_connection

base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_file):
    app = Flask(__name__, static_url_path='/static')

    app.config.from_pyfile(config_file)
    app.register_blueprint(server)
    db.init_app(app)

    return app
