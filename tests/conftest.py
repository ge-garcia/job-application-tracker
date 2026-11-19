from collections.abc import Generator

# from unittest.mock import patch
import pytest
from flask.testing import FlaskClient
from mysql.connector.abstracts import MySQLCursorAbstract

from jot.app import app as flask_app


@pytest.fixture
def cursor() -> Generator[MySQLCursorAbstract, None, None]:
    """Transaction-wrapped cursor for repository tests (always rolls back)."""
    from jot.db import get_conn

    conn = get_conn()
    conn.start_transaction()
    cur = conn.cursor(dictionary=True)
    try:
        yield cur
    finally:
        cur.close()
        conn.rollback()
        conn.close()


@pytest.fixture
def client(cursor: MySQLCursorAbstract) -> Generator[FlaskClient, None, None]:
    """
    Test client sharing the rolling-back `cursor`.
    Patches `get_cursor` to return `cursor` and turns `commit_db` into a flush-only no-op
    so route writes remain visible within the test transaction and roll back afterward.
    """

    flask_app.config["TESTING"] = True
    with (
        # TODO: setup cursor + transactions in routes
        # patch("jot.routes.companies.get_cursor", return_value=cursor),
        # patch("jot.routes.companies.commit_db"),
        flask_app.test_client() as test_client,
    ):
        yield test_client
