"""
This module provides DTO models for our four tables.

Each one (companies, jobs, applications, contacts) gets their own respective
Base, Create, Update, and Response models. With these models, we can enforce
types for our tables, as well as other logical validation rules for data entry
(e.g. salary_max cannot be < salary_min).
"""

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator

from jot.core.validation import sanitize_empty_string, validate_pair_rule


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


# COMPANIES SCHEMAS
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


# JOBS SCHEMAS
# TODO: Design the type for the requirements property, enforce validation on it
class JobBase(BaseModel):
    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    job_title: str = Field(..., min_length=1, max_length=100)
    job_type: JobType | None = None
    salary_min: int | None = Field(None, ge=0)
    salary_max: int | None = Field(None, ge=0)
    job_url: HttpUrl | None = Field(None, max_length=300)
    date_posted: date | None = None
    requirements: dict[str, Any] | None = None

    @field_validator("job_url", mode="before")
    def clean_url(cls, v):
        return sanitize_empty_string(v)


@validate_pair_rule(
    field1="salary_min",
    field2="salary_max",
    predicate=lambda min_v, max_v: max_v >= min_v,
    error_msg="salary_max must be greater than or equal to salary_min",
)
class JobCreate(JobBase):
    """Payload for posting a new job. Body ommitted since only JobBase is needed"""


@validate_pair_rule(
    field1="salary_min",
    field2="salary_max",
    predicate=lambda min_v, max_v: max_v >= min_v,
    error_msg="salary_max must be greater than or equal to salary_min",
)
class JobUpdate(BaseModel):
    company_id: int | None = Field(None, gt=0)
    job_title: str | None = Field(None, min_length=1, max_length=100)
    job_type: JobType | None = None
    salary_min: int | None = Field(None, ge=0)
    salary_max: int | None = Field(None, ge=0)
    job_url: HttpUrl | None = Field(None, max_length=300)
    date_posted: date | None = None
    requirements: dict[str, Any] | None = None

    @field_validator("job_url", mode="before")
    def clean_url(cls, v):
        return sanitize_empty_string(v)


@validate_pair_rule(
    field1="salary_min",
    field2="salary_max",
    predicate=lambda min_v, max_v: max_v >= min_v,
    error_msg="salary_max must be greater than or equal to salary_min",
)
class JobResponse(JobBase):
    job_id: int = Field(..., gt=0, description="PK cannot be null")


# APPLICATIONS SCHEMAS
# TODO: Design the type for the interview_data property, enforce validation on it
class ApplicationBase(BaseModel):
    job_id: int = Field(..., gt=0, description="FK referencing jobs.job_id")
    application_date: date
    status: ApplicationStatus = ApplicationStatus.APPLIED
    resume_version: str | None = Field(None, max_length=50)
    cover_letter_sent: bool = False
    interview_data: dict[str, Any] | None = None


class ApplicationCreate(ApplicationBase):
    """Payload for submitting a job application."""


class ApplicationUpdate(BaseModel):
    job_id: int | None = Field(None, gt=0)
    application_date: date | None = None
    status: ApplicationStatus | None = None
    resume_version: str | None = Field(None, max_length=50)
    cover_letter_sent: bool | None = None
    interview_data: dict[str, Any] | None = None


class ApplicationResponse(ApplicationBase):
    application_id: int = Field(..., gt=0, description="PK cannot be null")


# CONTACTS SCHEMAS
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
    created_at: datetime | None = None
