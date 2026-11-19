from typing import Any

import mysql.connector
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from mysql.connector import errorcode
from pydantic import ValidationError

from jot.db import commit_db, get_cursor
from jot.models import JobForm, JobRow, JobType
from jot.repositories.companies import CompanyRepository
from jot.repositories.jobs import JobRepository
from jot.routes.base import format_validation_errors

bp = Blueprint("jobs", __name__, url_prefix="/jobs")

TEMPLATE = "jobs.html"


def _repo() -> JobRepository:
    """Build a request-scoped JobRepository"""
    return JobRepository(get_cursor())


def _get_or_404(job_id: int) -> JobRow:
    """Fetch a job by primary key, aborting with 404 when it does not exist"""
    job = _repo().get_by_id(job_id)
    if job is None:
        abort(404)
    return job


def _render_form(job: JobRow | None, status: int = 200, **context: Any):
    """Render the create (job=None) or edit form with its company and job type options"""
    return (
        render_template(
            TEMPLATE,
            mode="form",
            job=job,
            companies=CompanyRepository(get_cursor()).list_summaries(),
            job_types=list(JobType),
            **context,
        ),
        status,
    )


@bp.get("/")
def index():
    """Render the jobs list with optional search filtering"""
    search = request.args.get("q", "").strip() or None
    jobs = _repo().list_all(search=search)

    return render_template(
        TEMPLATE,
        mode="list",
        jobs=jobs,
        search=search or "",
    )


@bp.get("/new")
def new():
    """Render the create job form"""
    return _render_form(None)


@bp.get("/<int:job_id>")
def detail(job_id: int):
    """Render a single job"""
    return render_template(
        TEMPLATE,
        mode="detail",
        job=_get_or_404(job_id),
    )


@bp.get("/<int:job_id>/edit")
def edit(job_id: int):
    """Render the edit job form"""
    return _render_form(_get_or_404(job_id))


@bp.post("/")
def create():
    """Validate and insert a new job"""
    try:
        form = JobForm.model_validate(request.form)
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return _render_form(None, 422, form_data=request.form)

    new_id = _repo().create(form)
    commit_db()
    flash(f"Added {form.job_title}", "success")
    return redirect(url_for("jobs.detail", job_id=new_id))


@bp.post("/<int:job_id>")
def update(job_id: int):
    """Validate and update an existing job"""
    job = _get_or_404(job_id)
    try:
        form = JobForm.model_validate(request.form)
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return _render_form(job, 422, form_data=request.form)

    # Existence is checked above: MySQL reports 0 affected rows when nothing changed
    _repo().update(job_id, form)
    commit_db()
    flash(f"Updated {form.job_title}", "success")
    return redirect(url_for("jobs.detail", job_id=job_id))


@bp.post("/<int:job_id>/delete")
def delete(job_id: int):
    """Delete a job if no applications reference it"""
    try:
        deleted = _repo().delete(job_id)
    except mysql.connector.IntegrityError as exc:
        if exc.errno != errorcode.ER_ROW_IS_REFERENCED_2:
            raise
        flash("Cannot delete job while applications still reference it", "error")
        return redirect(url_for("jobs.detail", job_id=job_id))

    if not deleted:
        abort(404)

    commit_db()
    flash("Job deleted", "success")
    return redirect(url_for("jobs.index"))
