import os
from flask import Flask
from datetime import timedelta

# developer define imports
from .routes import server
from .extensions import mysql, db

base_dir = os.path.relpath(os.path.dirname(__file__))

static_path = os.path.join(r"/", base_dir,  'static') or '/static'


def create_app(config_file):
    app = Flask(__name__, static_url_path=static_path, instance_relative_config=False)

    # attaching config file to app
    app.config.from_object('flask_config.ProdConfig')
    app.secret_key = "dafdafd5af7548s7fd7a5f"   
    app.permanent_session_lifetime = timedelta(minutes=10)

    with app.app_context():

        # initialising the database

        db.init_app(app)
        mysql.init_app(app)

        # registering blueprints for routs
        app.register_blueprint(server)

        return app
