from typing import Any, cast

from jot.models import ApplicationRow, ApplicationStatus
from jot.models.validation import RowModel
from jot.repositories.applications import _SELECT as _APPLICATION_SELECT
from jot.repositories.base import BaseRepository


class DashboardStats(RowModel):
    """Record totals for the dashboard cards, plus an application count for every status"""

    companies: int
    jobs: int
    contacts: int
    applications: int
    by_status: dict[ApplicationStatus, int]


class DashboardRepository(BaseRepository):
    """Read-only aggregates for the dashboard"""

    def stats(self) -> DashboardStats:
        """Counts every table, and applications per status in ApplicationStatus order (zeros included)"""
        sql = """
            SELECT
                (SELECT COUNT(*) FROM companies) AS companies,
                (SELECT COUNT(*) FROM jobs) AS jobs,
                (SELECT COUNT(*) FROM contacts) AS contacts,
                (SELECT COUNT(*) FROM applications) AS applications
        """
        self.cursor.execute(sql)
        totals = cast(dict[str, Any], self.cursor.fetchone())

        sql = """
            SELECT status, COUNT(*) AS total
            FROM applications
            GROUP BY status
        """
        self.cursor.execute(sql)
        rows = cast(list[dict[str, Any]], self.cursor.fetchall())
        counts = {row["status"]: row["total"] for row in rows}

        return DashboardStats.model_validate(
            {**totals, "by_status": {status: counts.get(status.value, 0) for status in ApplicationStatus}}
        )

    def recent_applications(self, limit: int = 5) -> list[ApplicationRow]:
        """Returns the newest applications, ordered like ApplicationRepository.list_all"""
        sql = f"""
            {_APPLICATION_SELECT}
            ORDER BY a.application_date DESC, a.application_id DESC
            LIMIT %s
        """
        self.cursor.execute(sql, (limit,))
        return self._fetch_all(ApplicationRow)
