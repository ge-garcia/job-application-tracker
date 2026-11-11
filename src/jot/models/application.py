from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


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
