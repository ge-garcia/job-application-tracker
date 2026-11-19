from flask import Blueprint, flash, render_template

bp = Blueprint("components", __name__, url_prefix="/_components")


@bp.get("/")
def components():
    """Render every partial macro on one page, to compare against assets/figma/components.png"""
    flash("Saved.", "success")
    flash("Cannot delete company while jobs still reference it", "error")
    return render_template("_components.html")
