import os

import mysql.connector


def get_connection():
    """Establishes and returns a database connection with the provided
    environment variables and sensible defaults otherwise. `DB_PASSWORD` is
    required.

    Returns:
        A connection to a MySQL database (or pool)
    """
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "3307")),
        user=os.environ.get("DB_USER", "app"),
        password=os.environ["DB_PASSWORD"],
        database=os.environ.get("DB_NAME", "jobtracker"),
    )
