from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, field_validator

from jot.models.validation import sanitize_empty_string, validate_pair_rule


class JobType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"


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
