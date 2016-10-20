import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'main.index'


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # import configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize extensions
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)

    # import blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
