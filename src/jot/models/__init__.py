"""
This module provides DTO models for our four tables.

Each table: companies, jobs, applications, contacts gets their own respective
Base, Create, Update, and Response models. With these models, we can enforce
types for our tables, as well as other logical validation rules for data entry
(e.g. salary_max cannot be < salary_min).
"""

from jot.models.application import (
    ApplicationBase,
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from jot.models.company import (
    CompanyBase,
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)
from jot.models.contact import (
    ContactBase,
    ContactCreate,
    ContactResponse,
    ContactUpdate,
)
from jot.models.job import JobBase, JobCreate, JobResponse, JobUpdate

__all__ = [
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationResponse",
    "ApplicationUpdate",
    "CompanyBase",
    "CompanyCreate",
    "CompanyResponse",
    "CompanyUpdate",
    "ContactBase",
    "ContactCreate",
    "ContactResponse",
    "ContactUpdate",
    "JobBase",
    "JobCreate",
    "JobResponse",
    "JobUpdate",
]
