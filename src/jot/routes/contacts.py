from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from pydantic import ValidationError

from jot.db import commit_db, get_cursor
from jot.models import ContactForm, ContactRow
from jot.repositories.companies import CompanyRepository
from jot.repositories.contacts import ContactRepository
from jot.routes.base import format_validation_errors

bp = Blueprint("contacts", __name__, url_prefix="/contacts")

# Swap for "contacts.html" once the page template exists
TEMPLATE = "_stubs/contacts.html"


def _repo() -> ContactRepository:
    """Build a request-scoped ContactRepository"""
    return ContactRepository(get_cursor())


def _get_or_404(contact_id: int) -> ContactRow:
    """Fetch a contact by primary key, aborting with 404 when it does not exist"""
    contact = _repo().get_by_id(contact_id)
    if contact is None:
        abort(404)
    return contact


def _render_form(contact: ContactRow | None, status: int = 200, **context: Any):
    """Render the create (contact=None) or edit form with its company options"""
    return (
        render_template(
            TEMPLATE,
            mode="form",
            contact=contact,
            companies=CompanyRepository(get_cursor()).list_summaries(),
            **context,
        ),
        status,
    )


@bp.get("/")
def index():
    """Render the contacts directory with optional search filtering"""
    search = request.args.get("q", "").strip() or None
    contacts = _repo().list_all(search=search)

    return render_template(
        TEMPLATE,
        mode="list",
        contacts=contacts,
        search=search or "",
    )


@bp.get("/new")
def new():
    """Render the create contact form"""
    return _render_form(None)


@bp.get("/<int:contact_id>")
def detail(contact_id: int):
    """Render a single contact"""
    return render_template(
        TEMPLATE,
        mode="detail",
        contact=_get_or_404(contact_id),
    )


@bp.get("/<int:contact_id>/edit")
def edit(contact_id: int):
    """Render the edit contact form"""
    return _render_form(_get_or_404(contact_id))


@bp.post("/")
def create():
    """Validate and insert a new contact"""
    try:
        form = ContactForm.model_validate(request.form)
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return _render_form(None, 422, form_data=request.form)

    new_id = _repo().create(form)
    commit_db()
    flash(f"Added {form.contact_name}", "success")
    return redirect(url_for("contacts.detail", contact_id=new_id))


@bp.post("/<int:contact_id>")
def update(contact_id: int):
    """Validate and update an existing contact"""
    contact = _get_or_404(contact_id)
    try:
        form = ContactForm.model_validate(request.form)
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return _render_form(contact, 422, form_data=request.form)

    # Existence is checked above: MySQL reports 0 affected rows when nothing changed
    _repo().update(contact_id, form)
    commit_db()
    flash(f"Updated {form.contact_name}", "success")
    return redirect(url_for("contacts.detail", contact_id=contact_id))


@bp.post("/<int:contact_id>/delete")
def delete(contact_id: int):
    """Delete a contact (no other table references contacts)"""
    if not _repo().delete(contact_id):
        abort(404)

    commit_db()
    flash("Contact deleted", "success")
    return redirect(url_for("contacts.index"))
