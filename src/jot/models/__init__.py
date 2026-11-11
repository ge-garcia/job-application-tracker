"""
DTO models for the companies, jobs, applications, and contacts tables. Each table defines:
- Shared Fields
- Inbound Form models (full and action-specific)
- Outbound immutable Row models for database reads
"""

from jot.models.application import (
    ApplicationFields,
    ApplicationForm,
    ApplicationRow,
    ApplicationStatus,
    ApplicationStatusForm,
)
from jot.models.company import (
    CompanyFields,
    CompanyForm,
    CompanyNotesForm,
    CompanyRow,
    CompanySummaryFields,
    CompanySummaryRow,
)
from jot.models.contact import (
    ContactFields,
    ContactForm,
    ContactNotesForm,
    ContactRow,
)
from jot.models.job import (
    JobFields,
    JobForm,
    JobRow,
    JobType,
)

__all__ = [
    "ApplicationFields",
    "ApplicationForm",
    "ApplicationRow",
    "ApplicationStatus",
    "ApplicationStatusForm",
    "CompanyFields",
    "CompanyForm",
    "CompanyNotesForm",
    "CompanyRow",
    "CompanySummaryFields",
    "CompanySummaryRow",
    "ContactFields",
    "ContactForm",
    "ContactNotesForm",
    "ContactRow",
    "JobFields",
    "JobForm",
    "JobRow",
    "JobType",
]
