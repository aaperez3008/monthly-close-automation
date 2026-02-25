from __future__ import annotations

import json
from pathlib import Path

from .models import ValidationReport


def write_json_report(path: Path, report: ValidationReport) -> None:
    payload = {
        "summary": report.to_summary(),
        "issues": [
            {
                "severity": issue.severity,
                "code": issue.code,
                "message": issue.message,
                "row_number": issue.row_number,
                "file_name": issue.file_name,
            }
            for issue in report.issues
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_markdown_report(path: Path, report: ValidationReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Monthly Close Validation Report",
        "",
        f"- Errors: **{report.error_count}**",
        f"- Warnings: **{report.warning_count}**",
        f"- Total issues: **{len(report.issues)}**",
        "",
        "## Issues",
        "",
    ]
    if not report.issues:
        lines.append("No issues found.")
    else:
        for issue in report.issues:
            location = ""
            if issue.file_name:
                location += f"`{issue.file_name}`"
            if issue.row_number:
                location += f":{issue.row_number}"
            if location:
                location = f" ({location})"
            lines.append(f"- [{issue.severity.upper()}] `{issue.code}` {issue.message}{location}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sql_load_template(path: Path, transformed_csv_path: Path, void_csv_path: Path) -> None:
    sql = f"""-- Manual DB load template for Points (MVP: no automatic production writes)
-- 1) Create backup before import
CREATE TABLE IF NOT EXISTS points_backup_{{YYYYMM}} AS
SELECT *
FROM points;

-- 2) Load transformed monthly points (example uses psql \\copy)
-- \\copy points_stage(consultant_id, original_points, current_points, start_date, expiry_date, description_source, display_text_es, display_text_en)
-- FROM '{transformed_csv_path.as_posix()}' WITH (FORMAT csv, HEADER true);

-- 3) Optional: apply former consultant void rows
-- \\copy points_void_stage(consultant_id, void_points, void_date, reason)
-- FROM '{void_csv_path.as_posix()}' WITH (FORMAT csv, HEADER true);

-- 4) Reconcile totals and counts before merge.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(sql, encoding="utf-8")

