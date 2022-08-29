from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
# from flask_login import LoginManager
#
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # login_manager.init_app(app)

    return app
