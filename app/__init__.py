import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_login import current_user

bootstrap = Bootstrap()
db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'main.index'
admin = Admin()


def create_app(config_name):
    """
        Create an application instance.
        
        This function acts as a factory function that
        can create different flask app instances based
        on the configuration settings it is passed
    """
    app = Flask(__name__)

    # import configuration for the application from config folder
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize flask extensions on the application instance
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    admin.init_app(app)

    # import blueprints and register them on application's instance
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
