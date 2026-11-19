import os

from flask import Flask, render_template

from jot.db import init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

init_db(app)


@app.get("/")
def index():
    return render_template("dash.html")
