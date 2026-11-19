import contextlib
import json
from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from pydantic import ValidationError

from jot.db import commit_db, get_cursor
from jot.models import ApplicationForm, ApplicationRow, ApplicationStatus
from jot.repositories.applications import ApplicationRepository
from jot.repositories.jobs import JobRepository
from jot.routes.base import format_validation_errors

bp = Blueprint("applications", __name__, url_prefix="/applications")

TEMPLATE = "applications.html"


def _repo() -> ApplicationRepository:
    """Build a request-scoped ApplicationRepository"""
    return ApplicationRepository(get_cursor())


def _get_or_404(application_id: int) -> ApplicationRow:
    """Fetch an application by primary key, aborting with 404 when it does not exist"""
    application = _repo().get_by_id(application_id)
    if application is None:
        abort(404)
    return application


def _form_payload(application: ApplicationRow | None = None) -> dict[str, Any]:
    """
    request.form as ApplicationForm input. interview_data is posted as JSON text, and an edit form
    that leaves the field out keeps the stored rounds rather than clearing them
    """
    payload: dict[str, Any] = request.form.to_dict()
    raw = payload.get("interview_data")
    if raw is None and application is not None:
        payload["interview_data"] = application.interview_data
    elif raw and raw.strip():
        # Undecodable text is left as-is so validation reports it
        with contextlib.suppress(json.JSONDecodeError):
            payload["interview_data"] = json.loads(raw)
    return payload


def _render_form(application: ApplicationRow | None, status: int = 200, **context: Any):
    """Render the create (application=None) or edit form with its job and status options"""
    return (
        render_template(
            TEMPLATE,
            mode="form",
            application=application,
            jobs=JobRepository(get_cursor()).list_all(),
            statuses=list(ApplicationStatus),
            **context,
        ),
        status,
    )


@bp.get("/")
def index():
    """Render the applications list with optional search filtering"""
    search = request.args.get("q", "").strip() or None
    applications = _repo().list_all(search=search)

    return render_template(
        TEMPLATE,
        mode="list",
        applications=applications,
        search=search or "",
    )


@bp.get("/new")
def new():
    """Render the create application form"""
    return _render_form(None)


@bp.get("/<int:application_id>")
def detail(application_id: int):
    """Render a single application"""
    return render_template(
        TEMPLATE,
        mode="detail",
        application=_get_or_404(application_id),
    )


@bp.get("/<int:application_id>/edit")
def edit(application_id: int):
    """Render the edit application form"""
    return _render_form(_get_or_404(application_id))


@bp.post("/")
def create():
    """Validate and insert a new application"""
    try:
        form = ApplicationForm.model_validate(_form_payload())
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return _render_form(None, 422, form_data=request.form)

    new_id = _repo().create(form)
    commit_db()
    flash("Application added", "success")
    return redirect(url_for("applications.detail", application_id=new_id))


@bp.post("/<int:application_id>")
def update(application_id: int):
    """Validate and update an existing application"""
    application = _get_or_404(application_id)
    try:
        form = ApplicationForm.model_validate(_form_payload(application))
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return _render_form(application, 422, form_data=request.form)

    # Existence is checked above: MySQL reports 0 affected rows when nothing changed
    _repo().update(application_id, form)
    commit_db()
    flash("Application updated", "success")
    return redirect(url_for("applications.detail", application_id=application_id))


@bp.post("/<int:application_id>/delete")
def delete(application_id: int):
    """Delete an application (no other table references applications)"""
    if not _repo().delete(application_id):
        abort(404)

    commit_db()
    flash("Application deleted", "success")
    return redirect(url_for("applications.index"))
