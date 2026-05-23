"""
Command handler for `agentforge lint` -- run 12-Factor Agent compliance checks.
"""

import argparse
import sys

from agentforge.core.linter import run_lint, format_report_table, format_report_json
from agentforge.utils.console import error, print_header


def cmd_lint(args: argparse.Namespace) -> int:
    """
    Execute the 'lint' command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments with: path, format, rules.

    Returns
    -------
    int
        Exit code (0 for success, 1 for failure).
    """
    report = run_lint(
        project_path=args.path,
        rule_ids=args.rules,
    )

    if args.format == "json":
        print(format_report_json(report))
    else:
        print(format_report_table(report))

    # Return non-zero if score is below threshold
    return 0 if report.score >= 50 else 1
