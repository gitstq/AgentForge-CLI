"""
Health diagnostics engine for AgentForge-CLI.

Performs comprehensive health checks on an AI agent project, including
Python version compatibility, required files, security issues, dependency
health, and code quality indicators.
"""

import os
import re
import sys
import subprocess
from typing import Dict, List, Optional, Tuple

from agentforge.utils.console import success, error, warning, info, bold, print_header, print_table
from agentforge.utils.file_ops import (
    has_file,
    list_files,
    read_file,
    get_python_files,
)


class DiagnosticResult:
    """Result of a single diagnostic check."""

    def __init__(
        self,
        category: str,
        name: str,
        status: str,  # "pass", "warn", "fail"
        message: str,
        details: str = "",
    ):
        self.category = category
        self.name = name
        self.status = status
        self.message = message
        self.details = details


def run_diagnostics(project_path: str, verbose: bool = False) -> List[DiagnosticResult]:
    """
    Run all health diagnostics on a project.

    Parameters
    ----------
    project_path : str
        Path to the project directory.
    verbose : bool
        If True, include extra detail in output.

    Returns
    -------
    list of DiagnosticResult
    """
    abs_path = os.path.abspath(project_path)
    results: List[DiagnosticResult] = []

    # ── Python Version ────────────────────────────────────────────────────
    results.extend(_check_python_version(verbose))

    # ── Required Files ────────────────────────────────────────────────────
    results.extend(_check_required_files(abs_path, verbose))

    # ── Security ──────────────────────────────────────────────────────────
    results.extend(_check_security(abs_path, verbose))

    # ── Dependencies ──────────────────────────────────────────────────────
    results.extend(_check_dependencies(abs_path, verbose))

    # ── Code Quality ──────────────────────────────────────────────────────
    results.extend(_check_code_quality(abs_path, verbose))

    # ── Agent-Specific ────────────────────────────────────────────────────
    results.extend(_check_agent_specific(abs_path, verbose))

    return results


def _check_python_version(verbose: bool) -> List[DiagnosticResult]:
    """Check Python version compatibility."""
    results: List[DiagnosticResult] = []
    version = sys.version_info

    if version >= (3, 8):
        results.append(DiagnosticResult(
            category="Environment",
            name="Python Version",
            status="pass",
            message=f"Python {version.major}.{version.minor}.{version.micro}",
            details="Compatible with Python >= 3.8" if verbose else "",
        ))
    else:
        results.append(DiagnosticResult(
            category="Environment",
            name="Python Version",
            status="fail",
            message=f"Python {version.major}.{version.minor}.{version.micro} (requires >= 3.8)",
        ))

    return results


def _check_required_files(project_path: str, verbose: bool) -> List[DiagnosticResult]:
    """Check for required project files."""
    results: List[DiagnosticResult] = []

    required_files = {
        "README.md": "high",
        "requirements.txt": "high",
        ".env.example": "medium",
        ".gitignore": "medium",
        "setup.py": "low",
        "pyproject.toml": "low",
    }

    for filename, priority in required_files.items():
        exists = has_file(project_path, filename)
        status = "pass" if exists else ("warn" if priority == "low" else "fail")
        message = f"{filename} {'found' if exists else 'missing'}"
        results.append(DiagnosticResult(
            category="Project Structure",
            name=f"File: {filename}",
            status=status,
            message=message,
        ))

    # Check for agent entry point
    py_files = get_python_files(project_path)
    has_agent = any("agent" in os.path.basename(f).lower() for f in py_files)
    results.append(DiagnosticResult(
        category="Project Structure",
        name="Agent Entry Point",
        status="pass" if has_agent else "warn",
        message=f"Agent module {'found' if has_agent else 'not found'}",
    ))

    return results


def _check_security(project_path: str, verbose: bool) -> List[DiagnosticResult]:
    """Check for common security issues."""
    results: List[DiagnosticResult] = []

    # Check for .env in repo (should be gitignored)
    env_path = os.path.join(project_path, ".env")
    gitignore_path = os.path.join(project_path, ".gitignore")

    if os.path.isfile(env_path):
        # Check if .env is in .gitignore
        gitignore_content = read_file(gitignore_path) or ""
        if ".env" in gitignore_content:
            results.append(DiagnosticResult(
                category="Security",
                name=".env Protection",
                status="pass",
                message=".env exists and is gitignored",
            ))
        else:
            results.append(DiagnosticResult(
                category="Security",
                name=".env Protection",
                status="fail",
                message=".env exists but is NOT in .gitignore",
                details="Add .env to your .gitignore to prevent committing secrets.",
            ))
    else:
        results.append(DiagnosticResult(
            category="Security",
            name=".env Protection",
            status="warn",
            message=".env not found (expected for local development)",
        ))

    # Check for hardcoded secrets
    secret_patterns = [
        (r'(?:api_key|apikey|secret|token|password)\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded secret"),
        (r'(?:sk-|pk-|ghp_|gho_|xox[bpas]-)[a-zA-Z0-9]{16,}', "API key pattern"),
    ]

    py_files = get_python_files(project_path)
    found_secrets = False
    for fpath in py_files:
        content = read_file(fpath)
        if content is None:
            continue
        for pattern, desc in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                rel = os.path.relpath(fpath, project_path)
                results.append(DiagnosticResult(
                    category="Security",
                    name=f"Secret in {rel}",
                    status="fail",
                    message=f"Potential {desc} detected",
                    details=f"File: {rel}" if verbose else "",
                ))
                found_secrets = True

    if not found_secrets:
        results.append(DiagnosticResult(
            category="Security",
            name="Hardcoded Secrets",
            status="pass",
            message="No hardcoded secrets detected",
        ))

    return results


def _check_dependencies(project_path: str, verbose: bool) -> List[DiagnosticResult]:
    """Check dependency health."""
    results: List[DiagnosticResult] = []

    req_path = os.path.join(project_path, "requirements.txt")
    if not os.path.isfile(req_path):
        results.append(DiagnosticResult(
            category="Dependencies",
            name="requirements.txt",
            status="warn",
            message="requirements.txt not found",
        ))
        return results

    content = read_file(req_path) or ""
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]

    if not lines:
        results.append(DiagnosticResult(
            category="Dependencies",
            name="requirements.txt",
            status="warn",
            message="requirements.txt is empty",
        ))
        return results

    results.append(DiagnosticResult(
        category="Dependencies",
        name="requirements.txt",
        status="pass",
        message=f"{len(lines)} dependencies listed",
        details="\n".join(f"  - {line}" for line in lines) if verbose else "",
    ))

    # Check for pinned versions
    pinned = sum(1 for l in lines if "==" in l)
    if pinned == len(lines) and len(lines) > 0:
        results.append(DiagnosticResult(
            category="Dependencies",
            name="Version Pinning",
            status="pass",
            message="All dependencies have pinned versions",
        ))
    elif pinned > 0:
        results.append(DiagnosticResult(
            category="Dependencies",
            name="Version Pinning",
            status="warn",
            message=f"{pinned}/{len(lines)} dependencies have pinned versions",
            details="Consider pinning all versions for reproducibility." if verbose else "",
        ))
    else:
        results.append(DiagnosticResult(
            category="Dependencies",
            name="Version Pinning",
            status="warn",
            message="No dependencies have pinned versions",
            details="Pin versions (e.g., package==1.0.0) for reproducibility.",
        ))

    return results


def _check_code_quality(project_path: str, verbose: bool) -> List[DiagnosticResult]:
    """Check code quality indicators."""
    results: List[DiagnosticResult] = []

    py_files = get_python_files(project_path)

    if not py_files:
        results.append(DiagnosticResult(
            category="Code Quality",
            name="Python Files",
            status="warn",
            message="No Python files found",
        ))
        return results

    results.append(DiagnosticResult(
        category="Code Quality",
        name="Python Files",
        status="pass",
        message=f"{len(py_files)} Python file(s) found",
    ))

    # Check for type hints
    files_with_hints = 0
    for fpath in py_files:
        content = read_file(fpath)
        if content and re.search(r"->\s*\w|:\s*\w+\s*=", content):
            files_with_hints += 1

    if files_with_hints > 0:
        results.append(DiagnosticResult(
            category="Code Quality",
            name="Type Hints",
            status="pass",
            message=f"{files_with_hints}/{len(py_files)} files use type hints",
        ))
    else:
        results.append(DiagnosticResult(
            category="Code Quality",
            name="Type Hints",
            status="warn",
            message="No type hints found",
            details="Consider adding type annotations for better maintainability.",
        ))

    # Check for docstrings
    files_with_docs = 0
    for fpath in py_files:
        content = read_file(fpath)
        if content and '"""' in content:
            files_with_docs += 1

    if files_with_docs > 0:
        results.append(DiagnosticResult(
            category="Code Quality",
            name="Docstrings",
            status="pass",
            message=f"{files_with_docs}/{len(py_files)} files have docstrings",
        ))
    else:
        results.append(DiagnosticResult(
            category="Code Quality",
            name="Docstrings",
            status="warn",
            message="No docstrings found",
            details="Add docstrings to document your code.",
        ))

    return results


def _check_agent_specific(project_path: str, verbose: bool) -> List[DiagnosticResult]:
    """Check agent-specific patterns and best practices."""
    results: List[DiagnosticResult] = []

    py_files = get_python_files(project_path)
    all_content = ""
    for fpath in py_files:
        content = read_file(fpath)
        if content:
            all_content += content + "\n"

    # Check for LLM framework usage
    frameworks = {
        "OpenAI": r"(openai|OpenAI|from openai)",
        "LangChain": r"(langchain|LangChain|from langchain)",
        "Anthropic": r"(anthropic|Anthropic|from anthropic)",
        "LlamaIndex": r"(llama_index|LlamaIndex|from llama_index)",
    }

    found_frameworks = []
    for name, pattern in frameworks.items():
        if re.search(pattern, all_content):
            found_frameworks.append(name)

    if found_frameworks:
        results.append(DiagnosticResult(
            category="Agent",
            name="LLM Framework",
            status="pass",
            message=f"Using: {', '.join(found_frameworks)}",
        ))
    else:
        results.append(DiagnosticResult(
            category="Agent",
            name="LLM Framework",
            status="warn",
            message="No recognized LLM framework detected",
            details="Consider using OpenAI, LangChain, Anthropic, or LlamaIndex.",
        ))

    # Check for tool definitions
    has_tools = bool(re.search(r"(def\s+tool|@tool|register_tool|tool_def|Tool\()", all_content))
    results.append(DiagnosticResult(
        category="Agent",
        name="Tool Definitions",
        status="pass" if has_tools else "warn",
        message=f"Tool definitions {'found' if has_tools else 'not found'}",
    ))

    # Check for prompt management
    has_prompts = bool(re.search(r"(prompt|PROMPT|system_message|template)", all_content))
    results.append(DiagnosticResult(
        category="Agent",
        name="Prompt Management",
        status="pass" if has_prompts else "warn",
        message=f"Prompt management {'found' if has_prompts else 'not found'}",
    ))

    return results


def print_diagnostic_report(results: List[DiagnosticResult], verbose: bool = False) -> None:
    """Print a formatted diagnostic report to the console."""
    print_header("AgentForge Doctor - Health Diagnostics")

    # Count statuses
    pass_count = sum(1 for r in results if r.status == "pass")
    warn_count = sum(1 for r in results if r.status == "warn")
    fail_count = sum(1 for r in results if r.status == "fail")

    # Summary line
    summary = (
        f"Results: {success.__name__ if pass_count else ''} "
        f"{pass_count} passed, {warn_count} warnings, {fail_count} failures"
    )
    print(f"  {bold('Summary')}: {pass_count} passed, {warn_count} warnings, {fail_count} failures")
    print()

    # Group by category
    categories: Dict[str, List[DiagnosticResult]] = {}
    for r in results:
        categories.setdefault(r.category, []).append(r)

    for category, items in categories.items():
        print(f"  {bold(category)}")
        for item in items:
            if item.status == "pass":
                success(item.message)
            elif item.status == "warn":
                warning(item.message)
            else:
                error(item.message)
            if verbose and item.details:
                print(f"         {item.details}")
        print()
