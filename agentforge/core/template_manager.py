"""
Template management for AgentForge-CLI.

Provides functionality to list, inspect, and retrieve metadata about
available project templates.
"""

import os
from typing import Dict, List, Optional

from agentforge.utils.console import bold, cyan, print_table


# ── Template metadata ─────────────────────────────────────────────────────

TEMPLATE_REGISTRY: Dict[str, Dict[str, str]] = {
    "minimal": {
        "name": "minimal",
        "display_name": "Minimal Agent",
        "description": "A lightweight AI agent with config, tools, and basic structure. "
                       "Perfect for getting started quickly or building simple agents.",
        "files": "agent.py, config.py, tools.py, requirements.txt, README.md, .env.example",
        "use_case": "Simple chatbots, single-task agents, prototyping",
    },
    "full": {
        "name": "full",
        "display_name": "Full-Featured Agent",
        "description": "A complete AI agent with memory management, prompt templates, "
                       "unit tests, and all best practices baked in.",
        "files": "agent.py, config.py, tools.py, memory.py, prompts.py, "
                 "requirements.txt, README.md, .env.example, tests/",
        "use_case": "Production agents, complex workflows, multi-tool agents",
    },
    "mcp": {
        "name": "mcp",
        "display_name": "MCP-Compatible Agent",
        "description": "An MCP (Model Context Protocol) compatible server that exposes "
                       "tools via the standardized MCP interface.",
        "files": "server.py, tools.py, config.py, requirements.txt, README.md, .env.example",
        "use_case": "MCP tool servers, IDE integrations, standardized tool exposure",
    },
}


def get_template_names() -> List[str]:
    """Return a list of all available template names."""
    return list(TEMPLATE_REGISTRY.keys())


def get_template_info(template_name: str) -> Optional[Dict[str, str]]:
    """
    Return metadata for a specific template.

    Returns None if the template name is not recognized.
    """
    return TEMPLATE_REGISTRY.get(template_name)


def list_templates() -> List[Dict[str, str]]:
    """Return metadata for all available templates."""
    return list(TEMPLATE_REGISTRY.values())


def print_template_list() -> None:
    """Print a formatted table of all available templates."""
    print()
    print(bold("Available Templates:"))
    print()

    headers = ["Name", "Description", "Use Case"]
    rows = []
    for tpl in list_templates():
        rows.append([
            cyan(tpl["name"]),
            tpl["description"],
            tpl["use_case"],
        ])

    print_table(headers, rows)
    print()


def print_template_info(template_name: str) -> bool:
    """
    Print detailed information about a specific template.

    Returns True if the template was found, False otherwise.
    """
    info = get_template_info(template_name)
    if info is None:
        return False

    print()
    print(bold(f"Template: {cyan(info['display_name'])}"))
    print()
    print(f"  {bold('Name:')}        {info['name']}")
    print(f"  {bold('Description:')} {info['description']}")
    print(f"  {bold('Files:')}       {info['files']}")
    print(f"  {bold('Use Case:')}    {info['use_case']}")
    print()

    return True
