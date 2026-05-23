"""
12-Factor Agent methodology rules definitions.

Each factor defines:
- id: Short identifier (e.g. "F01")
- name: Human-readable factor name
- description: What this factor checks
- weight: Importance weight for scoring (1-3)
- checks: List of concrete check functions
"""

import os
import re
from typing import Callable, Dict, List, Optional, Any

from agentforge.utils.file_ops import (
    list_files,
    read_file,
    has_file,
    get_python_files,
)


# ── Data structures ───────────────────────────────────────────────────────

class CheckResult:
    """Result of a single compliance check."""

    def __init__(self, passed: bool, message: str, suggestion: str = ""):
        self.passed = passed
        self.message = message
        self.suggestion = suggestion

    def __repr__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"<CheckResult [{status}] {self.message}>"


class FactorRule:
    """Definition of a single 12-Factor Agent rule."""

    def __init__(
        self,
        factor_id: str,
        name: str,
        description: str,
        weight: int = 1,
        checks: Optional[List[Callable]] = None,
    ):
        self.factor_id = factor_id
        self.name = name
        self.description = description
        self.weight = weight
        self.checks = checks or []

    def evaluate(self, project_path: str) -> List[CheckResult]:
        """Run all checks for this factor against the project."""
        results: List[CheckResult] = []
        for check_fn in self.checks:
            try:
                result = check_fn(project_path)
                if isinstance(result, list):
                    results.extend(result)
                else:
                    results.append(result)
            except Exception as exc:
                results.append(
                    CheckResult(False, f"Check raised an error: {exc}")
                )
        return results


# ── Check helper ──────────────────────────────────────────────────────────

def _any_file_contains(project_path: str, pattern: str, extensions: Optional[List[str]] = None) -> bool:
    """Return True if any file (optionally filtered by extension) matches *pattern*."""
    files = list_files(project_path, extensions=extensions)
    regex = re.compile(pattern, re.IGNORECASE)
    for fpath in files:
        content = read_file(fpath)
        if content and regex.search(content):
            return True
    return False


def _file_exists_check(filename: str, message: str, suggestion: str = "") -> Callable:
    """Return a check function that verifies a specific file exists."""
    def check(project_path: str) -> CheckResult:
        exists = has_file(project_path, filename)
        return CheckResult(
            exists,
            message,
            suggestion or f"Create a {filename} file in your project root.",
        )
    return check


def _pattern_check(
    pattern: str,
    message: str,
    extensions: Optional[List[str]] = None,
    suggestion: str = "",
) -> Callable:
    """Return a check function that looks for a regex pattern in project files."""
    def check(project_path: str) -> CheckResult:
        found = _any_file_contains(project_path, pattern, extensions=extensions)
        return CheckResult(found, message, suggestion)
    return check


# ── 12 Factor definitions ─────────────────────────────────────────────────

def get_twelve_factor_rules() -> List[FactorRule]:
    """
    Return the complete list of 12-Factor Agent rules.

    Each rule contains multiple checks that evaluate different aspects
    of the factor.
    """
    rules: List[FactorRule] = []

    # ── F01: Context Isolation ────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F01",
        name="Context Isolation",
        description="Agent has separate context management (not mixing system/user/tool contexts)",
        weight=2,
        checks=[
            _pattern_check(
                r"(system_prompt|SYSTEM|system_message|SystemMessage)",
                "System context is explicitly defined",
                extensions=[".py"],
                suggestion="Define a separate system prompt/context variable.",
            ),
            _pattern_check(
                r"(user_message|user_input|UserMessage|human_input)",
                "User context handling is present",
                extensions=[".py"],
                suggestion="Add explicit user message/context handling.",
            ),
            _pattern_check(
                r"(tool_result|ToolMessage|function_result)",
                "Tool result context is handled separately",
                extensions=[".py"],
                suggestion="Separate tool results from other message types.",
            ),
        ],
    ))

    # ── F02: Tool Interface ───────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F02",
        name="Tool Interface",
        description="Tools have clear input/output schemas (JSON Schema or Pydantic)",
        weight=2,
        checks=[
            _pattern_check(
                r"(BaseModel|pydantic|TypedDict|dataclass)",
                "Tools use structured input/output types",
                extensions=[".py"],
                suggestion="Use Pydantic BaseModel, TypedDict, or dataclass for tool schemas.",
            ),
            _pattern_check(
                r"(description|docstring|\"\"\".*input|\"\"\".*param)",
                "Tool functions have descriptive documentation",
                extensions=[".py"],
                suggestion="Add docstrings describing tool inputs and outputs.",
            ),
            _pattern_check(
                r"(def\s+\w+\s*\([^)]*\)\s*->|return_type|->\s*(str|dict|list|bool|None|Any))",
                "Tool functions have return type annotations",
                extensions=[".py"],
                suggestion="Add type annotations to tool function signatures.",
            ),
        ],
    ))

    # ── F03: Control Flow ─────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F03",
        name="Control Flow",
        description="Agent has explicit control flow (not just free-form generation)",
        weight=2,
        checks=[
            _pattern_check(
                r"(while\s+|for\s+|if\s+.*elif|state_machine|workflow|pipeline|step)",
                "Agent has explicit control flow logic",
                extensions=[".py"],
                suggestion="Implement structured control flow (loops, conditionals, state machine).",
            ),
            _pattern_check(
                r"(max_iterations|max_steps|max_retries|loop_limit)",
                "Agent has iteration/loop limits",
                extensions=[".py"],
                suggestion="Add max_iterations or similar safeguards to prevent infinite loops.",
            ),
        ],
    ))

    # ── F04: State Management ─────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F04",
        name="State Management",
        description="Agent state is externalized (not in-memory only)",
        weight=2,
        checks=[
            _pattern_check(
                r"(json\.dump|json\.load|save_state|load_state|persist|serialize|to_dict|from_dict)",
                "State persistence mechanism exists",
                extensions=[".py"],
                suggestion="Implement state serialization (JSON, database, file).",
            ),
            _pattern_check(
                r"(class\s+\w*[Ss]tate|state\s*[:=]|self\.state)",
                "State is managed as a structured object",
                extensions=[".py"],
                suggestion="Use a class or dataclass to manage agent state.",
            ),
        ],
    ))

    # ── F05: Error Handling ───────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F05",
        name="Error Handling",
        description="Graceful error handling with retry logic",
        weight=2,
        checks=[
            _pattern_check(
                r"(try\s*:|except\s+|raise\s+|Exception)",
                "Exception handling is present",
                extensions=[".py"],
                suggestion="Add try/except blocks for error-prone operations.",
            ),
            _pattern_check(
                r"(retry|backoff|tenacity|exponential)",
                "Retry logic is implemented",
                extensions=[".py"],
                suggestion="Implement retry logic with exponential backoff.",
            ),
            _pattern_check(
                r"(fallback|default_value|or\s+[\"'])",
                "Fallback/default values are provided",
                extensions=[".py"],
                suggestion="Add fallback behavior for when operations fail.",
            ),
        ],
    ))

    # ── F06: Observability ────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F06",
        name="Observability",
        description="Logging/tracing for agent decisions",
        weight=1,
        checks=[
            _pattern_check(
                r"(import logging|logger|getLogger|log\.info|log\.debug|log\.error)",
                "Logging is configured",
                extensions=[".py"],
                suggestion="Set up Python logging for agent decision tracking.",
            ),
            _pattern_check(
                r"(trace|span|telemetry|metric|counter)",
                "Tracing or metrics are present",
                extensions=[".py"],
                suggestion="Add distributed tracing or metrics collection.",
            ),
        ],
    ))

    # ── F07: Security ─────────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F07",
        name="Security",
        description="Input validation, output sanitization, no hardcoded secrets",
        weight=3,
        checks=[
            # Negative check: should NOT find hardcoded API keys
            _security_no_hardcoded_secrets(),
            _file_exists_check(
                ".env.example",
                "Environment variable documentation exists (.env.example)",
                suggestion="Create a .env.example file documenting required environment variables.",
            ),
            _pattern_check(
                r"(validate|sanitize|escape|clean_input|input_check|verify)",
                "Input validation is present",
                extensions=[".py"],
                suggestion="Add input validation before processing user data.",
            ),
        ],
    ))

    # ── F08: Testing ──────────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F08",
        name="Testing",
        description="Unit tests for tools and agent logic",
        weight=2,
        checks=[
            _file_exists_check(
                "tests",
                "Tests directory exists",
                suggestion="Create a tests/ directory with unit tests.",
            ),
            _pattern_check(
                r"(def test_|class Test|import unittest|import pytest|@pytest|@patch)",
                "Test functions or classes are defined",
                extensions=[".py"],
                suggestion="Write unit tests for tools and agent logic.",
            ),
        ],
    ))

    # ── F09: Configuration ────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F09",
        name="Configuration",
        description="Environment-based config, not hardcoded values",
        weight=2,
        checks=[
            _pattern_check(
                r"(os\.environ|os\.getenv|dotenv|load_dotenv|env_var|ENV)",
                "Environment variables are used for configuration",
                extensions=[".py"],
                suggestion="Use os.environ or python-dotenv for configuration.",
            ),
            _pattern_check(
                r"(config|settings|Config|Settings|configuration)",
                "Configuration management is in place",
                extensions=[".py"],
                suggestion="Create a config.py or settings module.",
            ),
            _file_exists_check(
                ".env.example",
                "Environment template file exists",
                suggestion="Create .env.example to document required env vars.",
            ),
        ],
    ))

    # ── F10: Documentation ────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F10",
        name="Documentation",
        description="README, API docs, usage examples",
        weight=1,
        checks=[
            _file_exists_check(
                "README.md",
                "README.md exists",
                suggestion="Create a README.md with project overview and usage instructions.",
            ),
            _pattern_check(
                r"(\"\"\"[\s\S]*?\"\"\"|class\s+\w+.*?:\s*\"\"\"|def\s+\w+.*?:\s*\"\"\")",
                "Python docstrings are present",
                extensions=[".py"],
                suggestion="Add docstrings to all public classes and functions.",
            ),
        ],
    ))

    # ── F11: Dependency Management ────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F11",
        name="Dependency Management",
        description="Proper requirements.txt or pyproject.toml",
        weight=1,
        checks=[
            _file_exists_check(
                "requirements.txt",
                "requirements.txt exists",
                suggestion="Create requirements.txt listing all dependencies.",
            ),
            _file_exists_check(
                "pyproject.toml",
                "pyproject.toml exists",
                suggestion="Create pyproject.toml for modern Python packaging.",
            ),
        ],
    ))

    # ── F12: Deployment ───────────────────────────────────────────────────
    rules.append(FactorRule(
        factor_id="F12",
        name="Deployment",
        description="Docker support or deployment instructions",
        weight=1,
        checks=[
            _file_exists_check(
                "Dockerfile",
                "Dockerfile exists",
                suggestion="Add a Dockerfile for containerized deployment.",
            ),
            _file_exists_check(
                "docker-compose.yml",
                "docker-compose.yml exists",
                suggestion="Add docker-compose.yml for multi-container setups.",
            ),
            _pattern_check(
                r"(deploy|deployment|Docker|container|CI|CD|pipeline)",
                "Deployment documentation or configuration is present",
                extensions=[".md", ".yml", ".yaml"],
                suggestion="Add deployment instructions to README or a separate guide.",
            ),
        ],
    ))

    return rules


# ── Special check functions ───────────────────────────────────────────────

def _security_no_hardcoded_secrets() -> Callable:
    """Return a check that flags hardcoded secrets (negative check)."""

    # Patterns that likely indicate hardcoded secrets
    SECRET_PATTERNS = [
        r'(?:api_key|apikey|secret|token|password)\s*=\s*["\'][^"\']{8,}["\']',
        r'(?:sk-|pk-|ghp_|gho_|xox[bpas]-)[a-zA-Z0-9]{16,}',
    ]

    def check(project_path: str) -> CheckResult:
        py_files = get_python_files(project_path)
        # Also check .env files but NOT .env.example
        env_files = [
            f for f in list_files(project_path)
            if os.path.basename(f) == ".env" and not f.endswith(".example")
        ]
        all_files = py_files + env_files

        for fpath in all_files:
            content = read_file(fpath)
            if content is None:
                continue
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    rel = os.path.relpath(fpath, project_path)
                    return CheckResult(
                        False,
                        f"Potential hardcoded secret found in {rel}",
                        suggestion="Move secrets to environment variables. Use .env for local dev.",
                    )
        return CheckResult(
            True,
            "No hardcoded secrets detected",
        )

    return check
