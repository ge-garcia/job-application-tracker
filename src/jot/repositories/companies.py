from typing import Any, cast

from mysql.connector.abstracts import MySQLCursorAbstract

from jot.models import CompanyForm, CompanyNotesForm, CompanyRow, CompanySummaryRow
from jot.repositories.base import BaseRepository


class CompanyRepository(BaseRepository):
    """Data access layer for the companies table"""

    def __init__(self, cursor: MySQLCursorAbstract) -> None:
        self.cursor = cursor

    def list_all(self, search: str | None = None) -> list[CompanyRow]:
        """Returns all companies ordered alphabetically, optionally searching by name or industry"""
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            sql = """
                SELECT company_id, company_name, industry, website, city, state, notes
                FROM companies
                WHERE company_name LIKE %s or industry LIKE %s
                ORDER BY company_name ASC
            """
            self.cursor.execute(sql, (pattern, pattern))
        else:
            sql = """
                SELECT company_id, company_name, industry, website, city, state, notes
                FROM companies
                ORDER BY company_name ASC
            """

            self.cursor.execute(sql)

        rows = cast(list[dict[str, Any]], self.cursor.fetchall())
        return [CompanyRow.from_row(row) for row in rows]

    def list_summaries(self) -> list[CompanySummaryRow]:
        """Returns lightweight company rows for dropdown menus and select inputs"""
        sql = """
            SELECT company_id, company_name, industry
            FROM companies
            ORDER BY company_name ASC
        """
        self.cursor.execute(sql)
        return self._fetch_all(CompanySummaryRow)

    def get_by_id(self, company_id: int) -> CompanyRow | None:
        """Fetches a single company by primary key, or None if not found"""
        sql = """
            SELECT company_id, company_name, industry, website, city, state, notes
            FROM companies
            WHERE company_id = %s
        """
        self.cursor.execute(sql, (company_id,))
        return self._fetch_one(CompanyRow)

    def create(self, data: CompanyForm) -> int | None:
        """Inserts a new company and returns its generated company_id"""
        params = data.to_params()
        sql = """
            INSERT INTO companies (
                company_name,
                industry,
                website,
                city,
                state,
                notes
            ) VALUES (
                %(company_name)s,
                %(industry)s,
                %(website)s,
                %(city)s,
                %(state)s,
                %(notes)s
            )
        """
        self.cursor.execute(sql, params)
        return self.cursor.lastrowid

    def update(self, company_id: int, data: CompanyForm) -> bool:
        """Updates all editable fields on a company and returns True if the row changed"""
        params = data.to_params()
        params["company_id"] = company_id
        sql = """
            UPDATE companies
            SET company_name = %(company_name)s,
                industry = %(industry)s,
                website = %(website)s,
                city = %(city)s,
                state = %(state)s,
                notes = %(notes)s
            WHERE company_id = %(company_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def update_notes(self, company_id: int, data: CompanyNotesForm) -> bool:
        """Updates only the notes column for a company, and returns True if the row changed"""
        params = data.to_params()
        params["company_id"] = company_id
        sql = """
            UPDATE companies
            SET notes = %(notes)s
            WHERE company_id = %(company_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def delete(self, company_id: int) -> bool:
        """
        Deletes a company by primary key.

        NOTE: cascades to contacts; raises IntegrityError if jobs still reference this company.
        """
        sql = "DELETE FROM companies WHERE company_id = %s"
        self.cursor.execute(sql, (company_id,))
        return self.cursor.rowcount > 0
