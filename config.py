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
    BOOKMARKS_PER_PAGE = os.environ.get('BOOKMARKS_PER_PAGE') or '10'

    @staticmethod
    def init_app(app):
        pass


"""
conditionally loaded configurations
"""


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sersky.db')
    DB_USER = os.environ.get('DB_USER') or 'user'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'webmane'
    DB_TYPE = os.environ.get('DB_TYPE') or 'postgresql'
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TestingConfig(Config):
    TESTING = True
    DB_USER = os.environ.get('DB_USER') or 'user'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'webmane'
    DB_TYPE = os.environ.get('DB_TYPE') or 'postgresql'
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://cra_user:xyz-replace-with-secret@localhost:5432/webmane'
    DB_USER = os.environ.get('DB_USER') or 'user'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'webmane'
    DB_TYPE = os.environ.get('DB_TYPE') or 'postgresql'
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
