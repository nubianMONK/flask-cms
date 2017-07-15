import os


basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'flask_cms'
USERNAME = 'admin'
PASSWORD = 'admin'
#SESSION_TYPE = 'sqlalchemy'
SECRET_KEY = 'hard to guess string'
#WTF_CSRF_ENABLED = 'True'
# DATABASE_PATH = os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postadmin@localhost/' + DATABASE
