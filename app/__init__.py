import logging

from flask import Flask

from app.extensions import db, migrate, bootstrap
from config import Config
from app.routes import bp as route_bp


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)

    app.logger.setLevel(logging.INFO)

    app.register_blueprint(route_bp)

    return app
