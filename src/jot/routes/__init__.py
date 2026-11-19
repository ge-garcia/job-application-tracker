from flask import Flask

from jot.routes.companies import bp as companies_bp


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints on the Flask application"""
    app.register_blueprint(companies_bp)
