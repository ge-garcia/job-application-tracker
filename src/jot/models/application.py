from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from jot.models.validation import FormModel, RowModel


class ApplicationStatus(str, Enum):
    """Lifecycle stages for a job application"""

    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


# TODO: Design the type for the interview_data property, enforce validation on it
class ApplicationFields(BaseModel):
    """Shared schema columns for a job application"""

    job_id: int
    application_date: date
    status: ApplicationStatus = ApplicationStatus.APPLIED
    resume_version: str | None = None
    cover_letter_sent: bool = False
    interview_data: dict[str, Any] | None = None


class ApplicationForm(FormModel, ApplicationFields):
    """Validated payload for creating or editing an application"""

    job_id: int = Field(..., gt=0, description="FK referencing jobs.job_id")
    resume_version: str | None = Field(None, max_length=50)


class ApplicationStatusForm(FormModel):
    """Targeted payload for updating only an application's status"""

    status: ApplicationStatus


class ApplicationRow(RowModel, ApplicationFields):
    """Immutable database row representation of an application"""

    application_id: int
    job_title: str | None = None
    company_name: str | None = None
