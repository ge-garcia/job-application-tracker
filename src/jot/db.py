import os
from collections.abc import Generator
from contextlib import contextmanager

import mysql.connector
from flask import Flask, g
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

_pool = MySQLConnectionPool(
    pool_name="job_tracker_pool",
    pool_size=int(os.environ.get("DB_POOL_SIZE", "5")),
    host=os.environ.get("DB_HOST", "127.0.0.1"),
    port=int(os.environ.get("DB_PORT", "3307")),
    user=os.environ.get("DB_USER", "app"),
    password=os.environ["DB_PASSWORD"],
    database=os.environ.get("DB_NAME", "jobtracker"),
)


def get_conn() -> PooledMySQLConnection | MySQLConnectionAbstract:
    """Borrows a connection from the pool (or creates a fallback connection)"""
    try:
        return _pool.get_connection()
    except Exception:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "127.0.0.1"),
            port=int(os.environ.get("DB_PORT", "3307")),
            user=os.environ.get("DB_USER", "app"),
            password=os.environ["DB_PASSWORD"],
            database=os.environ.get("DB_NAME", "jobtracker"),
        )


def get_cursor() -> MySQLCursorAbstract:
    """Returns a request-scoped cursor, opening a connection if needed"""
    if "db_conn" not in g:
        g.db_conn = get_conn()
        g.db_cursor = g.db_conn.cursor(dictionary=True)
    return g.db_cursor


def commit_db() -> None:
    """Commit the current request-scoped transaction (if it exists)"""
    conn = g.get("db_conn", None)
    if conn is not None:
        conn.commit()


def close_db(exc: BaseException | None = None) -> None:
    """Rollback on unhandled exceptions, close cursor, and return connection to pool"""
    cursor = g.pop("db_cursor", None)
    conn = g.pop("db_conn", None)

    if cursor is not None:
        cursor.close()

    if conn is not None:
        if exc is not None:
            conn.rollback()
        conn.close()


def init_db(app: Flask) -> None:
    """Register database teardown hooks on the application"""
    app.teardown_appcontext(close_db)


@contextmanager
def get_db_cursor(commit: bool = False) -> Generator[MySQLCursorAbstract, None, None]:
    """Standalone connection manager for tests or other non-request scoped cursors"""
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
