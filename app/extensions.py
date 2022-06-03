# Extensions are declared once in this file and then imported when needed throughout the app
# This prevents circular import errors that occur when extensions are declared in the same file as create_app()
# https://stackoverflow.com/questions/42909816/can-i-avoid-circular-imports-in-flask-and-sqlalchemy

from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()