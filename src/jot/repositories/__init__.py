"""Repositories (CRUD operations for each table)"""

from jot.repositories.companies import CompanyRepository
from jot.repositories.jobs import JobRepository

__all__ = ["CompanyRepository", "JobRepository"]
