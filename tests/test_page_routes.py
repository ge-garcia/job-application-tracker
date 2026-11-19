import pytest
from flask.testing import FlaskClient
from mysql.connector.abstracts import MySQLCursorAbstract


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/jobs/",
        "/jobs/?q=Fogline",
        "/jobs/1",
        "/jobs/53",
        "/jobs/new",
        "/jobs/1/edit",
        "/applications/",
        "/applications/1",
        "/applications/20",
        "/applications/new",
        "/applications/1/edit",
        "/contacts/",
        "/contacts/1",
        "/contacts/new",
        "/contacts/1/edit",
        "/match/",
        "/match/?skills=python,sql",
    ],
)
def test_page_renders(client: FlaskClient, path: str) -> None:
    """Every page view renders against the seed data"""
    res = client.get(path)
    assert res.status_code == 200
    assert b"<main" in res.data


def test_job_detail_shows_chips_and_salary(client: FlaskClient) -> None:
    """A job's requirements render as chips, and its salary as a range left out when unset"""
    res = client.get("/jobs/1")
    assert b'<span class="chip">Flask</span>' in res.data
    assert b"$85,000 to $105,000" in res.data

    # Seed job 53 has every optional column NULL
    bare = client.get("/jobs/53")
    assert b"<dt>Salary</dt>" not in bare.data


def test_job_edit_form_joins_requirements(client: FlaskClient) -> None:
    """The edit form shows stored requirements as comma-separated text"""
    res = client.get("/jobs/1/edit")
    assert b'value="Python, SQL, Flask"' in res.data
    assert b'<option value="Full-time" selected>Full-time</option>' in res.data


def test_application_detail_lists_rounds(client: FlaskClient) -> None:
    """Interview rounds render read-only, and an empty interview_data object shows the empty state"""
    res = client.get("/applications/1")
    assert b"Technical Screen" in res.data
    assert b"2026-10-28 14:00" in res.data
    assert b'<span class="chip chip-gr">Passed</span>' in res.data

    empty = client.get("/applications/20")
    assert b"No interview rounds yet" in empty.data


def test_application_edit_form_selects_stored_values(client: FlaskClient) -> None:
    """Status and the cover letter flag preselect from the stored row"""
    res = client.get("/applications/1/edit")
    assert b'<option value="Interview" selected>Interview</option>' in res.data
    assert b'<option value="true" selected>Yes</option>' in res.data


def test_contact_detail_links_email_and_linkedin(client: FlaskClient) -> None:
    """A contact's email and LinkedIn URL render as links, beside its company name"""
    res = client.get("/contacts/1")
    assert b'href="mailto:dana.whitfield@techcorp.example"' in res.data
    assert b'href="https://www.linkedin.com/in/dana-whitfield-3a91b2"' in res.data
    assert b"TechCorp" in res.data


def test_dashboard_shows_stats_and_recent_applications(client: FlaskClient) -> None:
    """The dashboard has stat cards, status counts, and the 5 newest applications"""
    res = client.get("/")
    assert b"Applications by status" in res.data
    assert b'<dt class="stat-label">Interviewing</dt>' in res.data
    assert res.data.count(b'class="row-actions"') == 5
    assert b"View all applications" in res.data


def test_match_ranks_jobs_for_skills(client: FlaskClient) -> None:
    """GET /match/?skills= ranks the specification's examples and keeps the typed skills"""
    res = client.get("/match/?skills=Python, SQL, Flask")
    assert res.status_code == 200
    assert b'value="Python, SQL, Flask"' in res.data
    assert res.data.index(b"Software Developer") < res.data.index(b"Missing: Tableau")

    assert b"Add your skills" in client.get("/match/").data
    assert b"No matching jobs" in client.get("/match/?skills=zzz-no-such-skill").data


def test_unknown_pages_render_404(client: FlaskClient) -> None:
    """Unknown URLs and abort(404) both render the 404 template"""
    for path in ("/no-such-page", "/jobs/999999", "/applications/999999", "/contacts/999999"):
        res = client.get(path)
        assert res.status_code == 404
        assert b"Page not found" in res.data
        assert b"Back to dashboard" in res.data


@pytest.mark.parametrize(
    ("path", "data", "kept"),
    [
        (
            "/jobs/",
            {"company_id": "2", "job_title": "Typed title", "salary_min": "900", "salary_max": "100"},
            [b'value="Typed title"', b'<option value="2" selected>', b'value="900"'],
        ),
        (
            "/applications/",
            {"job_id": "5", "application_date": "", "status": "Offer", "resume_version": "typed-resume"},
            [b'value="typed-resume"', b'<option value="Offer" selected>', b'<option value="5" selected>'],
        ),
        (
            "/contacts/",
            {"company_id": "3", "contact_name": 'Typed "Quote"', "email": "not-an-email"},
            [b'value="Typed &#34;Quote&#34;"', b'value="not-an-email"', b'<option value="3" selected>'],
        ),
    ],
)
def test_invalid_form_rerenders_with_errors_and_values(
    client: FlaskClient, path: str, data: dict[str, str], kept: list[bytes]
) -> None:
    """An invalid create re-renders the form with status 422, flashed errors, and the typed values"""
    res = client.post(path, data=data)
    assert res.status_code == 422
    assert b"flash flash-error" in res.data
    for value in kept:
        assert value in res.data


def test_lists_render_empty_states_with_zero_rows(client: FlaskClient, cursor: MySQLCursorAbstract) -> None:
    """With every table emptied inside the test transaction, each list shows its empty state"""
    for table in ("applications", "jobs", "contacts", "companies"):
        cursor.execute(f"DELETE FROM {table}")

    assert b"No jobs yet" in client.get("/jobs/").data
    assert b"No applications yet" in client.get("/applications/").data
    assert b"No contacts yet" in client.get("/contacts/").data
    assert b"No matching jobs" in client.get("/match/?skills=python").data

    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert b"No applications yet" in dashboard.data
    assert b'<dd class="stat-value">0</dd>' in dashboard.data
