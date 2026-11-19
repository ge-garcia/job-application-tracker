import pytest
from pydantic import ValidationError

from jot.models import ContactForm, ContactNotesForm

VALID = {"company_id": "1", "contact_name": "Dana Whitfield"}
LINKEDIN = "https://www.linkedin.com/in/"
# 64-character local part (the RFC maximum) plus a domain padded to the column's 100 characters
EMAIL_LOCAL = "d" * 64 + "@"


@pytest.mark.parametrize(
    ("field", "valid", "invalid"),
    [
        pytest.param("company_id", "1", "0", id="company_id-positive"),
        pytest.param("contact_name", "Kalani", "  ", id="contact_name-required"),
        pytest.param("contact_name", "N" * 100, "N" * 101, id="contact_name-max-length"),
        pytest.param("email", "dana@techcorp.example", "dana-at-techcorp", id="email-format"),
        pytest.param(
            "email",
            EMAIL_LOCAL + "e" * 27 + ".example",
            EMAIL_LOCAL + "e" * 28 + ".example",
            id="email-max-length",
        ),
        pytest.param("phone", "P" * 20, "P" * 21, id="phone-max-length"),
        pytest.param("title", "T" * 100, "T" * 101, id="title-max-length"),
        pytest.param("linkedin_url", LINKEDIN + "dana", "linkedin.com/in/dana", id="linkedin_url-http"),
        pytest.param(
            "linkedin_url", LINKEDIN.ljust(200, "a"), LINKEDIN.ljust(201, "a"), id="linkedin_url-max-length"
        ),
    ],
)
def test_contact_form_field_validators(field: str, valid: str, invalid: str) -> None:
    """Each field validator accepts a valid value and rejects an invalid one on that field alone"""
    ContactForm.model_validate({**VALID, field: valid})

    with pytest.raises(ValidationError) as exc_info:
        ContactForm.model_validate({**VALID, field: invalid})
    assert [err["loc"] for err in exc_info.value.errors()] == [(field,)]


def test_contact_form_to_params() -> None:
    """to_params produces a complete dictionary with blanks as None"""
    form = ContactForm.model_validate(
        {**VALID, "email": " dana@techcorp.example ", "phone": "", "notes": "  "}
    )

    assert form.to_params() == {
        "company_id": 1,
        "contact_name": "Dana Whitfield",
        "email": "dana@techcorp.example",
        "phone": None,
        "title": None,
        "linkedin_url": None,
        "notes": None,
    }


def test_contact_notes_form_normalizes_blank_notes() -> None:
    """Blank notes normalize to None while preserving multi-line text"""
    cleared = ContactNotesForm.model_validate({"notes": "   "})
    assert cleared.to_params() == {"notes": None}

    kept = ContactNotesForm.model_validate({"notes": "  Line 1\nLine 2  "})
    assert kept.to_params() == {"notes": "Line 1\nLine 2"}
