from datetime import date, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from jot.models.validation import FormModel, RowModel


class ApplicationStatus(StrEnum):
    """Lifecycle stages for a job application"""

    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class InterviewOutcome(StrEnum):
    """Result states for an individual interview round"""

    PENDING = "Pending"
    PASSED = "Passed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class InterviewRound(BaseModel):
    """Single interview stage inside applications.interview_data"""

    model_config = ConfigDict(str_strip_whitespace=True)

    type: str = Field(..., min_length=1, max_length=50)
    scheduled_at: datetime
    format: str | None = Field(None, max_length=50)
    interviewers: list[str] = Field(default_factory=list)
    outcome: InterviewOutcome = InterviewOutcome.PENDING
    notes: str | None = None

    @field_validator("interviewers", mode="before")
    @classmethod
    def parse_interviewers(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [name.strip() for name in value.split(",") if name.strip()]
        return value


class InterviewData(BaseModel):
    """Structured schema for the applications.interview_data JSON column"""

    rounds: list[InterviewRound] = Field(default_factory=list)


class ApplicationFields(BaseModel):
    """Shared schema columns for a job application"""

    job_id: int
    application_date: date
    status: ApplicationStatus = ApplicationStatus.APPLIED
    resume_version: str | None = None
    cover_letter_sent: bool = False
    interview_data: InterviewData | None = None


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
