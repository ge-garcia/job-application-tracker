from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

bp = Blueprint("errors", __name__)


@bp.app_errorhandler(404)
def not_found(_exc: HTTPException):
    """Render the 404 page for unknown URLs and abort(404) in any blueprint"""
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def server_error(_exc: Exception):
    """Render the 500 page for unhandled exceptions (debug mode shows the debugger instead)"""
    return render_template("errors/500.html"), 500
