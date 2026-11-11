"""
Defines our types (and validates them) based on the tables defined in
`./src/schema.sql`. Besides the core models and enums translated from MySQL,
this module will be extended with type definitions for the table's JSON fields.
"""

from collections.abc import Callable
from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)


def validate_pair_rule(
    field1: str, field2: str, predicate: Callable[[Any, Any], bool], error_msg: str
):
    """
    Generic model validator decorator. Uses Python match/case to safely extract
    and narrow two optional fields before evaluating a rule predicate.
    """

    def decorator(cls):
        def validator(self):
            val1 = getattr(self, field1, None)
            val2 = getattr(self, field2, None)

            # Match extracts values when BOTH are non-None
            match (val1, val2):
                case (v1, v2) if v1 is not None and v2 is not None:
                    if not predicate(v1, v2):
                        raise ValueError(error_msg)
                case _:
                    pass
            return self

        # Attach as a Pydantic model_validator (mode="after")
        return model_validator(mode="after")(validator)

    return decorator


def sanitize_empty_string(val: Any) -> Any | None:
    """Helper for empty string cleanup inside field validators."""
    match val:
        case str() if not val.strip():
            return None
        case _:
            return val


# === Enums


class JobType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


@validate_pair_rule(
    field1="application_date",
    field2="response_date",
    predicate=lambda app_d, resp_d: resp_d >= app_d,
    error_msg="response_date cannot be earlier than application_date",
)
class ApplicationModel(BaseModel):
    application_id: int | None = Field(None, description="PK")
    job_id: int = Field(..., gt=0, description="FK referencing jobs.job_id")
    application_date: date
    status: ApplicationStatus = ApplicationStatus.APPLIED  # add sensible default
    resume_version: str | None = Field(None, max_length=50)
    cover_letter_sent: bool = False
    response_date: date | None = None
    # TODO: Design the type for the interview_data property, enforce validation on it
    interview_data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_interview_status(self):
        """Pattern matching internal logic check for interview_data presence."""
        match (self.status, self.interview_data):
            case (ApplicationStatus.INTERVIEW, None):
                # TODO: decide what to do if status is Interview but data is missing
                pass
            case _:
                pass
        return self


class CompanyModel(BaseModel):
    company_id: int | None = Field(None, description="PK")
    company_name: str = Field(..., min_length=1, max_length=100)
    industry: str | None = Field(None, max_length=50)
    website: HttpUrl | None = Field(None, max_length=200)
    city: str | None = Field(None, max_length=50)
    state: str | None = Field(None, max_length=50)
    notes: str | None = None

    @field_validator("website", mode="before")
    def clean_website(cls, v):
        return sanitize_empty_string(v)


@validate_pair_rule(
    field1="salary_min",
    field2="salary_max",
    predicate=lambda min_v, max_v: max_v >= min_v,
    error_msg="salary_max must be greater than or equal to salary_min",
)
class JobModel(BaseModel):
    job_id: int | None = Field(None, description="Primary Key")
    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    job_title: str = Field(..., min_length=1, max_length=100)
    job_type: JobType | None = None
    salary_min: int | None = Field(None, ge=0)
    salary_max: int | None = Field(None, ge=0)
    job_url: HttpUrl | None = Field(None, max_length=300)
    date_posted: date | None = None
    # TODO: Design the type for the requirements property, enforce validation on it
    requirements: dict[str, Any] | None = Field(
        default=None, description="Structured JSON data for job skills/qualifications"
    )

    @field_validator("job_url", mode="before")
    def clean_url(cls, v):
        return sanitize_empty_string(v)


class ContactModel(BaseModel):
    contact_id: int | None = Field(None, description="PK")
    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    job_title: str | None = Field(None, max_length=100)
    linkedin_url: HttpUrl | None = Field(None, max_length=200)
    notes: str | None = None

    @field_validator("email", "linkedin_url", mode="before")
    def clean_strings(cls, v):
        return sanitize_empty_string(v)
