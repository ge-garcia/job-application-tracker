import os

from flask import Flask, render_template

from jot.db import init_db
from jot.routes import register_blueprints

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

init_db(app)
register_blueprints(app)


@app.get("/")
def index():
    return render_template("dashboard.html")
