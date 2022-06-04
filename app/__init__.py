import logging

from flask import Flask

from app.extensions import db, migrate, bootstrap, mail, login
from app.config import Config
from app.money_movements import bp as route_bp
from app.auth import bp as auth_bp


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)
    login.init_app(app)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)

    app.logger.setLevel(logging.INFO)

    app.register_blueprint(route_bp)
    app.register_blueprint(auth_bp)

    return app
