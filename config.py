import os
"""
adding base directory as the absolute path of this file
note that __file__ will not be present running script from interpreter
"""
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration:
    creating properties for each config variable, some are pulled
    from environment variables
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SERVER_MAIL_SUBJECT_PREFIX = '[Server]'
    SERVER_MAIL_SENDER = 'Server Admin <server@server.com>'
    SERVER_ADMIN = os.environ.get('SERVER_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super secret jwt'

    @staticmethod
    def init_app(app):
        pass


"""
conditionally loaded configurations
"""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sersky.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cra_user:xyz-replace-with-secret@localhost:3306/webmane'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cra_user:xyz-replace-with-secret@localhost:3306/webmane'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
