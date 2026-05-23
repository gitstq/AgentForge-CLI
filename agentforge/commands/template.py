"""
Command handler for `agentforge template` -- browse and inspect templates.
"""

import argparse

from agentforge.core.template_manager import print_template_list, print_template_info
from agentforge.utils.console import error


def cmd_template(args: argparse.Namespace) -> int:
    """
    Execute the 'template' command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments with: list_templates, info.

    Returns
    -------
    int
        Exit code (0 for success, 1 for failure).
    """
    if args.list_templates:
        print_template_list()
        return 0

    if args.info:
        if print_template_info(args.info):
            return 0
        else:
            error(f"Template '{args.info}' not found.")
            error("Available templates: minimal, full, mcp")
            return 1

    # No flags -- default to listing
    print_template_list()
    return 0
