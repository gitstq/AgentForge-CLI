"""
Unit tests for the AgentForge-CLI argument parser.

Tests cover subcommand parsing, argument validation, and default values.
"""

import unittest
from argparse import Namespace

from agentforge.cli import build_parser


class TestCLIParser(unittest.TestCase):
    """Tests for the CLI argument parser."""

    def setUp(self) -> None:
        self.parser = build_parser()

    def test_no_args_shows_help(self) -> None:
        """Parsing with no arguments should not set a command."""
        args = self.parser.parse_args([])
        self.assertIsNone(args.command)

    def test_version_flag(self) -> None:
        """The -V flag should trigger version display."""
        with self.assertRaises(SystemExit) as ctx:
            self.parser.parse_args(["-V"])
        self.assertEqual(ctx.exception.code, 0)

    def test_init_required_name(self) -> None:
        """The init command requires --name."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["init"])

    def test_init_defaults(self) -> None:
        """The init command should have correct defaults."""
        args = self.parser.parse_args(["init", "--name", "test-bot"])
        self.assertEqual(args.name, "test-bot")
        self.assertEqual(args.template, "minimal")
        self.assertEqual(args.output_dir, ".")
        self.assertEqual(args.description, "An AI agent built with AgentForge")

    def test_init_full_template(self) -> None:
        """The init command should accept 'full' template."""
        args = self.parser.parse_args([
            "init", "--name", "bot", "--template", "full",
        ])
        self.assertEqual(args.template, "full")

    def test_init_mcp_template(self) -> None:
        """The init command should accept 'mcp' template."""
        args = self.parser.parse_args([
            "init", "--name", "bot", "--template", "mcp",
        ])
        self.assertEqual(args.template, "mcp")

    def test_init_custom_output(self) -> None:
        """The init command should accept custom output directory."""
        args = self.parser.parse_args([
            "init", "--name", "bot", "--output-dir", "/tmp/projects",
        ])
        self.assertEqual(args.output_dir, "/tmp/projects")

    def test_init_custom_description(self) -> None:
        """The init command should accept custom description."""
        args = self.parser.parse_args([
            "init", "--name", "bot", "--description", "My custom agent",
        ])
        self.assertEqual(args.description, "My custom agent")

    def test_lint_defaults(self) -> None:
        """The lint command should default to current directory and table format."""
        args = self.parser.parse_args(["lint"])
        self.assertEqual(args.path, ".")
        self.assertEqual(args.format, "table")
        self.assertIsNone(args.rules)

    def test_lint_custom_path(self) -> None:
        """The lint command should accept a custom path."""
        args = self.parser.parse_args(["lint", "--path", "/some/project"])
        self.assertEqual(args.path, "/some/project")

    def test_lint_json_format(self) -> None:
        """The lint command should accept json format."""
        args = self.parser.parse_args(["lint", "--format", "json"])
        self.assertEqual(args.format, "json")

    def test_lint_specific_rules(self) -> None:
        """The lint command should accept specific rule IDs."""
        args = self.parser.parse_args(["lint", "--rules", "F01", "F07"])
        self.assertEqual(args.rules, ["F01", "F07"])

    def test_doctor_defaults(self) -> None:
        """The doctor command should default to current directory."""
        args = self.parser.parse_args(["doctor"])
        self.assertEqual(args.path, ".")
        self.assertFalse(args.verbose)

    def test_doctor_verbose(self) -> None:
        """The doctor command should accept --verbose flag."""
        args = self.parser.parse_args(["doctor", "--verbose"])
        self.assertTrue(args.verbose)

    def test_template_list(self) -> None:
        """The template command should accept --list flag."""
        args = self.parser.parse_args(["template", "--list"])
        self.assertTrue(args.list_templates)

    def test_template_info(self) -> None:
        """The template command should accept --info with a name."""
        args = self.parser.parse_args(["template", "--info", "minimal"])
        self.assertEqual(args.info, "minimal")

    def test_invalid_template_rejected(self) -> None:
        """The init command should reject invalid template names."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args([
                "init", "--name", "bot", "--template", "nonexistent",
            ])


if __name__ == "__main__":
    unittest.main()
