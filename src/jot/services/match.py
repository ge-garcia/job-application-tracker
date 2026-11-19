"""
Job Match: rank saved jobs by how much of their requirements a list of skills covers
"""

from collections.abc import Iterable
from dataclasses import dataclass

from jot.models import JobRow


@dataclass(frozen=True)
class MatchResult:
    """A job's score against a list of skills, with requirements in the job's own spelling"""

    job: JobRow
    matched: tuple[str, ...]
    missing: tuple[str, ...]
    percent: int

    @property
    def total(self) -> int:
        """Number of distinct requirements on the job"""
        return len(self.matched) + len(self.missing)


def _unique(skills: Iterable[str]) -> dict[str, str]:
    """Map each skill's case-insensitive key to its first spelling, dropping blanks and repeats"""
    unique: dict[str, str] = {}
    for skill in skills:
        name = skill.strip()
        if name:
            unique.setdefault(name.casefold(), name)
    return unique


def parse_skills(raw: str) -> list[str]:
    """Split a comma-separated skills query into distinct skills, keeping the first spelling of each"""
    return list(_unique(raw.split(",")).values())


def rank_jobs(skills: list[str], jobs: list[JobRow]) -> list[MatchResult]:
    """
    Score each job by the share of its requirements found in `skills`, best first, then by title.

    Skills and requirements compare case-insensitively with surrounding whitespace ignored, and a
    repeated skill or requirement counts once. Jobs without requirements are left out, as are jobs
    that match none of the skills.
    """
    have = _unique(skills).keys()
    results: list[MatchResult] = []

    for job in jobs:
        required = _unique(job.requirements or [])
        matched = tuple(name for key, name in required.items() if key in have)
        if not matched:
            continue
        missing = tuple(name for key, name in required.items() if key not in have)
        percent = round(len(matched) / len(required) * 100)
        results.append(MatchResult(job=job, matched=matched, missing=missing, percent=percent))

    results.sort(key=lambda result: (-result.percent, result.job.job_title.casefold()))
    return results
