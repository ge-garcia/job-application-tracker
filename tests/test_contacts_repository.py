from typing import Any

import mysql.connector
import pytest
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

from jot.models import ContactForm, ContactNotesForm
from jot.repositories.contacts import ContactRepository


def _form(**overrides: Any) -> ContactForm:
    """A valid ContactForm for Quiet Harbor Partners (22), which has no contacts in the seed"""
    return ContactForm.model_validate(
        {
            "company_id": 22,
            "contact_name": "Elena Marsh",
            "email": "elena.marsh@quietharbor.example",
            "phone": "(305) 555-0107",
            "title": "Head of Engineering",
            "linkedin_url": "https://www.linkedin.com/in/elena-marsh",
            "notes": "Met at Miami Tech Week",
            **overrides,
        }
    )


def test_list_all_returns_sorted_contacts(cursor: MySQLCursorAbstract) -> None:
    """list_all returns every seeded contact with its company name, ordered alphabetically by contact_name"""
    repo = ContactRepository(cursor)
    contacts = repo.list_all()

    assert len(contacts) >= 38
    assert all(c.company_name for c in contacts)
    names = [c.contact_name for c in contacts]
    assert names == sorted(names, key=str.casefold)


def test_list_all_filters_by_name_or_email(cursor: MySQLCursorAbstract) -> None:
    """list_all matches substrings in either contact_name or email"""
    repo = ContactRepository(cursor)

    # Seed has two contacts named Alex Kim, at DataCo (5) and Cascade Ridge Cloud (19)
    by_name = repo.list_all(search="Alex Kim")
    assert [c.contact_id for c in by_name] == [5, 19]

    by_email = repo.list_all(search="@cascaderidge")
    assert sorted(c.contact_id for c in by_email) == [19, 20, 21, 22, 23]

    whitespace_only = repo.list_all(search="   ")
    assert len(whitespace_only) == len(repo.list_all())


def test_get_by_id_found_and_missing(cursor: MySQLCursorAbstract) -> None:
    """get_by_id returns a ContactRow with its company_name when found and None when missing"""
    repo = ContactRepository(cursor)

    found = repo.get_by_id(13)
    assert found is not None
    assert found.contact_name == 'Robert "Bobby" Chen'
    assert found.company_name == "Palmetto Aerospace"

    assert repo.get_by_id(999_999) is None


def test_create_and_fetch_contact(cursor: MySQLCursorAbstract) -> None:
    """create inserts a contact and returns its generated primary key"""
    repo = ContactRepository(cursor)

    new_id = repo.create(_form())
    assert new_id is not None

    created = repo.get_by_id(new_id)
    assert created is not None
    assert created.contact_name == "Elena Marsh"
    assert created.company_name == "Quiet Harbor Partners"
    assert created.email == "elena.marsh@quietharbor.example"
    assert created.linkedin_url == "https://www.linkedin.com/in/elena-marsh"


def test_update_contact(cursor: MySQLCursorAbstract) -> None:
    """update modifies all editable fields and returns False for unknown IDs"""
    repo = ContactRepository(cursor)
    form = _form(company_id=16, contact_name="Pat Morgan", phone="", notes="")

    # Seed contact 26 (Lakeshore Insurance) has only a name
    assert repo.update(26, form) is True
    updated = repo.get_by_id(26)
    assert updated is not None
    assert updated.contact_name == "Pat Morgan"
    assert updated.title == "Head of Engineering"
    assert updated.phone is None
    assert updated.notes is None

    assert repo.update(999_999, form) is False


def test_update_notes_only(cursor: MySQLCursorAbstract) -> None:
    """update_notes updates notes without altering other contact columns"""
    repo = ContactRepository(cursor)
    before = repo.get_by_id(3)
    assert before is not None

    assert repo.update_notes(3, ContactNotesForm(notes="Referred me to Dana")) is True

    after = repo.get_by_id(3)
    assert after is not None
    assert after.notes == "Referred me to Dana"
    assert after.model_dump(exclude={"notes"}) == before.model_dump(exclude={"notes"})

    assert repo.update_notes(999_999, ContactNotesForm(notes="No-op")) is False


def test_create_or_update_with_unknown_company_raises_1452(cursor: MySQLCursorAbstract) -> None:
    """create and update raise IntegrityError 1452 when company_id references no company"""
    repo = ContactRepository(cursor)
    form = _form(company_id=999_999)

    with pytest.raises(mysql.connector.IntegrityError) as created:
        repo.create(form)
    assert created.value.errno == errorcode.ER_NO_REFERENCED_ROW_2

    with pytest.raises(mysql.connector.IntegrityError) as updated:
        repo.update(26, form)
    assert updated.value.errno == errorcode.ER_NO_REFERENCED_ROW_2


def test_delete_contact(cursor: MySQLCursorAbstract) -> None:
    """delete removes a contact and returns False once it is gone"""
    repo = ContactRepository(cursor)

    assert repo.delete(26) is True
    assert repo.get_by_id(26) is None
    assert repo.delete(26) is False
