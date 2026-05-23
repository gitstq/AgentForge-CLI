"""
Unit tests for the AgentForge-CLI scaffolding engine.

Tests cover template resolution, placeholder replacement, and project generation.
"""

import os
import shutil
import tempfile
import unittest

from agentforge.core.scaffolder import (
    _resolve_template_dir,
    _collect_template_files,
    _process_placeholders,
    _strip_template_extension,
    scaffold_project,
)


class TestTemplateResolution(unittest.TestCase):
    """Tests for template directory resolution."""

    def test_resolve_minimal_template(self) -> None:
        """The 'minimal' template should be resolvable."""
        path = _resolve_template_dir("minimal")
        self.assertIsNotNone(path)
        self.assertTrue(os.path.isdir(path))

    def test_resolve_full_template(self) -> None:
        """The 'full' template should be resolvable."""
        path = _resolve_template_dir("full")
        self.assertIsNotNone(path)
        self.assertTrue(os.path.isdir(path))

    def test_resolve_mcp_template(self) -> None:
        """The 'mcp' template should be resolvable."""
        path = _resolve_template_dir("mcp")
        self.assertIsNotNone(path)
        self.assertTrue(os.path.isdir(path))

    def test_resolve_nonexistent_template(self) -> None:
        """A nonexistent template should return None."""
        path = _resolve_template_dir("nonexistent")
        self.assertIsNone(path)


class TestTemplateFiles(unittest.TestCase):
    """Tests for template file collection."""

    def test_collect_minimal_files(self) -> None:
        """The minimal template should have at least 5 files."""
        template_dir = _resolve_template_dir("minimal")
        files = _collect_template_files(template_dir)
        self.assertGreaterEqual(len(files), 5)

    def test_collect_full_files(self) -> None:
        """The full template should have at least 8 files."""
        template_dir = _resolve_template_dir("full")
        files = _collect_template_files(template_dir)
        self.assertGreaterEqual(len(files), 8)

    def test_collect_mcp_files(self) -> None:
        """The mcp template should have at least 5 files."""
        template_dir = _resolve_template_dir("mcp")
        files = _collect_template_files(template_dir)
        self.assertGreaterEqual(len(files), 5)

    def test_files_are_relative(self) -> None:
        """Collected file paths should be relative to the template dir."""
        template_dir = _resolve_template_dir("minimal")
        files = _collect_template_files(template_dir)
        for rel_path, abs_path in files:
            self.assertFalse(os.path.isabs(rel_path))
            self.assertTrue(abs_path.startswith(template_dir))


class TestPlaceholderProcessing(unittest.TestCase):
    """Tests for placeholder replacement."""

    def test_basic_replacement(self) -> None:
        """Simple {variable} placeholders should be replaced."""
        content = "Hello, {project_name}!"
        result = _process_placeholders(
            content,
            {"project_name": "TestBot"},
        )
        self.assertEqual(result, "Hello, TestBot!")

    def test_multiple_placeholders(self) -> None:
        """Multiple placeholders should all be replaced."""
        content = "{project_name} v{version} by {author}"
        result = _process_placeholders(
            content,
            {
                "project_name": "MyAgent",
                "version": "1.0.0",
                "author": "Test Author",
            },
        )
        self.assertEqual(result, "MyAgent v1.0.0 by Test Author")

    def test_snake_case_derivation(self) -> None:
        """project_name_snake should be derived from project_name."""
        content = "from {project_name_snake} import agent"
        result = _process_placeholders(
            content,
            {"project_name": "my-agent"},
        )
        self.assertEqual(result, "from my_agent import agent")

    def test_pascal_case_derivation(self) -> None:
        """project_name_pascal should be derived from project_name."""
        content = "class {project_name_pascal}:"
        result = _process_placeholders(
            content,
            {"project_name": "my-agent",
             "description": "",
             "author": "",
             "date": "",
             "version": ""},
        )
        self.assertEqual(result, "class MyAgent:")

    def test_no_placeholders(self) -> None:
        """Content without placeholders should remain unchanged."""
        content = "No placeholders here."
        result = _process_placeholders(content, {"project_name": "Test"})
        self.assertEqual(result, "No placeholders here.")


class TestStripExtension(unittest.TestCase):
    """Tests for .j2 extension stripping."""

    def test_strip_j2(self) -> None:
        """Files ending in .j2 should have the extension removed."""
        self.assertEqual(_strip_template_extension("agent.py.j2"), "agent.py")

    def test_no_j2(self) -> None:
        """Files without .j2 should remain unchanged."""
        self.assertEqual(_strip_template_extension("README.md"), "README.md")


class TestScaffoldProject(unittest.TestCase):
    """Integration tests for project scaffolding."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_scaffold_minimal(self) -> None:
        """Scaffolding a minimal project should succeed."""
        ok = scaffold_project(
            template_name="minimal",
            project_name="test-minimal",
            output_dir=self.temp_dir,
        )
        self.assertTrue(ok)

        project_dir = os.path.join(self.temp_dir, "test-minimal")
        self.assertTrue(os.path.isdir(project_dir))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "agent.py")))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "config.py")))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "tools.py")))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "README.md")))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, ".env.example")))

    def test_scaffold_full(self) -> None:
        """Scaffolding a full project should succeed."""
        ok = scaffold_project(
            template_name="full",
            project_name="test-full",
            output_dir=self.temp_dir,
        )
        self.assertTrue(ok)

        project_dir = os.path.join(self.temp_dir, "test-full")
        self.assertTrue(os.path.isdir(project_dir))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "memory.py")))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "prompts.py")))
        self.assertTrue(os.path.isdir(os.path.join(project_dir, "tests")))

    def test_scaffold_mcp(self) -> None:
        """Scaffolding an MCP project should succeed."""
        ok = scaffold_project(
            template_name="mcp",
            project_name="test-mcp",
            output_dir=self.temp_dir,
        )
        self.assertTrue(ok)

        project_dir = os.path.join(self.temp_dir, "test-mcp")
        self.assertTrue(os.path.isdir(project_dir))
        self.assertTrue(os.path.isfile(os.path.join(project_dir, "server.py")))

    def test_scaffold_replaces_placeholders(self) -> None:
        """Scaffolded files should have placeholders replaced."""
        scaffold_project(
            template_name="minimal",
            project_name="placeholder-test",
            output_dir=self.temp_dir,
            description="A test description",
        )

        readme_path = os.path.join(self.temp_dir, "placeholder-test", "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("placeholder-test", content)
        self.assertIn("A test description", content)
        self.assertNotIn("{project_name}", content)

    def test_scaffold_existing_dir_fails(self) -> None:
        """Scaffolding into an existing directory should fail."""
        os.makedirs(os.path.join(self.temp_dir, "existing"))
        ok = scaffold_project(
            template_name="minimal",
            project_name="existing",
            output_dir=self.temp_dir,
        )
        self.assertFalse(ok)

    def test_scaffold_invalid_template_fails(self) -> None:
        """Scaffolding with an invalid template should fail."""
        ok = scaffold_project(
            template_name="nonexistent",
            project_name="fail-test",
            output_dir=self.temp_dir,
        )
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
