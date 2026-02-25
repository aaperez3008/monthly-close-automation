from __future__ import annotations

import csv
from pathlib import Path

from .models import ValidationIssue, ValidationReport
from .validators import (
    require_columns,
    validate_duplicates,
    validate_emails,
    validate_non_empty,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def normalize_consultant_id(raw_id: str) -> str:
    value = (raw_id or "").strip()
    normalized = value.lstrip("0")
    return normalized or "0"


def transform_commissions(input_path: Path, output_path: Path, report: ValidationReport) -> None:
    file_name = input_path.name
    rows = read_csv(input_path)
    required_columns = [
        "EMAIL",
        "EMAILADDRESS",
        "COMMAND",
        "Metafield: custom.commission_percentage[number_integer]",
        "CONSID",
    ]
    report.extend(require_columns(rows, required_columns, file_name))
    if report.error_count:
        return
    report.extend(
        validate_non_empty(
            rows,
            file_name,
            "Metafield: custom.commission_percentage[number_integer]",
            "EMPTY_COMMISSION_PCT",
        )
    )
    report.extend(validate_non_empty(rows, file_name, "CONSID", "EMPTY_CONSID"))
    report.extend(validate_emails(rows, file_name, "EMAIL"))
    report.extend(validate_emails(rows, file_name, "EMAILADDRESS"))

    transformed: list[dict[str, str]] = []
    for idx, row in enumerate(rows, start=2):
        email = (row.get("EMAIL") or "").strip()
        email_address = (row.get("EMAILADDRESS") or "").strip()
        command = (row.get("COMMAND") or "").strip() or "Update"
        commission = (row.get("Metafield: custom.commission_percentage[number_integer]") or "").strip()
        consid = normalize_consultant_id(row.get("CONSID", ""))
        normalized_email = email or email_address
        normalized_email_address = email_address or email

        if email and email_address and email.lower() != email_address.lower():
            report.add(
                ValidationIssue(
                    "warning",
                    "EMAIL_MISMATCH",
                    f"EMAIL and EMAILADDRESS differ: '{email}' vs '{email_address}'",
                    row_number=idx,
                    file_name=file_name,
                )
            )

        if commission not in {"40", "45", "50"}:
            report.add(
                ValidationIssue(
                    "warning",
                    "UNEXPECTED_COMMISSION_VALUE",
                    f"Commission percentage '{commission}' is outside expected 40/45/50",
                    row_number=idx,
                    file_name=file_name,
                )
            )

        if not normalized_email and consid == "0":
            report.add(
                ValidationIssue(
                    "error",
                    "MISSING_IDENTITY",
                    "Row must contain at least one email or a valid CONSID",
                    row_number=idx,
                    file_name=file_name,
                )
            )

        transformed.append(
            {
                "EMAIL": normalized_email.upper(),
                "EMAILADDRESS": normalized_email_address.upper(),
                "COMMAND": command,
                "Metafield: custom.commission_percentage[number_integer]": commission,
                "CONSID": consid,
            }
        )

    report.extend(validate_duplicates(transformed, file_name, ["CONSID"], "DUPLICATE_CONSID"))
    write_csv(
        output_path,
        transformed,
        [
            "EMAIL",
            "EMAILADDRESS",
            "COMMAND",
            "Metafield: custom.commission_percentage[number_integer]",
            "CONSID",
        ],
    )


def _parse_int(value: str) -> int | None:
    cleaned = (value or "").strip()
    try:
        return int(float(cleaned))
    except ValueError:
        return None


def transform_points_load(points_path: Path, output_path: Path, report: ValidationReport) -> None:
    points_file = points_path.name
    points_rows = read_csv(points_path)

    report.extend(
        require_columns(
            points_rows,
            ["consultant_id", "original", "current", "earns_at", "expires_at", "description"],
            points_file,
        )
    )
    if report.error_count:
        return

    report.extend(validate_non_empty(points_rows, points_file, "consultant_id", "EMPTY_CONSULTANT_ID"))
    report.extend(validate_non_empty(points_rows, points_file, "original", "EMPTY_ORIGINAL_POINTS"))
    report.extend(validate_non_empty(points_rows, points_file, "current", "EMPTY_CURRENT_POINTS"))
    transformed_rows: list[dict[str, str]] = []
    for idx, row in enumerate(points_rows, start=2):
        original_value = _parse_int(row.get("original", ""))
        current_value = _parse_int(row.get("current", ""))
        if original_value is None or current_value is None:
            report.add(
                ValidationIssue(
                    "error",
                    "INVALID_POINTS",
                    "Original/current points must be numeric",
                    row_number=idx,
                    file_name=points_file,
                )
            )
            continue

        if original_value != current_value:
            report.add(
                ValidationIssue(
                    "warning",
                    "ORIGINAL_CURRENT_MISMATCH",
                    f"original ({original_value}) differs from current ({current_value})",
                    row_number=idx,
                    file_name=points_file,
                )
            )

        transformed_rows.append(
            {
                "consultant_id": normalize_consultant_id(row.get("consultant_id", "")),
                "original": str(original_value),
                "current": str(current_value),
                "earns_at": (row.get("earns_at") or "").strip(),
                "expires_at": (row.get("expires_at") or "").strip(),
                "description": (row.get("description") or "").strip(),
            }
        )

    report.extend(validate_duplicates(transformed_rows, points_file, ["consultant_id"], "DUPLICATE_POINTS_RECORD"))
    write_csv(
        output_path,
        transformed_rows,
        ["consultant_id", "original", "current", "earns_at", "expires_at", "description"],
    )

def transform_points_void(void_path: Path, output_path: Path, report: ValidationReport) -> None:
    file_name = void_path.name
    rows = read_csv(void_path)
    report.extend(
        require_columns(
            rows,
            ["consultant_id", "original", "current", "earns_at", "expires_at", "description"],
            file_name,
        )
    )
    if report.error_count:
        return

    transformed_rows: list[dict[str, str]] = []
    for idx, row in enumerate(rows, start=2):
        original_value = _parse_int(row.get("original", ""))
        current_value = _parse_int(row.get("current", ""))
        if original_value is None or current_value is None:
            report.add(
                ValidationIssue(
                    "error",
                    "INVALID_VOID_POINTS",
                    "Void original/current must be numeric",
                    row_number=idx,
                    file_name=file_name,
                )
            )
            continue

        if original_value > 0 or current_value > 0:
            report.add(
                ValidationIssue(
                    "warning",
                    "VOID_NOT_NEGATIVE",
                    f"Void row should be negative values, got original={original_value}, current={current_value}",
                    row_number=idx,
                    file_name=file_name,
                )
            )

        transformed_rows.append(
            {
                "consultant_id": normalize_consultant_id(row.get("consultant_id", "")),
                "original": str(original_value),
                "current": str(current_value),
                "earns_at": (row.get("earns_at") or "").strip(),
                "expires_at": (row.get("expires_at") or "").strip(),
                "description": (row.get("description") or "").strip(),
            }
        )

    report.extend(validate_duplicates(transformed_rows, file_name, ["consultant_id"], "DUPLICATE_VOID_RECORD"))
    write_csv(
        output_path,
        transformed_rows,
        ["consultant_id", "original", "current", "earns_at", "expires_at", "description"],
    )

