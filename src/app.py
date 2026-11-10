import os

import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "3307")),
        user=os.environ.get("DB_USER", "app"),
        password=os.environ["DB_PASSWORD"],
        database=os.environ.get("DB_NAME", "jobtracker"),
    )


@app.get("/")
def index():
    return render_template("index.html")
