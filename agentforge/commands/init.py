"""
Command handler for `agentforge init` -- scaffold a new AI agent project.
"""

import argparse
import sys

from agentforge.core.scaffolder import scaffold_project
from agentforge.utils.console import error


def cmd_init(args: argparse.Namespace) -> int:
    """
    Execute the 'init' command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments with: name, template, output_dir, description.

    Returns
    -------
    int
        Exit code (0 for success, 1 for failure).
    """
    ok = scaffold_project(
        template_name=args.template,
        project_name=args.name,
        output_dir=args.output_dir,
        description=args.description,
    )
    return 0 if ok else 1
