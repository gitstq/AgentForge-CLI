"""
Project scaffolding engine for AgentForge-CLI.

Generates new AI agent projects from template directories using simple
string placeholder replacement (no Jinja2 or other template engines).
"""

import os
import shutil
from datetime import date
from typing import Dict, Optional

from agentforge.utils.console import success, error, info, bold, cyan
from agentforge.utils.file_ops import ensure_directory, write_file, list_files, read_file


# ── Default placeholders ──────────────────────────────────────────────────

DEFAULT_PLACEHOLDERS: Dict[str, str] = {
    "project_name": "my-agent",
    "description": "An AI agent built with AgentForge",
    "author": "AgentForge User",
    "date": date.today().isoformat(),
    "version": "0.1.0",
}


def _resolve_template_dir(template_name: str) -> Optional[str]:
    """
    Resolve a template name to its absolute directory path.

    Searches in several locations:
    1. The bundled templates/ directory at the project root (when installed).
    2. Relative to this file's parent's parent (development mode).
    3. Relative to the current working directory.
    """
    # Candidate directories to search for templates/
    candidates = []

    # Development mode: templates/ is a sibling of the agentforge/ package
    this_dir = os.path.dirname(os.path.abspath(__file__))
    pkg_dir = os.path.dirname(this_dir)          # agentforge/
    project_root = os.path.dirname(pkg_dir)      # AgentForge-CLI/
    candidates.append(os.path.join(project_root, "templates"))

    # Installed mode: templates/ might be at site-packages/agentforge/../templates
    # or alongside the package data
    candidates.append(os.path.join(pkg_dir, "templates"))

    # Current working directory
    candidates.append(os.path.join(os.getcwd(), "templates"))

    for candidate in candidates:
        template_path = os.path.join(candidate, template_name)
        if os.path.isdir(template_path):
            return template_path

    return None


def _collect_template_files(template_dir: str) -> list:
    """
    Recursively collect all files in the template directory.

    Returns a list of (relative_path, absolute_path) tuples.
    """
    files = []
    for root, _dirs, filenames in os.walk(template_dir):
        for fname in filenames:
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, template_dir)
            files.append((rel_path, abs_path))
    return files


def _process_placeholders(content: str, placeholders: Dict[str, str]) -> str:
    """
    Replace {placeholder} tokens in *content* with values from *placeholders*.

    Also derives a snake_case and PascalCase variant of project_name for
    convenience in templates.
    """
    # Derive extra convenience placeholders
    extra = {}
    name = placeholders.get("project_name", "my-agent")
    extra["project_name_snake"] = name.replace("-", "_").replace(" ", "_").lower()
    extra["project_name_pascal"] = "".join(
        word.capitalize() for word in name.replace("-", "_").replace(" ", "_").split("_") if word
    )

    merged = {**placeholders, **extra}

    for key, value in merged.items():
        content = content.replace(f"{{{key}}}", value)

    return content


def _strip_template_extension(filename: str) -> str:
    """Remove the .j2 extension from template filenames."""
    if filename.endswith(".j2"):
        return filename[:-3]
    return filename


def scaffold_project(
    template_name: str,
    project_name: str,
    output_dir: str,
    description: str = "",
    author: str = "",
) -> bool:
    """
    Scaffold a new AI agent project from a template.

    Parameters
    ----------
    template_name : str
        Name of the template (minimal, full, or mcp).
    project_name : str
        Name for the new project.
    output_dir : str
        Directory where the project will be created.
    description : str
        Project description for README and metadata.
    author : str
        Author name for project metadata.

    Returns
    -------
    bool
        True if scaffolding succeeded, False otherwise.
    """
    # Resolve template directory
    template_dir = _resolve_template_dir(template_name)
    if template_dir is None:
        error(f"Template '{template_name}' not found.")
        return False

    # Build placeholder values
    placeholders = {
        **DEFAULT_PLACEHOLDERS,
        "project_name": project_name,
        "description": description or DEFAULT_PLACEHOLDERS["description"],
        "author": author or DEFAULT_PLACEHOLDERS["author"],
    }

    # Target project directory
    project_dir = os.path.join(os.path.abspath(output_dir), project_name)

    if os.path.exists(project_dir):
        error(f"Directory already exists: {project_dir}")
        return False

    # Collect template files
    template_files = _collect_template_files(template_dir)
    if not template_files:
        error(f"No files found in template '{template_name}'.")
        return False

    info(f"Scaffolding {bold(project_name)} from {cyan(template_name)} template...")

    # Process and write each file
    created_files = []
    for rel_path, abs_path in template_files:
        content = read_file(abs_path)
        if content is None:
            warning(f"Could not read template file: {rel_path}")
            continue

        # Replace placeholders
        content = _process_placeholders(content, placeholders)

        # Strip .j2 extension
        dest_rel = _strip_template_extension(rel_path)
        dest_path = os.path.join(project_dir, dest_rel)

        # Write file
        write_file(dest_path, content)
        created_files.append(dest_rel)

    # Summary
    print()
    success(f"Project {bold(project_name)} created successfully!")
    print()
    info(f"Location: {project_dir}")
    info(f"Files created: {len(created_files)}")
    print()
    info(bold("Next steps:"))
    info(f"  cd {project_name}")
    info(f"  pip install -r requirements.txt")
    info(f"  cp .env.example .env  # then edit with your API keys")
    print()

    return True
