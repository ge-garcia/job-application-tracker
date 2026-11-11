from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator

from jot.models.validation import sanitize_empty_string


class ContactBase(BaseModel):
    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    job_title: str | None = Field(None, max_length=100)
    linkedin_url: HttpUrl | None = Field(None, max_length=200)
    notes: str | None = None

    @field_validator("email", "linkedin_url", mode="before")
    def clean_strings(cls, v):
        return sanitize_empty_string(v)


class ContactCreate(ContactBase):
    """Payload for adding a contact. Body ommitted since only ContactBase is needed"""


class ContactUpdate(BaseModel):
    company_id: int | None = Field(None, gt=0)
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    job_title: str | None = Field(None, max_length=100)
    linkedin_url: HttpUrl | None = Field(None, max_length=200)
    notes: str | None = None

    @field_validator("email", "linkedin_url", mode="before")
    def clean_strings(cls, v):
        return sanitize_empty_string(v)


class ContactResponse(ContactBase):
    contact_id: int = Field(..., gt=0, description="Strictly required primary key")
