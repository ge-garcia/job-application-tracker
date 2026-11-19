from collections.abc import Generator
from contextlib import ExitStack
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient
from mysql.connector.abstracts import MySQLCursorAbstract

# Route modules whose get_cursor/commit_db the `client` fixture patches
ROUTE_MODULES = ("companies", "jobs", "applications", "contacts")


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
    # Imported here so database-free tests (e.g. test_match.py) never open the pool in jot.db
    from jot.app import create_app

    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with ExitStack() as stack:
        for module in ROUTE_MODULES:
            stack.enter_context(patch(f"jot.routes.{module}.get_cursor", return_value=cursor))
            stack.enter_context(patch(f"jot.routes.{module}.commit_db"))
        yield stack.enter_context(flask_app.test_client())
