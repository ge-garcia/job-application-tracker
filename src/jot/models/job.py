from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from jot.models.validation import FormModel, RowModel, check_http_url


class JobType(str, Enum):
    """Employment classification types for job postings"""

    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"


class JobFields(BaseModel):
    """Shared schema columns for a job posting"""

    company_id: int
    job_title: str
    job_type: JobType | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    job_url: str | None = None
    date_posted: date | None = None
    requirements: list[str] | None = None


class JobForm(FormModel, JobFields):
    """Validated form payload for creating or updating a job posting"""

    company_id: int = Field(
        ..., gt=0, description="FK referencing companies.company_id"
    )
    job_title: str = Field(..., min_length=1, max_length=100)
    salary_min: int | None = Field(None, ge=0)
    salary_max: int | None = Field(None, ge=0)
    job_url: str | None = Field(None, max_length=300)

    _job_url_valid = field_validator("job_url")(check_http_url)

    @field_validator("requirements", mode="before")
    @classmethod
    def parse_requirements(cls, value: Any) -> list[str] | None:
        """Take a job form's requirements entry and strip, split, and collect it in a list (or return None)"""
        if value is None:
            return None
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",") if item.strip()]
            return items or None
        return value

    @model_validator(mode="after")
    def validate_salary_range(self, Any) -> Any:
        salary_min = getattr(self, "salary_min", None)
        salary_max = getattr(self, "salary_max", None)

        match (salary_min, salary_max):
            case (salary_min, salary_max) if (
                salary_min is not None
                and salary_max is not None
                and salary_max < salary_min
            ):
                raise ValueError(
                    "salary_max must be greater than or equal to salary_min"
                )
            case _:
                pass
        return self


class JobRow(RowModel, JobFields):
    """Immutable database row representation of a job posting"""

    job_id: int
    company_name: str | None = None
