# COP-4751: Job Application Tracker

A web application project for COP-4751 at FIU. Built to help track job
applications during the job search process.

## Planned Features

- [ ] Track companies and job listings
- [ ] Record application submissions
- [ ] Manage interview schedules
- [ ] Store contact information

## Technologies

- [MySQL](https://dev.mysql.com/doc/) Database
- Python with [Flask](https://flask.palletsprojects.com/en/stable/)
- HTML/CSS for the web interface

## Getting Started

First, copy `.env.example` to `.env`, and modify the values as necessary for the
connection. Then install dependencies:

```bash
# unix
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# windows
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# with uv
uv pip install -r requirements.txt
```

And run the project (in that same virtual environment) with:

```bash
flask --app src/app run --debug
```

### Docker

A Docker compose setup is included which runs the Flask application and MySQL with the `job_tracker` database created.

TODO: Seed the database with some generated data

## Architecture
