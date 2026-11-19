from datetime import date, datetime
from typing import Any

import mysql.connector
import pytest
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

from jot.models import ApplicationForm, ApplicationStatus, ApplicationStatusForm
from jot.models.application import InterviewOutcome
from jot.repositories.applications import ApplicationRepository


def _form(**overrides: Any) -> ApplicationForm:
    """A valid ApplicationForm for job 3 (TechCorp Frontend Engineer), which has no seeded applications"""
    return ApplicationForm.model_validate(
        {
            "job_id": 3,
            "application_date": "2026-11-16",
            "status": "Interview",
            "resume_version": "frontend-v2",
            "cover_letter_sent": "1",
            "interview_data": {
                "rounds": [
                    {
                        "type": "Phone screen",
                        "scheduled_at": "2026-11-20T10:00:00",
                        "format": "Video",
                        "interviewers": "Dana Whitfield, Marcus Bell",
                        "outcome": "Passed",
                    }
                ]
            },
            **overrides,
        }
    )


def test_list_all_returns_newest_first(cursor: MySQLCursorAbstract) -> None:
    """list_all returns every seeded application with job and company names, newest application_date first"""
    repo = ApplicationRepository(cursor)
    applications = repo.list_all()

    assert len(applications) >= 43
    assert all(a.job_title and a.company_name for a in applications)

    dates = [a.application_date for a in applications]
    assert dates == sorted(dates, reverse=True)


def test_list_all_filters_by_job_title_or_company(cursor: MySQLCursorAbstract) -> None:
    """list_all matches substrings in either the joined job_title or company_name"""
    repo = ApplicationRepository(cursor)

    by_title = repo.list_all(search="Penetration")
    assert [a.application_id for a in by_title] == [19]

    # Lumen Retail Co. (11): applications 22 and 23 to job 27, 24 to job 28
    by_company = repo.list_all(search="Lumen")
    assert sorted(a.application_id for a in by_company) == [22, 23, 24]

    whitespace_only = repo.list_all(search="   ")
    assert len(whitespace_only) == len(repo.list_all())


def test_get_by_id_found_and_missing(cursor: MySQLCursorAbstract) -> None:
    """get_by_id returns an ApplicationRow with decoded interview_data and joined names, or None"""
    repo = ApplicationRepository(cursor)

    found = repo.get_by_id(1)
    assert found is not None
    assert found.job_title == "Software Developer"
    assert found.company_name == "TechCorp"
    assert found.status is ApplicationStatus.INTERVIEW
    assert found.cover_letter_sent is True
    assert found.interview_data is not None
    assert len(found.interview_data.rounds) == 3

    # Seed application 2 has no interview_data
    no_rounds = repo.get_by_id(2)
    assert no_rounds is not None
    assert no_rounds.interview_data is None

    assert repo.get_by_id(999_999) is None


def test_create_and_fetch_application(cursor: MySQLCursorAbstract) -> None:
    """create inserts an application, round-tripping interview_data through the JSON column"""
    repo = ApplicationRepository(cursor)

    new_id = repo.create(_form())
    assert new_id is not None

    created = repo.get_by_id(new_id)
    assert created is not None
    assert created.job_title == "Frontend Engineer"
    assert created.application_date == date(2026, 11, 16)
    assert created.cover_letter_sent is True
    assert created.interview_data is not None
    [round_one] = created.interview_data.rounds
    assert round_one.scheduled_at == datetime(2026, 11, 20, 10, 0)
    assert round_one.interviewers == ["Dana Whitfield", "Marcus Bell"]
    assert round_one.outcome is InterviewOutcome.PASSED


def test_update_application(cursor: MySQLCursorAbstract) -> None:
    """update modifies all editable fields and returns False for unknown IDs"""
    repo = ApplicationRepository(cursor)
    form = _form(job_id=7, status="Rejected", resume_version="", cover_letter_sent="0", interview_data=None)

    # Seed application 1 (job 1, Interview, three rounds)
    assert repo.update(1, form) is True
    updated = repo.get_by_id(1)
    assert updated is not None
    assert updated.job_title == "Business Intelligence Intern"
    assert updated.status is ApplicationStatus.REJECTED
    assert updated.resume_version is None
    assert updated.cover_letter_sent is False
    assert updated.interview_data is None

    assert repo.update(999_999, form) is False


def test_update_status_only(cursor: MySQLCursorAbstract) -> None:
    """update_status changes status without altering other application columns"""
    repo = ApplicationRepository(cursor)
    before = repo.get_by_id(5)
    assert before is not None

    assert repo.update_status(5, ApplicationStatusForm(status=ApplicationStatus.SCREENING)) is True

    after = repo.get_by_id(5)
    assert after is not None
    assert after.status is ApplicationStatus.SCREENING
    assert after.model_dump(exclude={"status"}) == before.model_dump(exclude={"status"})

    assert repo.update_status(999_999, ApplicationStatusForm(status=ApplicationStatus.OFFER)) is False


def test_create_or_update_with_unknown_job_raises_1452(cursor: MySQLCursorAbstract) -> None:
    """create and update raise IntegrityError 1452 when job_id references no job"""
    repo = ApplicationRepository(cursor)
    form = _form(job_id=999_999)

    with pytest.raises(mysql.connector.IntegrityError) as created:
        repo.create(form)
    assert created.value.errno == errorcode.ER_NO_REFERENCED_ROW_2

    with pytest.raises(mysql.connector.IntegrityError) as updated:
        repo.update(1, form)
    assert updated.value.errno == errorcode.ER_NO_REFERENCED_ROW_2


def test_delete_application(cursor: MySQLCursorAbstract) -> None:
    """delete removes an application and returns False once it is gone"""
    repo = ApplicationRepository(cursor)

    assert repo.delete(5) is True
    assert repo.get_by_id(5) is None
    assert repo.delete(5) is False
