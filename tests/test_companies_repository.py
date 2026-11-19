import mysql.connector
import pytest
from mysql.connector.abstracts import MySQLCursorAbstract

from jot.models import CompanyForm, CompanyNotesForm
from jot.repositories.companies import CompanyRepository


def test_list_all_returns_sorted_companies(cursor: MySQLCursorAbstract) -> None:
    """list_all returns all seeded companies ordered alphabetically by company_name"""
    repo = CompanyRepository(cursor)
    companies = repo.list_all()

    assert len(companies) >= 26
    names = [c.company_name for c in companies]
    assert names == sorted(names, key=str.casefold)


def test_list_all_filters_by_name_or_industry(cursor: MySQLCursorAbstract) -> None:
    """list_all matches substrings in either company_name or industry"""
    repo = CompanyRepository(cursor)

    by_name = repo.list_all(search="Mangrove")
    assert [c.company_name for c in by_name] == ["Mangrove Financial"]

    by_industry = repo.list_all(search="Aerospace")
    assert [c.company_name for c in by_industry] == ["Palmetto Aerospace"]

    whitespace_only = repo.list_all(search="   ")
    assert len(whitespace_only) == len(repo.list_all())


def test_list_summaries_returns_lightweight_rows(cursor: MySQLCursorAbstract) -> None:
    """list_summaries returns CompanySummaryRow projections for select inputs"""
    repo = CompanyRepository(cursor)
    summaries = repo.list_summaries()

    assert len(summaries) >= 26
    first = next(s for s in summaries if s.company_id == 1)
    assert first.company_name == "TechCorp"
    assert first.industry == "Software"


def test_get_by_id_found_and_missing(cursor: MySQLCursorAbstract) -> None:
    """get_by_id returns a full CompanyRow when found and None when missing"""
    repo = CompanyRepository(cursor)

    found = repo.get_by_id(20)
    assert found is not None
    assert found.company_name == "Müller & Söhne Systemhaus GmbH"
    assert found.city == "München"

    assert repo.get_by_id(999_999) is None


def test_create_and_fetch_company(cursor: MySQLCursorAbstract) -> None:
    """create inserts a company and returns its generated primary key"""
    repo = CompanyRepository(cursor)
    form = CompanyForm.model_validate(
        {
            "company_name": "Biscayne Systems",
            "industry": "Cloud",
            "website": "https://biscaynesystems.example",
            "city": "Miami",
            "state": "FL",
            "notes": "Met at local PyData",
        }
    )

    new_id = repo.create(form)
    assert new_id is not None

    created = repo.get_by_id(new_id)
    assert created is not None
    assert created.company_name == "Biscayne Systems"
    assert created.website == "https://biscaynesystems.example"
    assert created.notes == "Met at local PyData"


def test_update_company(cursor: MySQLCursorAbstract) -> None:
    """update modifies all editable fields and returns False for unknown IDs"""
    repo = CompanyRepository(cursor)
    form = CompanyForm.model_validate(
        {
            "company_name": "Quiet Harbor Partners LLC",
            "industry": "Finance",
            "website": "https://quietharbor.example",
            "city": "Coral Gables",
            "state": "FL",
            "notes": "Updated record",
        }
    )

    assert repo.update(22, form) is True
    updated = repo.get_by_id(22)
    assert updated is not None
    assert updated.company_name == "Quiet Harbor Partners LLC"
    assert updated.city == "Coral Gables"

    assert repo.update(999_999, form) is False


def test_update_notes_only(cursor: MySQLCursorAbstract) -> None:
    """update_notes updates notes without altering other company columns"""
    repo = CompanyRepository(cursor)
    before = repo.get_by_id(3)
    assert before is not None

    assert repo.update_notes(3, CompanyNotesForm(notes="Followed up with Renee")) is True

    after = repo.get_by_id(3)
    assert after is not None
    assert after.notes == "Followed up with Renee"
    assert after.company_name == before.company_name
    assert after.website == before.website

    assert repo.update_notes(999_999, CompanyNotesForm(notes="No-op")) is False


def test_delete_unreferenced_company_and_cascade(cursor: MySQLCursorAbstract) -> None:
    """delete removes a company with no jobs and cascades to its contacts"""
    repo = CompanyRepository(cursor)

    # Seed company 22 has no jobs and no contacts
    assert repo.delete(22) is True
    assert repo.get_by_id(22) is None
    assert repo.delete(22) is False

    # Seed company 25 (Seagrape Ventures) has contacts (36, 37) and no jobs
    assert repo.delete(25) is True
    assert repo.get_by_id(25) is None
    cursor.execute("SELECT COUNT(*) AS cnt FROM contacts WHERE company_id = 25")
    row = cursor.fetchone()
    assert row is not None and row["cnt"] == 0


def test_delete_company_with_jobs_raises_integrity_error(
    cursor: MySQLCursorAbstract,
) -> None:
    """delete raises IntegrityError when jobs still reference the company (ON DELETE RESTRICT)"""
    repo = CompanyRepository(cursor)

    # Seed company 1 (TechCorp) has jobs 1-4
    with pytest.raises(mysql.connector.IntegrityError):
        repo.delete(1)
