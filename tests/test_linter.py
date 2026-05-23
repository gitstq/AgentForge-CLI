"""
Unit tests for the AgentForge-CLI 12-Factor linter.

Tests cover rule evaluation, scoring, and report formatting.
"""

import json
import os
import shutil
import tempfile
import unittest

from agentforge.core.linter import run_lint, _calculate_score, LintReport
from agentforge.rules.twelve_factor import get_twelve_factor_rules, FactorRule


class TestTwelveFactorRules(unittest.TestCase):
    """Tests for the 12-Factor rule definitions."""

    def test_all_twelve_factors_defined(self) -> None:
        """There should be exactly 12 factor rules defined."""
        rules = get_twelve_factor_rules()
        self.assertEqual(len(rules), 12)

    def test_factor_ids_are_unique(self) -> None:
        """Each factor should have a unique ID."""
        rules = get_twelve_factor_rules()
        ids = [r.factor_id for r in rules]
        self.assertEqual(len(ids), len(set(ids)))

    def test_factor_ids_sequential(self) -> None:
        """Factor IDs should be F01 through F12."""
        rules = get_twelve_factor_rules()
        expected = {f"F{i:02d}" for i in range(1, 13)}
        actual = {r.factor_id for r in rules}
        self.assertEqual(actual, expected)

    def test_each_factor_has_checks(self) -> None:
        """Each factor should have at least one check function."""
        rules = get_twelve_factor_rules()
        for rule in rules:
            self.assertGreater(len(rule.checks), 0, f"{rule.factor_id} has no checks")

    def test_each_factor_has_weight(self) -> None:
        """Each factor should have a positive weight."""
        rules = get_twelve_factor_rules()
        for rule in rules:
            self.assertGreater(rule.weight, 0, f"{rule.factor_id} has no weight")


class TestLinterOnEmptyDir(unittest.TestCase):
    """Tests for linting an empty directory."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_lint_empty_dir(self) -> None:
        """Linting an empty directory should produce a low score."""
        report = run_lint(self.temp_dir)
        self.assertIsInstance(report, LintReport)
        self.assertLess(report.score, 50)
        self.assertGreater(report.total_checks, 0)

    def test_lint_empty_dir_has_failures(self) -> None:
        """Linting an empty directory should have many failures."""
        report = run_lint(self.temp_dir)
        self.assertGreater(report.failed_checks, 0)


class TestLinterOnGoodProject(unittest.TestCase):
    """Tests for linting a well-structured project."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        # Create a well-structured project
        project_dir = os.path.join(self.temp_dir, "good-project")
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, "tests"))

        # Create essential files
        files = {
            "README.md": "# Good Project\n\nA well-structured agent.",
            "requirements.txt": "openai>=1.0.0\npython-dotenv>=1.0.0",
            ".env.example": "API_KEY=your-key-here\n",
            ".gitignore": ".env\n__pycache__/\n",
            "pyproject.toml": "[project]\nname = 'good-project'\n",
            "agent.py": (
                '"""Agent module with context isolation."""\n'
                "import logging\n"
                "import os\n"
                "import json\n\n"
                "logger = logging.getLogger(__name__)\n\n"
                "SYSTEM_PROMPT = 'You are a helpful assistant.'\n\n"
                "def run_agent(user_input: str) -> str:\n"
                '    """Run the agent with user input."""\n'
                "    try:\n"
                "        result = process(user_input)\n"
                "        return result\n"
                "    except Exception as e:\n"
                "        logger.error('Error: %s', e)\n"
                "        return str(e)\n\n"
                "def process(data: str) -> str:\n"
                "    return data.upper()\n"
            ),
            "tools.py": (
                '"""Tool definitions."""\n'
                "from dataclasses import dataclass\n"
                "from typing import Any, Dict\n\n"
                "@dataclass\n"
                "class ToolInput:\n"
                "    query: str\n\n"
                "def search_tool(query: str) -> Dict[str, Any]:\n"
                '    """Search for information."""\n'
                "    return {'result': query}\n"
            ),
            "tests/test_agent.py": (
                "import unittest\n\n"
                "class TestAgent(unittest.TestCase):\n"
                "    def test_run(self):\n"
                "        self.assertTrue(True)\n"
            ),
        }

        for filename, content in files.items():
            with open(os.path.join(project_dir, filename), "w") as f:
                f.write(content)

        self.project_dir = project_dir

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_lint_good_project_better_score(self) -> None:
        """A well-structured project should score higher than an empty dir."""
        report = run_lint(self.project_dir)
        self.assertGreater(report.score, 30)

    def test_lint_good_project_has_passes(self) -> None:
        """A well-structured project should have some passing checks."""
        report = run_lint(self.project_dir)
        self.assertGreater(report.passed_checks, 0)

    def test_lint_specific_rules(self) -> None:
        """Linting specific rules should only evaluate those rules."""
        report = run_lint(self.project_dir, rule_ids=["F10", "F11"])
        # Should have fewer total checks than a full lint
        full_report = run_lint(self.project_dir)
        self.assertLessEqual(report.total_checks, full_report.total_checks)


class TestLintReport(unittest.TestCase):
    """Tests for the LintReport data structure."""

    def test_report_to_dict(self) -> None:
        """Report should be serializable to a dictionary."""
        report = LintReport("/fake/path")
        report.score = 75
        report.total_checks = 20
        report.passed_checks = 15
        report.failed_checks = 5

        d = report.to_dict()
        self.assertEqual(d["score"], 75)
        self.assertEqual(d["total_checks"], 20)
        self.assertEqual(d["passed_checks"], 15)
        self.assertEqual(d["failed_checks"], 5)
        self.assertEqual(d["project_path"], "/fake/path")

    def test_report_to_json(self) -> None:
        """Report should be JSON-serializable."""
        report = LintReport("/fake/path")
        report.score = 50
        report.total_checks = 10
        report.passed_checks = 5
        report.failed_checks = 5

        d = report.to_dict()
        json_str = json.dumps(d)
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["score"], 50)


class TestScoreCalculation(unittest.TestCase):
    """Tests for the score calculation algorithm."""

    def test_all_pass_is_100(self) -> None:
        """All checks passing should yield a score of 100."""
        report = LintReport("/test")
        from agentforge.rules.twelve_factor import FactorRule, CheckResult

        rule = FactorRule("F01", "Test", "Test rule", weight=1)
        report.rules = [rule]
        report.results = {
            "F01": [CheckResult(True, "ok"), CheckResult(True, "ok")],
        }
        report.total_checks = 2
        report.passed_checks = 2
        report.failed_checks = 0
        self.assertEqual(_calculate_score(report), 100)

    def test_no_rules_is_0(self) -> None:
        """No rules should yield a score of 0."""
        report = LintReport("/test")
        report.rules = []
        self.assertEqual(_calculate_score(report), 0)


if __name__ == "__main__":
    unittest.main()
