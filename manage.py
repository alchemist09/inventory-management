from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from app import create_app, db

app = create_app('development')

config_file = os.path.join(os.getcwd(), 'config', 'development.py')
app.config.from_pyfile(config_file)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
