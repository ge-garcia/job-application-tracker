from typing import Any

from jot.models import ApplicationForm, ApplicationRow, ApplicationStatusForm
from jot.repositories.base import BaseRepository

_SELECT = """
    SELECT
        a.application_id,
        a.job_id,
        a.application_date,
        a.status,
        a.resume_version,
        a.cover_letter_sent,
        a.interview_data,
        j.job_title,
        c.company_name
    FROM applications a
    JOIN jobs j ON j.job_id = a.job_id
    JOIN companies c ON c.company_id = j.company_id
"""


def _params(data: ApplicationForm) -> dict[str, Any]:
    """to_params, with interview_data serialized by pydantic since json.dumps can't encode its datetimes"""
    params = data.model_copy(update={"interview_data": None}).to_params()
    if data.interview_data is not None:
        params["interview_data"] = data.interview_data.model_dump_json()
    return params


class ApplicationRepository(BaseRepository):
    """Data access layer for the applications table"""

    def list_all(self, search: str | None = None) -> list[ApplicationRow]:
        """Returns all applications, newest first, optionally searching by job title or company name"""
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            sql = f"""
                {_SELECT}
                WHERE j.job_title LIKE %s OR c.company_name LIKE %s
                ORDER BY a.application_date DESC, a.application_id DESC
            """
            self.cursor.execute(sql, (pattern, pattern))
        else:
            sql = f"""
                {_SELECT}
                ORDER BY a.application_date DESC, a.application_id DESC
            """
            self.cursor.execute(sql)

        return self._fetch_all(ApplicationRow)

    def get_by_id(self, application_id: int) -> ApplicationRow | None:
        """Fetches a single application by primary key, or None if not found"""
        sql = f"""
            {_SELECT}
            WHERE a.application_id = %s
        """
        self.cursor.execute(sql, (application_id,))
        return self._fetch_one(ApplicationRow)

    def create(self, data: ApplicationForm) -> int | None:
        """Inserts a new application and returns its generated application_id"""
        params = _params(data)
        sql = """
            INSERT INTO applications (
                job_id,
                application_date,
                status,
                resume_version,
                cover_letter_sent,
                interview_data
            ) VALUES (
                %(job_id)s,
                %(application_date)s,
                %(status)s,
                %(resume_version)s,
                %(cover_letter_sent)s,
                %(interview_data)s
            )
        """
        self.cursor.execute(sql, params)
        return self.cursor.lastrowid

    def update(self, application_id: int, data: ApplicationForm) -> bool:
        """Updates all editable fields on an application and returns True if the row changed"""
        params = _params(data)
        params["application_id"] = application_id
        sql = """
            UPDATE applications
            SET job_id = %(job_id)s,
                application_date = %(application_date)s,
                status = %(status)s,
                resume_version = %(resume_version)s,
                cover_letter_sent = %(cover_letter_sent)s,
                interview_data = %(interview_data)s
            WHERE application_id = %(application_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def update_status(self, application_id: int, data: ApplicationStatusForm) -> bool:
        """Updates only the status column for an application, and returns True if the row changed"""
        params = data.to_params()
        params["application_id"] = application_id
        sql = """
            UPDATE applications
            SET status = %(status)s
            WHERE application_id = %(application_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def delete(self, application_id: int) -> bool:
        """Deletes an application by primary key"""
        sql = "DELETE FROM applications WHERE application_id = %s"
        self.cursor.execute(sql, (application_id,))
        return self.cursor.rowcount > 0
