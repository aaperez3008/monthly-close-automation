import re
from collections import Counter
from typing import Iterable

from .models import ValidationIssue

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_columns(
    rows: list[dict[str, str]],
    required: Iterable[str],
    file_name: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not rows:
        return [ValidationIssue("error", "EMPTY_FILE", "Input file is empty", file_name=file_name)]

    available = set(rows[0].keys())
    for column in required:
        if column not in available:
            issues.append(
                ValidationIssue(
                    "error",
                    "MISSING_COLUMN",
                    f"Missing required column '{column}'",
                    file_name=file_name,
                )
            )
    return issues


def validate_non_empty(
    rows: list[dict[str, str]],
    file_name: str,
    column: str,
    code: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for idx, row in enumerate(rows, start=2):
        if not (row.get(column) or "").strip():
            issues.append(
                ValidationIssue(
                    "error",
                    code,
                    f"Column '{column}' is required",
                    row_number=idx,
                    file_name=file_name,
                )
            )
    return issues


def validate_emails(rows: list[dict[str, str]], file_name: str, column: str = "Email") -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for idx, row in enumerate(rows, start=2):
        email = (row.get(column) or "").strip()
        if not email:
            continue
        if not EMAIL_RE.match(email):
            issues.append(
                ValidationIssue(
                    "error",
                    "INVALID_EMAIL",
                    f"Invalid email '{email}'",
                    row_number=idx,
                    file_name=file_name,
                )
            )
    return issues


def validate_duplicates(
    rows: list[dict[str, str]],
    file_name: str,
    key_columns: list[str],
    code: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    key_values: list[tuple[str, ...]] = []

    for row in rows:
        key_values.append(tuple((row.get(col) or "").strip().lower() for col in key_columns))

    counts = Counter(key_values)
    duplicate_keys = {k for k, count in counts.items() if count > 1}

    if not duplicate_keys:
        return issues

    for idx, key in enumerate(key_values, start=2):
        if key in duplicate_keys:
            issues.append(
                ValidationIssue(
                    "warning",
                    code,
                    f"Duplicate key across columns {key_columns}: {key}",
                    row_number=idx,
                    file_name=file_name,
                )
            )
    return issues

