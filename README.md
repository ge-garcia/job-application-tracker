# COP-4751: Job Application Tracker: `jot`

A web application project for COP-4751 at FIU. Built to help track job
applications during the job search process.

## Stack

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

A Docker compose setup is included which runs the Flask application and MySQL
with the `job_tracker` database created. Run it with:

```bash
docker compose up -d
```

And then visit the [website](http://localhost:5000)

## Project Structure

```
├── README.md
├── AGENTS.md
├── AI_USAGE.md                    # Project AI usage trace
├── .env                           # Configure database environment variables
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── sql                            # Base schema, applied in Docker compose directly
│   └── 01_schema.sql
└── src
    └── jot
        ├── app.py                 # Core setup
        ├── db.py                  # Connection configuration
        ├── core
        │   └── models.py          # Core types and validation
        ├── repositories           # TODO: CRUD operations
        ├── static                 # CSS Styling
        │   ├── style.css
        │   └── theme.css
        └── templates              # Components and pages
            ├── base.html
            └── index.html
```

## TODO

### Features in SPECIFICATION.md

- [ ] Track companies and job listings
- [ ] Record application submissions
- [ ] Manage interview schedules
- [ ] Store contact information

## Roadmap

- [ ] Seed the database with generated data
- [ ] Finalize JSON field types
- [ ] Create basic CRUD routes for each table
- [ ] Generate page routing layout and their respective templates
- [ ] Create core components, layouts, and views
- [ ] Polish UI
