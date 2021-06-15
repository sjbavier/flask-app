from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_marshmallow import Marshmallow

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    """
    parameters: config_name<string>
    returns application with all of the necessary configuration
    initialized
    """

    app = Flask(__name__)

    """
    configure app
    """
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    """
    run initialization from app settings
    """
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

