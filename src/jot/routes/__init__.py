from flask import Flask

from jot.routes._components import bp as components_bp
from jot.routes.applications import bp as applications_bp
from jot.routes.companies import bp as companies_bp
from jot.routes.contacts import bp as contacts_bp
from jot.routes.dashboard import bp as dashboard_bp
from jot.routes.errors import bp as errors_bp
from jot.routes.jobs import bp as jobs_bp
from jot.routes.match import bp as match_bp


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints on the Flask application"""
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(components_bp)
    app.register_blueprint(errors_bp)
