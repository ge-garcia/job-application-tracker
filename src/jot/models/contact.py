from pydantic import BaseModel, EmailStr, Field, HttpUrl

from jot.models.validation import FormModel, RowModel


class ContactFields(BaseModel):
    """Shared schema columns for a professional contact."""

    company_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    job_title: str | None = None
    linkedin_url: str | None = None
    notes: str | None = None


class ContactForm(FormModel, ContactFields):
    """Validated form payload for creating or updating a contact"""

    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    job_title: str | None = Field(None, max_length=100)
    linkedin_url: HttpUrl | None = Field(None, max_length=200)


class ContactNotesForm(FormModel):
    """Targeted payload for updating only a contact's notes"""

    notes: str | None = None


class ContactRow(RowModel, ContactFields):
    """Immutable database row representation of a contact"""

    contact_id: int
    company_name: str | None = None
