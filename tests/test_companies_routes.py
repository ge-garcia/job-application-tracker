from flask.testing import FlaskClient


def test_companies_index_and_search(client: FlaskClient) -> None:
    """GET /companies/ renders the directory and filters by query parameter q"""
    res = client.get("/companies/")
    assert res.status_code == 200
    assert b"TechCorp" in res.data
    assert b"Mangrove Financial" in res.data

    filtered = client.get("/companies/?q=Mangrove")
    assert filtered.status_code == 200
    assert b"Mangrove Financial" in filtered.data
    assert b"TechCorp" not in filtered.data


def test_company_detail_found_and_missing(client: FlaskClient) -> None:
    """GET /companies/<id> renders company details or redirects when missing"""
    res = client.get("/companies/1")
    assert res.status_code == 200
    assert b"TechCorp" in res.data
    assert b"Brickell" in res.data

    missing = client.get("/companies/999999", follow_redirects=True)
    assert missing.status_code == 200
    assert b"Company not found" in missing.data


def test_new_and_create_company_flow(client: FlaskClient) -> None:
    """GET /companies/new renders the create form and POST /companies/ inserts and redirects"""
    form_page = client.get("/companies/new")
    assert form_page.status_code == 200
    assert b"Add company" in form_page.data

    res = client.post(
        "/companies/",
        data={
            "company_name": "Coral Way Labs",
            "industry": "AI",
            "website": "https://coralwaylabs.example",
            "city": "Miami",
            "state": "FL",
            "notes": "Seed route test",
        },
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert b"Coral Way Labs" in res.data
    assert b"Added Coral Way Labs" in res.data


def test_create_company_validation_error_returns_422(client: FlaskClient) -> None:
    """Invalid POST /companies/ re-renders the form with status 422 and preserves input"""
    res = client.post(
        "/companies/",
        data={
            "company_name": "",
            "website": "not-a-valid-url",
            "city": "Miami",
        },
    )
    assert res.status_code == 422
    assert b"Miami" in res.data


def test_edit_and_update_company_flow(client: FlaskClient) -> None:
    """GET /companies/<id>/edit renders prefilled form and POST /companies/<id> updates record"""
    edit_page = client.get("/companies/22/edit")
    assert edit_page.status_code == 200
    assert b"Quiet Harbor Partners" in edit_page.data

    res = client.post(
        "/companies/22",
        data={
            "company_name": "Quiet Harbor Capital",
            "industry": "Finance",
            "website": "https://quietharbor.example",
            "city": "Miami",
            "state": "FL",
            "notes": "Updated via route",
        },
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert b"Quiet Harbor Capital" in res.data
    assert b"Updated Quiet Harbor Capital" in res.data


def test_update_notes_route(client: FlaskClient) -> None:
    """POST /companies/<id>/notes updates notes and flashes confirmation"""
    res = client.post(
        "/companies/3/notes",
        data={"notes": "Spoke with Renee Castillo"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert b"Spoke with Renee Castillo" in res.data
    assert b"Notes saved" in res.data


def test_delete_company_success_and_restricted(client: FlaskClient) -> None:
    """POST /companies/<id>/delete removes unreferenced companies and blocks those with jobs"""
    # Seed company 22 has no jobs or contacts
    ok = client.post("/companies/22/delete", follow_redirects=True)
    assert ok.status_code == 200
    assert b"Company deleted" in ok.data

    # Seed company 1 (TechCorp) has jobs (ON DELETE RESTRICT)
    blocked = client.post("/companies/1/delete", follow_redirects=True)
    assert blocked.status_code == 200
    assert b"Cannot delete company while jobs still reference it" in blocked.data
