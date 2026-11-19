import mysql.connector
from flask import Blueprint, flash, redirect, render_template, request, url_for
from pydantic import ValidationError

from jot.db import commit_db, get_cursor
from jot.models import CompanyForm, CompanyNotesForm
from jot.repositories.companies import CompanyRepository
from jot.routes.base import format_validation_errors

bp = Blueprint("companies", __name__, url_prefix="/companies")

# TODO: Add templates


def _repo() -> CompanyRepository:
    """Build a request-scoped CompanyRepository"""
    return CompanyRepository(get_cursor())


@bp.get("/")
def index():
    """Render the companies directory with optional search filtering"""
    search = request.args.get("q", "").strip() or None
    repo = _repo()
    companies = repo.list_all(search=search)

    return render_template(
        "companies.html",
        companies=companies,
        search=search or "",
        selected_company=None,
    )


@bp.get("/<int:company_id>")
def detail(company_id: int):
    """Render the companies page parameterized with a selected company"""
    repo = _repo()
    company = repo.get_by_id(company_id)
    if company is None:
        flash("Company not found", "error")
        return redirect(url_for("companies.index"))

    return render_template(
        "companies.html",
        companies=repo.list_all(),
        search="",
        selected_company=company,
    )


@bp.post("/")
def create():
    """Validate and insert a new company"""
    repo = _repo()
    try:
        form = CompanyForm.model_validate(request.form)
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return (
            render_template(
                "companies.html",
                companies=repo.list_all(),
                search="",
                selected_company=None,
                form_data=request.form,
            ),
            422,
        )

    new_id = repo.create(form)
    commit_db()
    flash(f"Added {form.company_name}", "success")
    return redirect(url_for("companies.detail", company_id=new_id))


@bp.post("/<int:company_id>")
def update(company_id: int):
    """Validate and update an existing company"""
    repo = _repo()
    try:
        form = CompanyForm.model_validate(request.form)
    except ValidationError as exc:
        for msg in format_validation_errors(exc):
            flash(msg, "error")
        return (
            render_template(
                "companies.html",
                companies=repo.list_all(),
                search="",
                selected_company=repo.get_by_id(company_id),
                form_data=request.form,
            ),
            422,
        )

    if not repo.update(company_id, form):
        flash("Company not found", "error")
        return redirect(url_for("companies.index"))

    commit_db()
    flash(f"Updated {form.company_name}", "success")
    return redirect(url_for("companies.detail", company_id=company_id))


@bp.post("/<int:company_id>/notes")
def update_notes(company_id: int):
    """Update only the notes field for a company"""
    repo = _repo()
    form = CompanyNotesForm.model_validate(request.form)

    if not repo.update_notes(company_id, form):
        flash("Company not found", "error")
        return redirect(url_for("companies.index"))

    commit_db()
    flash("Notes saved", "success")
    return redirect(url_for("companies.detail", company_id=company_id))


@bp.post("/<int:company_id>/delete")
def delete(company_id: int):
    """Delete a company if no jobs reference it"""
    repo = _repo()
    try:
        deleted = repo.delete(company_id)
    except mysql.connector.IntegrityError:
        flash("Cannot delete company while jobs still reference it", "error")
        return redirect(url_for("companies.detail", company_id=company_id))

    if not deleted:
        flash("Company not found", "error")
        return redirect(url_for("companies.index"))

    commit_db()
    flash("Company deleted", "success")
    return redirect(url_for("companies.index"))
