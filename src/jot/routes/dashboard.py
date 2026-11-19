from flask import Blueprint, render_template

from jot.db import get_cursor
from jot.repositories.dashboard import DashboardRepository

bp = Blueprint("dashboard", __name__)


def _repo() -> DashboardRepository:
    """Build a request-scoped DashboardRepository"""
    return DashboardRepository(get_cursor())


@bp.get("/")
def index():
    """Render the dashboard: record totals, applications by status, and the 5 newest applications"""
    repo = _repo()

    return render_template(
        "dashboard.html",
        stats=repo.stats(),
        recent_applications=repo.recent_applications(limit=5),
    )
