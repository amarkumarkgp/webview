import os
from flask import Flask
from datetime import timedelta

# developer define imports
from .routes import server
from .extensions import mysql

base_dir = os.path.relpath(os.path.dirname(__file__))
print(base_dir)

static_path = os.path.join(r"/", base_dir,  'static') or '/static'


def create_app(config_file):
    app = Flask(__name__, static_url_path=static_path)

    # attaching config file to app
    app.config.from_object('flask_config.DevConfig')
    
    app.permanent_session_lifetime = timedelta(minutes=10)

    with app.app_context():

        # initialising the database
        mysql.init_app(app)

        # registering blueprints for routs
        app.register_blueprint(server)

        return app
