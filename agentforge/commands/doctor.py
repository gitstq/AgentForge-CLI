"""
Command handler for `agentforge doctor` -- run health diagnostics.
"""

import argparse

from agentforge.core.doctor_engine import run_diagnostics, print_diagnostic_report
from agentforge.utils.console import error


def cmd_doctor(args: argparse.Namespace) -> int:
    """
    Execute the 'doctor' command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments with: path, verbose.

    Returns
    -------
    int
        Exit code (0 for success, 1 for failure).
    """
    results = run_diagnostics(
        project_path=args.path,
        verbose=args.verbose,
    )

    print_diagnostic_report(results, verbose=args.verbose)

    # Return non-zero if any failures
    has_failures = any(r.status == "fail" for r in results)
    return 1 if has_failures else 0
