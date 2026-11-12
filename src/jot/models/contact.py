from pydantic import BaseModel, EmailStr, Field, field_validator

from jot.models.validation import FormModel, RowModel, check_http_url


class ContactFields(BaseModel):
    """Shared schema columns for a professional contact."""

    company_id: int
    contact_name: str
    email: str | None = None
    phone: str | None = None
    title: str | None = None
    linkedin_url: str | None = None
    notes: str | None = None


class ContactForm(FormModel, ContactFields):
    """Validated form payload for creating or updating a contact"""

    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    contact_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    title: str | None = Field(None, max_length=100)
    linkedin_url: str | None = Field(None, max_length=200)

    _linkedin_url_valid = field_validator("linkedin_url")(check_http_url)


class ContactNotesForm(FormModel):
    """Targeted payload for updating only a contact's notes"""

    notes: str | None = None


class ContactRow(RowModel, ContactFields):
    """Immutable database row representation of a contact"""

    contact_id: int
    company_name: str | None = None
