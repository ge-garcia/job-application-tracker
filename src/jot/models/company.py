from pydantic import BaseModel, Field, HttpUrl, field_validator

from jot.models.validation import sanitize_empty_string


class CompanyBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=100)
    industry: str | None = Field(None, max_length=50)
    website: HttpUrl | None = Field(None, max_length=200)
    city: str | None = Field(None, max_length=50)
    state: str | None = Field(None, max_length=50)
    notes: str | None = None

    @field_validator("website", mode="before")
    def clean_website(cls, v):
        return sanitize_empty_string(v)


class CompanyCreate(CompanyBase):
    """Payload for creating a new company. Body ommitted since only CompanyBase is needed"""


class CompanyUpdate(BaseModel):
    company_name: str | None = Field(None, min_length=1, max_length=100)
    industry: str | None = Field(None, max_length=50)
    website: HttpUrl | None = Field(None, max_length=200)
    city: str | None = Field(None, max_length=50)
    state: str | None = Field(None, max_length=50)
    notes: str | None = None

    @field_validator("website", mode="before")
    def clean_website(cls, v):
        return sanitize_empty_string(v)


class CompanyResponse(CompanyBase):
    company_id: int = Field(..., gt=0, description="PK cannot be null")
