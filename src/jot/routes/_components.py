from flask import flash, render_template


def components():
    """Render every partial macro on one page, to compare against assets/figma/components.png"""
    flash("Saved.", "success")
    flash("Cannot delete company while jobs still reference it", "error")
    return render_template("_components.html")
