from datetime import date
from typing import Any

import pytest
from pydantic import ValidationError

from jot.models import ApplicationForm, ApplicationStatusForm

VALID = {"job_id": "1", "application_date": "2026-11-01"}
ROUND = {"type": "Phone screen", "scheduled_at": "2026-11-20T10:00:00"}


def _with_round(**round_fields: Any) -> dict[str, Any]:
    """A valid application payload holding one interview round"""
    return {**VALID, "interview_data": {"rounds": [{**ROUND, **round_fields}]}}


@pytest.mark.parametrize(
    ("field", "valid", "invalid"),
    [
        pytest.param("job_id", "1", "0", id="job_id-positive"),
        pytest.param("application_date", "2026-11-01", "2026-02-30", id="application_date-date"),
        pytest.param("status", "Interview", "Interviewing", id="status-enum"),
        pytest.param("resume_version", "v" * 50, "v" * 51, id="resume_version-max-length"),
        pytest.param("cover_letter_sent", "on", "maybe", id="cover_letter_sent-bool"),
        pytest.param("interview_data", {"rounds": []}, ["Phone screen"], id="interview_data-object"),
    ],
)
def test_application_form_field_validators(field: str, valid: object, invalid: object) -> None:
    """Each field validator accepts a valid value and rejects an invalid one on that field alone"""
    ApplicationForm.model_validate({**VALID, field: valid})

    with pytest.raises(ValidationError) as exc_info:
        ApplicationForm.model_validate({**VALID, field: invalid})
    assert [err["loc"] for err in exc_info.value.errors()] == [(field,)]


@pytest.mark.parametrize(
    ("field", "valid", "invalid"),
    [
        pytest.param("type", "Technical", " ", id="type-required"),
        pytest.param("type", "T" * 50, "T" * 51, id="type-max-length"),
        pytest.param("scheduled_at", "2026-11-20T10:00:00", "next Tuesday", id="scheduled_at-datetime"),
        pytest.param("format", "Video", "F" * 51, id="format-max-length"),
        pytest.param("interviewers", ["Renee Castillo"], 42, id="interviewers-list"),
        pytest.param("outcome", "Passed", "Won", id="outcome-enum"),
    ],
)
def test_interview_round_field_validators(field: str, valid: object, invalid: object) -> None:
    """Each interview round validator accepts a valid value and rejects an invalid one on that field alone"""
    ApplicationForm.model_validate(_with_round(**{field: valid}))

    with pytest.raises(ValidationError) as exc_info:
        ApplicationForm.model_validate(_with_round(**{field: invalid}))
    assert [err["loc"] for err in exc_info.value.errors()] == [("interview_data", "rounds", 0, field)]


def test_interview_round_parses_interviewers() -> None:
    """Comma separated interviewers are stripped and split, and None becomes an empty list"""
    form = ApplicationForm.model_validate(_with_round(interviewers=" Renee Castillo, , Omar Haddad "))
    assert form.interview_data is not None
    assert form.interview_data.rounds[0].interviewers == ["Renee Castillo", "Omar Haddad"]

    cleared = ApplicationForm.model_validate(_with_round(interviewers=None))
    assert cleared.interview_data is not None
    assert cleared.interview_data.rounds[0].interviewers == []


def test_application_form_to_params() -> None:
    """to_params stores the status value and blanks as None"""
    form = ApplicationForm.model_validate({**VALID, "status": "Offer", "resume_version": "  "})

    assert form.to_params() == {
        "job_id": 1,
        "application_date": date(2026, 11, 1),
        "status": "Offer",
        "resume_version": None,
        "cover_letter_sent": False,
        "interview_data": None,
    }


def test_application_status_form() -> None:
    """ApplicationStatusForm accepts a known status and rejects an unknown one"""
    assert ApplicationStatusForm.model_validate({"status": "Offer"}).to_params() == {"status": "Offer"}

    with pytest.raises(ValidationError):
        ApplicationStatusForm.model_validate({"status": "Hired"})
