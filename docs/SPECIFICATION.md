# Course Project: Job Application Tracker

Full-Stack Database Application with GenAI Integration

## Project Overview

Build a complete web application to track job applications. Use MySQL for data, Python/Flask for the backend, HTML/CSS for the frontend, and GenAI tools (ChatGPT, Claude, Gemini) to assist with development. This creates a portfolio piece demonstrating real-world skills!

## Grading Breakdown (20% of Course)

| Component                        |  Points |        % |
| -------------------------------- | ------: | -------: |
| Database Design & Implementation |      25 |      25% |
| CRUD Functionality               |      25 |      25% |
| User Interface                   |      15 |      15% |
| Job Match Feature                |      15 |      15% |
| Code Quality & GitHub            |      10 |      10% |
| GenAI Documentation              |      10 |      10% |
| **TOTAL**                        | **100** | **100%** |

## Required Technologies (All Free)

- **Database:** MySQL
- **Backend:** Python 3 with Flask
- **Frontend:** HTML, CSS (Bootstrap optional)
- **Version Control:** GitHub
- **GenAI:** ChatGPT, Claude, or Gemini (free tiers)

## Database Schema (4 Tables)

### `companies`

| Column         | Type           | Constraints                     |
| -------------- | -------------- | ------------------------------- |
| `company_id`   | `INT`          | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `company_name` | `VARCHAR(100)` | `NOT NULL`                      |
| `industry`     | `VARCHAR(50)`  |                                 |
| `website`      | `VARCHAR(200)` |                                 |
| `city`         | `VARCHAR(50)`  |                                 |
| `state`        | `VARCHAR(50)`  |                                 |
| `notes`        | `TEXT`         |                                 |

### `jobs`

| Column         | Type                                                    | Constraints                     |
| -------------- | ------------------------------------------------------- | ------------------------------- |
| `job_id`       | `INT`                                                   | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `company_id`   | `INT`                                                   | Foreign key → `companies`       |
| `job_title`    | `VARCHAR(100)`                                          | `NOT NULL`                      |
| `job_type`     | `ENUM('Full-time','Part-time','Contract','Internship')` |                                 |
| `salary_min`   | `INT`                                                   |                                 |
| `salary_max`   | `INT`                                                   |                                 |
| `job_url`      | `VARCHAR(300)`                                          |                                 |
| `date_posted`  | `DATE`                                                  |                                 |
| `requirements` | `JSON`                                                  |                                 |

### `applications`

| Column              | Type                                                                     | Constraints                     |
| ------------------- | ------------------------------------------------------------------------ | ------------------------------- |
| `application_id`    | `INT`                                                                    | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `job_id`            | `INT`                                                                    | Foreign key → `jobs`            |
| `application_date`  | `DATE`                                                                   | `NOT NULL`                      |
| `status`            | `ENUM('Applied','Screening','Interview','Offer','Rejected','Withdrawn')` |                                 |
| `resume_version`    | `VARCHAR(50)`                                                            |                                 |
| `cover_letter_sent` | `BOOLEAN`                                                                |                                 |
| `interview_data`    | `JSON`                                                                   |                                 |

### `contacts`

| Column         | Type           | Constraints                     |
| -------------- | -------------- | ------------------------------- |
| `contact_id`   | `INT`          | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `company_id`   | `INT`          | Foreign key → `companies`       |
| `contact_name` | `VARCHAR(100)` | `NOT NULL`                      |
| `title`        | `VARCHAR(100)` |                                 |
| `email`        | `VARCHAR(100)` |                                 |
| `phone`        | `VARCHAR(20)`  |                                 |
| `linkedin_url` | `VARCHAR(200)` |                                 |
| `notes`        | `TEXT`         |                                 |

## Required Features

### CRUD for All Tables

- **Create:** Forms to add new records
- **Read:** Lists and detail views
- **Update:** Edit forms for existing records
- **Delete:** Remove with confirmation

### Required Pages

1. **Dashboard:** Statistics overview
2. **Companies:** List/Add/Edit/Delete
3. **Jobs:** List/Add/Edit/Delete
4. **Applications:** List/Add/Edit/Delete
5. **Contacts:** List/Add/Edit/Delete
6. **Job Match:** Skills matching feature

## Job Match Feature

User enters skills; app shows jobs ranked by match percentage.

**Your Skills:** Python, SQL, Flask

**Matching Jobs:**

1. Software Developer at TechCorp — 100% (3/3 skills)
2. Data Analyst at DataCo — 67% (2/3 skills)
   - **Missing:** Tableau

Use GenAI to help write the matching algorithm!

## GenAI Documentation Requirement

**Required: `AI_USAGE.md` File**

You MUST document how you used AI tools. This teaches responsible AI use and proper attribution — a critical professional skill.

Include in your `AI_USAGE.md`:

1. **Tools Used:** Which AI tools (ChatGPT, Claude, Gemini)
2. **Prompts:** Key prompts you used
3. **What Worked:** Helpful AI-generated code/ideas
4. **What You Changed:** Modifications you made to the AI output
5. **Lessons Learned:** What you learned about using AI

### Example `AI_USAGE.md`

```markdown
# AI Usage Documentation

## Tools Used

- ChatGPT (GPT-4) for Flask routes and SQL queries
- Claude for debugging and code review

## Key Prompts

1. "Write a Flask route to display all jobs with company names using JOIN."
2. "Debug this error: MySQL connector not finding database."
3. "Create a function to calculate skill match percentage."

## What Worked Well

- AI-generated the basic CRUD routes quickly
- Excellent at explaining error messages

## What I Modified

- Changed variable names to match my schema
- Added input validation, AI didn't include
- Fixed SQL to use my actual table names

## Lessons Learned

- Always test AI code — it often has minor errors
- AI is great for boilerplate, but needs customization
- Asking for explanations helps me learn
```

## Project Structure

```text
job_tracker/
├── app.py               # Main Flask application
├── database.py          # Database connection functions
├── templates/           # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── jobs.html
│   ├── applications.html
│   ├── contacts.html
│   └── job_match.html
├── static/              # CSS, images
│   └── style.css
├── schema.sql           # Database creation script
├── AI_USAGE.md          # GenAI documentation
├── README.md            # Project description
└── requirements.txt     # Python dependencies
```

## Getting Started with Flask

Install Flask:

```bash
pip install flask mysql-connector-python
```

Basic `app.py` structure:

```python
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="YOUR_PASSWORD", database="job_tracker"
    )


@app.route("/")
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM applications")
    stats = cursor.fetchone()
    conn.close()
    return render_template("dashboard.html", stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
```

## Submission Requirements

1. GitHub repository link (public or add instructor as collaborator)
2. A 3 to 7-minute recorded video file of the execution of your project (client, server, database)
3. `README.md` with setup instructions
4. `AI_USAGE.md` documenting GenAI assistance
5. `schema.sql` file to recreate the database
6. Working application (instructor will clone and run)

## Grading Rubric Detail

| Category         | Excellent                                      | Good                                   | Needs Work                            |
| ---------------- | ---------------------------------------------- | -------------------------------------- | ------------------------------------- |
| Database (25)    | All 4 tables, proper FKs, JSON columns (23–25) | 3–4 tables, most relationships (18–22) | Missing tables or relationships (<18) |
| CRUD (25)        | Full CRUD all tables, validation (23–25)       | CRUD most tables, minor issues (18–22) | Incomplete CRUD (<18)                 |
| UI (15)          | Clean, intuitive, consistent (14–15)           | Functional, minor issues (11–13)       | Confusing or broken (<11)             |
| Job Match (15)   | Works correctly, shows % (14–15)               | Partially works (11–13)                | Not implemented (<11)                 |
| Code/GitHub (10) | Clean code, good commits (9–10)                | Readable, some commits (7–8)           | Messy, few commits (<7)               |
| AI Docs (10)     | Thorough `AI_USAGE.md` (9–10)                  | Basic documentation (7–8)              | Missing or minimal (<7)               |

## Timeline Suggestion

- **Week 1–2:** Database setup, basic Flask app, one table CRUD
- **Week 3–4:** Complete CRUD for all tables
- **Week 5–6:** Dashboard, Job Match feature
- **Week 7:** Polish UI, write documentation, test

## Need Help?

Use GenAI tools! Ask questions in discussion forums. Visit office hours. Start early — don't wait until the last week!

**Good luck — you've got this!**
