import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application import create_app
from application.extensions import db
from application.models import User, Articles


base_dir = os.path.abspath(os.path.dirname(__file__))
app = create_app(os.path.join(base_dir, 'flask_config.py'))
app.config.from_object('flask_config.DevConfig')

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
