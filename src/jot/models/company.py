from pydantic import BaseModel, Field, field_validator

from jot.models.validation import FormModel, RowModel, check_http_url


class CompanySummaryFields(BaseModel):
    """Minimal company columns for list views and dropdowns"""

    company_name: str
    industry: str | None = None


class CompanyFields(CompanySummaryFields):
    """Full schema columns for a company"""

    website: str | None = None
    city: str | None = None
    state: str | None = None
    notes: str | None = None


class CompanyForm(FormModel, CompanyFields):
    """Validated form payload for creating or updating a company"""

    company_name: str = Field(..., min_length=1, max_length=100)
    industry: str | None = Field(None, max_length=50)
    website: str | None = Field(None, max_length=200)
    city: str | None = Field(None, max_length=50)
    state: str | None = Field(None, max_length=50)

    _website_valid = field_validator("website")(check_http_url)


class CompanyNotesForm(FormModel):
    """Targeted payload for updating only a company's notes"""

    notes: str | None = None


class CompanySummaryRow(RowModel, CompanySummaryFields):
    """Lightweight immutable row for company directory tables or select inputs"""

    company_id: int


class CompanyRow(RowModel, CompanyFields):
    """Full immutable database row representation of a company"""

    company_id: int
