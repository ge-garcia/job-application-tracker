import os

from flask import Flask

from jot.db import init_db
from jot.routes import register_blueprints


def create_app() -> Flask:
    """Build the Flask application with database teardown and every route blueprint registered"""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

    init_db(app)
    register_blueprints(app)

    return app
