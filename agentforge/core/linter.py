"""
12-Factor Agent compliance linter.

Scans a project directory, evaluates each of the 12 factors, and produces
a compliance score (0-100) with per-rule pass/fail details and suggestions.
"""

import json
import os
import sys
from typing import Dict, List, Optional

from agentforge.rules.twelve_factor import get_twelve_factor_rules, FactorRule, CheckResult
from agentforge.utils.console import (
    success, error, warning, info,
    print_header, print_table, bold, green, red, yellow,
)


class LintReport:
    """Aggregated linting report with scores and details."""

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.rules: List[FactorRule] = []
        self.results: Dict[str, List[CheckResult]] = {}
        self.score: int = 0
        self.total_checks: int = 0
        self.passed_checks: int = 0
        self.failed_checks: int = 0

    def to_dict(self) -> dict:
        """Serialize the report to a plain dictionary (for JSON output)."""
        rule_details = []
        for rule in self.rules:
            checks = self.results.get(rule.factor_id, [])
            rule_details.append({
                "id": rule.factor_id,
                "name": rule.name,
                "description": rule.description,
                "weight": rule.weight,
                "checks": [
                    {
                        "passed": c.passed,
                        "message": c.message,
                        "suggestion": c.suggestion,
                    }
                    for c in checks
                ],
                "passed_count": sum(1 for c in checks if c.passed),
                "total_count": len(checks),
            })
        return {
            "project_path": self.project_path,
            "score": self.score,
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "rules": rule_details,
        }


def run_lint(
    project_path: str,
    rule_ids: Optional[List[str]] = None,
) -> LintReport:
    """
    Run 12-Factor Agent compliance checks on a project.

    Parameters
    ----------
    project_path : str
        Path to the project directory to lint.
    rule_ids : list of str, optional
        If provided, only evaluate the specified rule IDs (e.g. ["F01", "F07"]).

    Returns
    -------
    LintReport
        Aggregated results with a compliance score.
    """
    abs_path = os.path.abspath(project_path)
    report = LintReport(abs_path)

    all_rules = get_twelve_factor_rules()

    # Filter rules if specific IDs were requested
    if rule_ids:
        rule_set = set(r.upper() for r in rule_ids)
        all_rules = [r for r in all_rules if r.factor_id.upper() in rule_set]

    report.rules = all_rules

    # Evaluate each rule
    for rule in all_rules:
        results = rule.evaluate(abs_path)
        report.results[rule.factor_id] = results
        for r in results:
            report.total_checks += 1
            if r.passed:
                report.passed_checks += 1
            else:
                report.failed_checks += 1

    # Calculate weighted score (0-100)
    report.score = _calculate_score(report)

    return report


def _calculate_score(report: LintReport) -> int:
    """
    Calculate a 0-100 compliance score.

    The score is weighted by factor importance:
    - Each factor contributes (passed / total) * weight
    - Maximum possible score = sum of all weights
    - Final score = (actual / maximum) * 100
    """
    if not report.rules:
        return 0

    max_score = 0
    actual_score = 0

    for rule in report.rules:
        checks = report.results.get(rule.factor_id, [])
        total = len(checks)
        passed = sum(1 for c in checks if c.passed)
        weight = rule.weight

        max_score += weight
        if total > 0:
            actual_score += (passed / total) * weight

    if max_score == 0:
        return 0

    return round((actual_score / max_score) * 100)


def format_report_table(report: LintReport) -> str:
    """Format the lint report as a human-readable table."""
    output_parts: List[str] = []

    # Header
    output_parts.append("")
    output_parts.append(f"  {bold('12-Factor Agent Compliance Report')}")
    output_parts.append(f"  Project: {report.project_path}")
    output_parts.append("")

    # Score
    score_color = green if report.score >= 80 else (yellow if report.score >= 50 else red)
    output_parts.append(f"  Overall Score: {score_color(str(report.score))}/100")
    output_parts.append(
        f"  Checks: {green(str(report.passed_checks))} passed, "
        f"{red(str(report.failed_checks))} failed, "
        f"{report.total_checks} total"
    )
    output_parts.append("")

    # Per-rule details
    headers = ["ID", "Factor", "Weight", "Status", "Details"]
    rows = []

    for rule in report.rules:
        checks = report.results.get(rule.factor_id, [])
        passed = sum(1 for c in checks if c.passed)
        total = len(checks)
        all_passed = passed == total and total > 0

        status = green("PASS") if all_passed else (yellow("PARTIAL") if passed > 0 else red("FAIL"))

        # Build detail string
        details = f"{passed}/{total}"
        if not all_passed:
            failed_msgs = [c.message for c in checks if not c.passed]
            if failed_msgs:
                details += f" - {'; '.join(failed_msgs[:2])}"

        rows.append([
            rule.factor_id,
            rule.name,
            str(rule.weight),
            status,
            details,
        ])

    # Print header and table
    print("\n".join(output_parts))
    print_table(headers, rows)

    # Suggestions
    suggestion_lines: List[str] = []
    suggestion_lines.append("")
    suggestion_lines.append(f"  {bold('Suggestions:')}")
    suggestion_lines.append("")

    has_suggestions = False
    for rule in report.rules:
        checks = report.results.get(rule.factor_id, [])
        for c in checks:
            if not c.passed and c.suggestion:
                has_suggestions = True
                suggestion_lines.append(f"  {yellow('[!]')} [{rule.factor_id}] {c.suggestion}")

    if not has_suggestions:
        suggestion_lines.append(f"  {green('All checks passed! No suggestions.')}")

    print("\n".join(suggestion_lines))

    return ""


def format_report_json(report: LintReport) -> str:
    """Format the lint report as JSON."""
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)


# Need List for type annotation in format_report_table
from typing import List  # noqa: E402 (already imported above, kept for clarity)
