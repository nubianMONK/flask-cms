import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'True'
    USERNAME = 'admin'
    PASSWORD = 'admin'

    @staticmethod
    def init_app(app):
        pass


#SESSION_TYPE = 'sqlalchemy'

#WTF_CSRF_ENABLED = 'True'
# DATABASE_PATH = os.path.join(basedir, DATABASE)
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = 'flask_cms'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postadmin@localhost/' + DATABASE


class TestConfig(Config):
    Testing = True
    DATABASE = 'flask_cms_test'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postadmin@localhost/' + DATABASE


class ProductionConfig(Config):
    DATABASE = 'flask_cms_prod'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postadmin@localhost/' + DATABASE


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
