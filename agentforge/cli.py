"""
CLI argument parser for AgentForge-CLI.

Provides subcommands: init, lint, doctor, template, version.
Uses only argparse from the Python standard library.
"""

import argparse
import sys

from agentforge import __version__
from agentforge.commands.init import cmd_init
from agentforge.commands.lint import cmd_lint
from agentforge.commands.doctor import cmd_doctor
from agentforge.commands.template import cmd_template


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="agentforge",
        description="AgentForge-CLI: AI Agent engineering scaffold and compliance checking engine.",
        epilog="Use 'agentforge <command> --help' for more information on a specific command.",
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"agentforge {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── init ──────────────────────────────────────────────────────────────
    p_init = subparsers.add_parser(
        "init",
        help="Scaffold a new AI agent project from a template.",
    )
    p_init.add_argument(
        "--name", required=True,
        help="Project name (used for directory and package naming).",
    )
    p_init.add_argument(
        "--template", choices=["minimal", "full", "mcp"], default="minimal",
        help="Template to use (default: minimal).",
    )
    p_init.add_argument(
        "--output-dir", default=".",
        help="Directory where the project will be created (default: current directory).",
    )
    p_init.add_argument(
        "--description", default="An AI agent built with AgentForge",
        help="Project description for README and metadata.",
    )

    # ── lint ──────────────────────────────────────────────────────────────
    p_lint = subparsers.add_parser(
        "lint",
        help="Run 12-Factor Agent compliance checks on a project.",
    )
    p_lint.add_argument(
        "--path", default=".",
        help="Path to the project directory (default: current directory).",
    )
    p_lint.add_argument(
        "--format", choices=["table", "json"], default="table",
        help="Output format (default: table).",
    )
    p_lint.add_argument(
        "--rules",
        nargs="*",
        help="Specific rule IDs to check (e.g., F01 F02). Checks all if omitted.",
    )

    # ── doctor ────────────────────────────────────────────────────────────
    p_doctor = subparsers.add_parser(
        "doctor",
        help="Run health diagnostics on an AI agent project.",
    )
    p_doctor.add_argument(
        "--path", default=".",
        help="Path to the project directory (default: current directory).",
    )
    p_doctor.add_argument(
        "--verbose", action="store_true",
        help="Show detailed diagnostic information.",
    )

    # ── template ──────────────────────────────────────────────────────────
    p_tpl = subparsers.add_parser(
        "template",
        help="Browse and inspect available project templates.",
    )
    p_tpl.add_argument(
        "--list", action="store_true", dest="list_templates",
        help="List all available templates.",
    )
    p_tpl.add_argument(
        "--info",
        metavar="NAME",
        help="Show detailed information about a specific template.",
    )

    return parser


def main() -> int:
    """Parse arguments and dispatch to the appropriate command handler."""
    parser = build_parser()
    args = parser.parse_args()

    # No subcommand given -- print help
    if args.command is None:
        parser.print_help()
        return 0

    dispatch = {
        "init": cmd_init,
        "lint": cmd_lint,
        "doctor": cmd_doctor,
        "template": cmd_template,
    }

    handler = dispatch.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
