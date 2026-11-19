from jot.models import JobForm, JobRow
from jot.repositories.base import BaseRepository

_SELECT = """
    SELECT
        j.job_id,
        j.company_id,
        j.job_title,
        j.job_type,
        j.salary_min,
        j.salary_max,
        j.job_url,
        j.date_posted,
        j.requirements,
        c.company_name
    FROM jobs j
    JOIN companies c ON c.company_id = j.company_id
"""


class JobRepository(BaseRepository):
    """Data access layer for the jobs table"""

    def list_all(self, search: str | None = None) -> list[JobRow]:
        """Returns all jobs, newest postings first, optionally searching by title or company name"""
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            sql = f"""
                {_SELECT}
                WHERE j.job_title LIKE %s OR c.company_name LIKE %s
                ORDER BY j.date_posted DESC, j.job_id DESC
            """
            self.cursor.execute(sql, (pattern, pattern))
        else:
            sql = f"""
                {_SELECT}
                ORDER BY j.date_posted DESC, j.job_id DESC
            """
            self.cursor.execute(sql)

        return self._fetch_all(JobRow)

    def get_by_id(self, job_id: int) -> JobRow | None:
        """Fetches a single job by primary key, or None if not found"""
        sql = f"""
            {_SELECT}
            WHERE j.job_id = %s
        """
        self.cursor.execute(sql, (job_id,))
        return self._fetch_one(JobRow)

    def create(self, data: JobForm) -> int | None:
        """Inserts a new job and returns its generated job_id"""
        params = data.to_params()
        sql = """
            INSERT INTO jobs (
                company_id,
                job_title,
                job_type,
                salary_min,
                salary_max,
                job_url,
                date_posted,
                requirements
            ) VALUES (
                %(company_id)s,
                %(job_title)s,
                %(job_type)s,
                %(salary_min)s,
                %(salary_max)s,
                %(job_url)s,
                %(date_posted)s,
                %(requirements)s
            )
        """
        self.cursor.execute(sql, params)
        return self.cursor.lastrowid

    def update(self, job_id: int, data: JobForm) -> bool:
        """Updates all editable fields on a job and returns True if the row changed"""
        params = data.to_params()
        params["job_id"] = job_id
        sql = """
            UPDATE jobs
            SET company_id = %(company_id)s,
                job_title = %(job_title)s,
                job_type = %(job_type)s,
                salary_min = %(salary_min)s,
                salary_max = %(salary_max)s,
                job_url = %(job_url)s,
                date_posted = %(date_posted)s,
                requirements = %(requirements)s
            WHERE job_id = %(job_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def delete(self, job_id: int) -> bool:
        """
        Deletes a job by primary key.

        NOTE: raises IntegrityError (1451) if applications still reference this job.
        """
        sql = "DELETE FROM jobs WHERE job_id = %s"
        self.cursor.execute(sql, (job_id,))
        return self.cursor.rowcount > 0
