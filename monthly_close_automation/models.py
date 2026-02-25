from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ValidationIssue:
    severity: str  # error | warning
    code: str
    message: str
    row_number: int | None = None
    file_name: str | None = None


@dataclass
class ValidationReport:
    issues: List[ValidationIssue] = field(default_factory=list)

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    def extend(self, issues: List[ValidationIssue]) -> None:
        self.issues.extend(issues)

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "warning")

    def to_summary(self) -> Dict[str, int]:
        return {
            "errors": self.error_count,
            "warnings": self.warning_count,
            "total": len(self.issues),
        }

