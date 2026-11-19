from flask import Blueprint, render_template

bp = Blueprint("dashboard", __name__)


@bp.get("/")
def index():
    """Render the dashboard"""
    return render_template("dashboard.html")
