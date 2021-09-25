from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_current_user


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


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
    jwt.init_app(app)

    from .api import api as api_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

