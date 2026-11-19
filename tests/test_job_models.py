from datetime import date

import pytest
from pydantic import ValidationError

from jot.models import JobForm

VALID = {"company_id": "1", "job_title": "Software Developer"}
URL = "https://jobs.example/"


@pytest.mark.parametrize(
    ("field", "valid", "invalid"),
    [
        pytest.param("company_id", "1", "0", id="company_id-positive"),
        pytest.param("job_title", "Software Developer", "  ", id="job_title-required"),
        pytest.param("job_title", "D" * 100, "D" * 101, id="job_title-max-length"),
        pytest.param("job_type", "Internship", "Freelance", id="job_type-enum"),
        pytest.param("salary_min", "0", "-1", id="salary_min-non-negative"),
        pytest.param("salary_max", "0", "-1", id="salary_max-non-negative"),
        pytest.param("job_url", URL.ljust(300, "a"), URL.ljust(301, "a"), id="job_url-max-length"),
        pytest.param("job_url", "https://jobs.example/1", "ftp://jobs.example/1", id="job_url-http"),
        pytest.param("date_posted", "2026-10-14", "2026-13-01", id="date_posted-date"),
        pytest.param("requirements", "Python, SQL", 42, id="requirements-list"),
    ],
)
def test_job_form_field_validators(field: str, valid: object, invalid: object) -> None:
    """Each field validator accepts a valid value and rejects an invalid one on that field alone"""
    JobForm.model_validate({**VALID, field: valid})

    with pytest.raises(ValidationError) as exc_info:
        JobForm.model_validate({**VALID, field: invalid})
    assert [err["loc"] for err in exc_info.value.errors()] == [(field,)]


def test_job_form_parses_requirements() -> None:
    """Comma separated requirements are stripped and split, and an all-blank list becomes None"""
    form = JobForm.model_validate({**VALID, "requirements": " Python, SQL ,, Flask "})
    assert form.requirements == ["Python", "SQL", "Flask"]

    assert JobForm.model_validate({**VALID, "requirements": " , "}).requirements is None


def test_job_form_salary_range() -> None:
    """salary_max may equal salary_min but not fall below it"""
    fixed = JobForm.model_validate({**VALID, "salary_min": "41600", "salary_max": "41600"})
    assert (fixed.salary_min, fixed.salary_max) == (41600, 41600)

    with pytest.raises(ValidationError, match="salary_max must be greater than or equal to salary_min"):
        JobForm.model_validate({**VALID, "salary_min": "90000", "salary_max": "80000"})


def test_job_form_to_params() -> None:
    """to_params stores the enum value, blanks as None, and requirements as a JSON array"""
    form = JobForm.model_validate(
        {
            **VALID,
            "job_type": "Full-time",
            "salary_min": "",
            "job_url": "  ",
            "date_posted": "2026-10-14",
            "requirements": "Python, SQL",
        }
    )

    assert form.to_params() == {
        "company_id": 1,
        "job_title": "Software Developer",
        "job_type": "Full-time",
        "salary_min": None,
        "salary_max": None,
        "job_url": None,
        "date_posted": date(2026, 10, 14),
        "requirements": '["Python", "SQL"]',
    }
