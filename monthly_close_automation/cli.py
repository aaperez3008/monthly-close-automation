from __future__ import annotations

import argparse
from pathlib import Path

from .models import ValidationReport
from .reporting import write_json_report, write_markdown_report
from .transformers import transform_commissions, transform_points_load, transform_points_void


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="monthly-close-automation",
        description="Monthly close file transformation and validation pipeline.",
    )
    parser.add_argument(
        "command",
        choices=["run"],
        help="Command to execute.",
    )
    parser.add_argument("--commission-file", required=True, help="Commission CSV source file.")
    parser.add_argument("--points-load-file", required=True, help="Points load CSV source file.")
    parser.add_argument("--points-void-file", required=True, help="Points void CSV source file.")
    parser.add_argument("--output-dir", required=True, help="Directory for transformed output files.")
    parser.add_argument("--reports-dir", required=True, help="Directory for validation reports.")
    parser.add_argument("--month", required=True, help="Month name used for commission tag suffix.")
    parser.add_argument("--year", required=True, help="Year used for commission tag suffix.")
    return parser


def run_pipeline(
    commission_file: Path,
    points_load_file: Path,
    points_void_file: Path,
    output_dir: Path,
    reports_dir: Path,
    month: str,
    year: str,
) -> int:
    report = ValidationReport()

    transform_commissions(
        commission_file,
        output_dir / "matrixify_commissions.csv",
        report,
        month=month,
        year=year,
    )
    transform_points_load(
        points_load_file,
        output_dir / "points_load_ready.csv",
        report,
    )
    transform_points_void(
        points_void_file,
        output_dir / "points_void_ready.csv",
        report,
    )

    write_json_report(reports_dir / "validation_report.json", report)
    write_markdown_report(reports_dir / "validation_report.md", report)

    return 1 if report.error_count else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    commission_file = Path(args.commission_file)
    points_load_file = Path(args.points_load_file)
    points_void_file = Path(args.points_void_file)
    output_dir = Path(args.output_dir)
    reports_dir = Path(args.reports_dir)
    month = args.month
    year = args.year

    if args.command == "run":
        return run_pipeline(
            commission_file,
            points_load_file,
            points_void_file,
            output_dir,
            reports_dir,
            month,
            year,
        )
    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

