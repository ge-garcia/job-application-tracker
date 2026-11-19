from typing import Any

from jot.models import JobRow
from jot.services.match import parse_skills, rank_jobs


def _job(job_id: int, title: str, requirements: list[str] | None, **overrides: Any) -> JobRow:
    """A JobRow with just the fields rank_jobs reads"""
    return JobRow(job_id=job_id, company_id=1, job_title=title, requirements=requirements, **overrides)


def test_full_and_partial_matches_report_matched_missing_and_percent() -> None:
    """The specification's examples: Python, SQL, Flask scores 100% and 67% missing Tableau"""
    developer = _job(1, "Software Developer", ["Python", "SQL", "Flask"])
    analyst = _job(5, "Data Analyst", ["Python", "SQL", "Tableau"])

    results = rank_jobs(["Python", "SQL", "Flask"], [analyst, developer])

    assert [result.job for result in results] == [developer, analyst]
    assert results[0].percent == 100
    assert results[0].missing == ()
    assert results[1].matched == ("Python", "SQL")
    assert results[1].missing == ("Tableau",)
    assert results[1].percent == 67
    assert results[1].total == 3


def test_comparison_ignores_case_and_whitespace() -> None:
    """Skills match requirements whatever their case or padding, reported in the job's spelling"""
    job = _job(1, "Backend Engineer", ["PostgreSQL", " Docker ", "Deutsch (fließend)"])

    (result,) = rank_jobs(["postgresql", "DOCKER", "  deutsch (FLIESSEND) "], [job])

    assert result.matched == ("PostgreSQL", "Docker", "Deutsch (fließend)")
    assert result.percent == 100


def test_repeated_skills_and_requirements_count_once() -> None:
    """Seed job 12's messy requirements score as four distinct skills"""
    job = _job(12, "Operations Data Analyst", ["excel", "SQL", "sql", "Power BI", " python "])

    (result,) = rank_jobs(["SQL", "sql", "Python", "python"], [job])

    assert result.matched == ("SQL", "python")
    assert result.missing == ("excel", "Power BI")
    assert result.total == 4
    assert result.percent == 50


def test_jobs_without_requirements_or_matches_are_left_out() -> None:
    """NULL and empty requirements are skipped, and so is a job none of the skills meet"""
    jobs = [
        _job(1, "Unlisted", None),
        _job(2, "Empty list", []),
        _job(3, "Frontend Engineer", ["JavaScript", "CSS"]),
        _job(4, "Data Analyst", ["Python", "SQL", "Tableau"]),
    ]

    results = rank_jobs(["Python"], jobs)

    assert [result.job.job_id for result in results] == [4]


def test_sorted_by_percent_then_title() -> None:
    """Higher percentages come first, and equal percentages sort by title ignoring case"""
    jobs = [
        _job(1, "zeta", ["Python", "Go"]),
        _job(2, "beta", ["Python"]),
        _job(3, "Alpha", ["Python"]),
        _job(4, "Gamma", ["Python", "SQL", "Go"]),
    ]

    results = rank_jobs(["python", "sql"], jobs)

    assert [(result.job.job_title, result.percent) for result in results] == [
        ("Alpha", 100),
        ("beta", 100),
        ("Gamma", 67),
        ("zeta", 50),
    ]


def test_no_skills_or_no_jobs_rank_nothing() -> None:
    """Blank skills match nothing, and an empty job list ranks nothing"""
    jobs = [_job(1, "Software Developer", ["Python"])]

    assert rank_jobs([], jobs) == []
    assert rank_jobs(["", "   "], jobs) == []
    assert rank_jobs(["Python"], []) == []


def test_parse_skills_splits_strips_and_dedupes() -> None:
    """A ?skills= query splits on commas, drops blanks, and keeps the first spelling of each skill"""
    assert parse_skills(" Python, sql,,PYTHON , Power BI,") == ["Python", "sql", "Power BI"]
    assert parse_skills("") == []
    assert parse_skills(" , ,") == []
