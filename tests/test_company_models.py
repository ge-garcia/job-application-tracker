import pytest
from pydantic import ValidationError

from jot.models import (
    CompanyForm,
    CompanyNotesForm,
    CompanyRow,
    CompanySummaryRow,
)
from jot.routes.base import format_validation_errors


def test_company_form_strips_and_normalizes_blanks() -> None:
    """Whitespace is stripped and empty strings become None"""
    form = CompanyForm.model_validate(
        {
            "company_name": "  Acme Corp  ",
            "industry": "   ",
            "website": "",
            "city": "  Miami ",
            "state": "\t\n",
            "notes": "  ",
        }
    )

    assert form.company_name == "Acme Corp"
    assert form.industry is None
    assert form.website is None
    assert form.city == "Miami"
    assert form.state is None
    assert form.notes is None


def test_company_form_requires_company_name() -> None:
    """Missing or whitespace-only company_name fails validation"""
    with pytest.raises(ValidationError):
        CompanyForm.model_validate({"company_name": "   "})

    with pytest.raises(ValidationError):
        CompanyForm.model_validate({})


def test_company_form_enforces_max_lengths() -> None:
    """Bounded VARCHAR fields reject strings exceeding schema limits"""
    with pytest.raises(ValidationError):
        CompanyForm.model_validate({"company_name": "A" * 101})

    with pytest.raises(ValidationError):
        CompanyForm.model_validate({"company_name": "Valid", "industry": "B" * 51})

    with pytest.raises(ValidationError):
        CompanyForm.model_validate(
            {
                "company_name": "Valid",
                "website": "https://example.com/" + ("a" * 185),
            }
        )


@pytest.mark.parametrize(
    "bad_url",
    [
        "not-a-url",
        "example.com",
        "ftp://files.example.com",
        "javascript:alert(1)",
    ],
)
def test_company_form_rejects_invalid_urls(bad_url: str) -> None:
    """Only valid http or https URLs are accepted for website"""
    with pytest.raises(ValidationError):
        CompanyForm.model_validate({"company_name": "Acme", "website": bad_url})


def test_company_form_to_params() -> None:
    """to_params produces a complete dictionary suitable for SQL bind parameters"""
    form = CompanyForm.model_validate(
        {
            "company_name": "TechCorp",
            "website": "https://www.techcorp.example",
        }
    )

    assert form.to_params() == {
        "company_name": "TechCorp",
        "industry": None,
        "website": "https://www.techcorp.example",
        "city": None,
        "state": None,
        "notes": None,
    }


def test_company_notes_form_normalizes_blank_notes() -> None:
    """Blank notes normalize to None while preserving multi-line text"""
    cleared = CompanyNotesForm.model_validate({"notes": "   "})
    assert cleared.to_params() == {"notes": None}

    kept = CompanyNotesForm.model_validate({"notes": "  Line 1\nLine 2  "})
    assert kept.to_params() == {"notes": "Line 1\nLine 2"}


def test_company_row_is_frozen_and_ignores_extra_columns() -> None:
    """CompanyRow and CompanySummaryRow are immutable and ignore unmapped JOIN columns"""
    raw = {
        "company_id": 1,
        "company_name": "TechCorp",
        "industry": "Software",
        "website": "https://www.techcorp.example",
        "city": "Miami",
        "state": "FL",
        "notes": "Product shop",
        "job_count": 4,
    }

    row = CompanyRow.from_row(raw)
    assert row.company_id == 1
    assert row.company_name == "TechCorp"
    assert not hasattr(row, "job_count")

    with pytest.raises(ValidationError):
        row.company_name = "Mutated"  # type: ignore[misc]

    summary = CompanySummaryRow.from_row(raw)
    assert summary.company_id == 1
    assert summary.company_name == "TechCorp"
    assert summary.industry == "Software"
    assert not hasattr(summary, "city")


def test_format_validation_errors() -> None:
    """format_validation_errors flattens Pydantic field paths into readable strings"""
    with pytest.raises(ValidationError) as exc_info:
        CompanyForm.model_validate({"company_name": "", "website": "not-a-url"})

    messages = format_validation_errors(exc_info.value)
    assert len(messages) == 2
    assert any(msg.startswith("company_name:") for msg in messages)
    assert any(msg.startswith("website:") for msg in messages)
