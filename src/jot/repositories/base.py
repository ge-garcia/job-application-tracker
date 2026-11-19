from typing import Any, TypeVar, cast

from mysql.connector.abstracts import MySQLCursorAbstract

from jot.models.validation import RowModel

T = TypeVar("T", bound=RowModel)


class BaseRepository:
    """Wraps fetching due to frequent type casting to narrow MySQLCursorAbstract"""

    def __init__(self, cursor: MySQLCursorAbstract) -> None:
        self.cursor = cursor

    def _fetch_all(self, model: type[T]) -> list[T]:
        rows = cast(list[dict[str, Any]], self.cursor.fetchall())
        return [model.from_row(row) for row in rows]

    def _fetch_one(self, model: type[T]) -> T | None:
        row = cast(dict[str, Any] | None, self.cursor.fetchone())
        return model.from_row(row) if row else None
