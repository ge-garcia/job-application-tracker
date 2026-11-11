import os
from contextlib import contextmanager

import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

# Initialize connection pool on module import
_pool = MySQLConnectionPool(
    pool_name="job_tracker_pool",
    pool_size=int(os.environ.get("DB_POOL_SIZE", "5")),
    host=os.environ.get("DB_HOST", "127.0.0.1"),
    port=int(os.environ.get("DB_PORT", "3307")),
    user=os.environ.get("DB_USER", "app"),
    password=os.environ["DB_PASSWORD"],
    database=os.environ.get("DB_NAME", "jobtracker"),
)


def get_connection():
    """Borrows a connection from the pool (or creates a fallback connection)."""
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


@contextmanager
def get_db_cursor(commit: bool = False):
    """
    Context manager yielding a dictionary cursor. Handles commit/rollback and returns the connection to the pool automatically.
    """
    conn = get_connection()
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
        conn.close()  # Returns connection back to pool
