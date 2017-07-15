from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from views import app, db


#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object('config')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
