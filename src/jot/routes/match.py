from flask import Blueprint, render_template, request

from jot.db import get_cursor
from jot.repositories.jobs import JobRepository
from jot.services.match import parse_skills, rank_jobs

bp = Blueprint("match", __name__, url_prefix="/match")


@bp.get("/")
def index():
    """Rank saved jobs against the comma-separated skills in ?skills="""
    skills = parse_skills(request.args.get("skills", ""))
    results = rank_jobs(skills, JobRepository(get_cursor()).list_all()) if skills else []

    return render_template(
        "match.html",
        skills=skills,
        results=results,
    )
