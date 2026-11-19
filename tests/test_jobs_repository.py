from datetime import date
from typing import Any

import mysql.connector
import pytest
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

from jot.models import JobForm, JobType
from jot.repositories.jobs import JobRepository


def _form(**overrides: Any) -> JobForm:
    """A valid JobForm for Quiet Harbor Partners (22), which has no jobs in the seed"""
    return JobForm.model_validate(
        {
            "company_id": 22,
            "job_title": "Treasury Systems Developer",
            "job_type": "Full-time",
            "salary_min": "95000",
            "salary_max": "120000",
            "job_url": "https://quietharbor.example/careers/treasury-systems",
            "date_posted": "2026-11-15",
            "requirements": "Python, SQL, Excel",
            **overrides,
        }
    )


def test_list_all_returns_newest_postings_first(cursor: MySQLCursorAbstract) -> None:
    """list_all returns every seeded job with its company name, newest date_posted first and undated last"""
    repo = JobRepository(cursor)
    jobs = repo.list_all()

    assert len(jobs) >= 54
    assert all(job.company_name for job in jobs)

    posted = [job.date_posted for job in jobs]
    assert posted == sorted(posted, key=lambda d: (d is not None, d or date.min), reverse=True)


def test_list_all_filters_by_title_or_company(cursor: MySQLCursorAbstract) -> None:
    """list_all matches substrings in either job_title or the joined company_name"""
    repo = JobRepository(cursor)

    by_title = repo.list_all(search="Penetration")
    assert [job.job_id for job in by_title] == [24]

    # Fogline Robotics (15) has jobs 38 and 39
    by_company = repo.list_all(search="Fogline")
    assert sorted(job.job_id for job in by_company) == [38, 39]

    whitespace_only = repo.list_all(search="   ")
    assert len(whitespace_only) == len(repo.list_all())


def test_get_by_id_found_and_missing(cursor: MySQLCursorAbstract) -> None:
    """get_by_id returns a JobRow with decoded requirements and company_name, or None when missing"""
    repo = JobRepository(cursor)

    found = repo.get_by_id(1)
    assert found is not None
    assert found.job_title == "Software Developer"
    assert found.company_name == "TechCorp"
    assert found.job_type is JobType.FULL_TIME
    assert found.date_posted == date(2026, 10, 14)
    assert found.requirements == ["Python", "SQL", "Flask"]

    assert repo.get_by_id(999_999) is None


def test_create_and_fetch_job(cursor: MySQLCursorAbstract) -> None:
    """create inserts a job and returns its generated primary key"""
    repo = JobRepository(cursor)

    new_id = repo.create(_form())
    assert new_id is not None

    created = repo.get_by_id(new_id)
    assert created is not None
    assert created.job_title == "Treasury Systems Developer"
    assert created.company_name == "Quiet Harbor Partners"
    assert (created.salary_min, created.salary_max) == (95000, 120000)
    assert created.requirements == ["Python", "SQL", "Excel"]


def test_update_job(cursor: MySQLCursorAbstract) -> None:
    """update modifies all editable fields and returns False for unknown IDs"""
    repo = JobRepository(cursor)
    form = _form(
        company_id=1,
        job_title="Senior Frontend Engineer",
        job_type="Contract",
        salary_min="",
        salary_max="",
        requirements="",
    )

    # Seed job 3 (TechCorp Frontend Engineer) has no applications
    assert repo.update(3, form) is True
    updated = repo.get_by_id(3)
    assert updated is not None
    assert updated.job_title == "Senior Frontend Engineer"
    assert updated.job_type is JobType.CONTRACT
    assert updated.salary_min is None
    assert updated.requirements is None

    assert repo.update(999_999, form) is False


def test_create_or_update_with_unknown_company_raises_1452(cursor: MySQLCursorAbstract) -> None:
    """create and update raise IntegrityError 1452 when company_id references no company"""
    repo = JobRepository(cursor)
    form = _form(company_id=999_999)

    with pytest.raises(mysql.connector.IntegrityError) as created:
        repo.create(form)
    assert created.value.errno == errorcode.ER_NO_REFERENCED_ROW_2

    with pytest.raises(mysql.connector.IntegrityError) as updated:
        repo.update(3, form)
    assert updated.value.errno == errorcode.ER_NO_REFERENCED_ROW_2


def test_delete_job_without_applications(cursor: MySQLCursorAbstract) -> None:
    """delete removes a job with no applications and returns False once it is gone"""
    repo = JobRepository(cursor)

    # Seed job 38 (Fogline Robotics) has no applications
    assert repo.delete(38) is True
    assert repo.get_by_id(38) is None
    assert repo.delete(38) is False


def test_delete_job_with_applications_raises_1451(cursor: MySQLCursorAbstract) -> None:
    """delete raises IntegrityError 1451 when applications still reference the job (ON DELETE RESTRICT)"""
    repo = JobRepository(cursor)

    # Seed job 1 (TechCorp Software Developer) has application 1
    with pytest.raises(mysql.connector.IntegrityError) as exc_info:
        repo.delete(1)
    assert exc_info.value.errno == errorcode.ER_ROW_IS_REFERENCED_2
