"""
Colorful console output utilities using ANSI escape codes.

Provides styled text output, progress indicators, table formatting,
and convenience functions for success/error/warning/info messages.

Zero external dependencies -- only uses Python standard library.
"""

import os
import sys
import textwrap
import time
from typing import List, Optional


# ── ANSI color codes ──────────────────────────────────────────────────────

class _Colors:
    """ANSI escape code constants for terminal colors and styles."""

    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"


# Detect whether the terminal supports color output.
# Respect NO_COLOR environment variable (https://no-color.org/).
_SUPPORTS_COLOR = (
    hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    and os.environ.get("NO_COLOR", "") == ""
    and os.environ.get("TERM", "") != "dumb"
)


def _colorize(text: str, code: str) -> str:
    """Wrap *text* in an ANSI escape code if the terminal supports it."""
    if _SUPPORTS_COLOR:
        return f"{code}{text}{_Colors.RESET}"
    return text


# ── Public style helpers ──────────────────────────────────────────────────

def bold(text: str) -> str:
    return _colorize(text, _Colors.BOLD)

def red(text: str) -> str:
    return _colorize(text, _Colors.RED)

def green(text: str) -> str:
    return _colorize(text, _Colors.GREEN)

def yellow(text: str) -> str:
    return _colorize(text, _Colors.YELLOW)

def blue(text: str) -> str:
    return _colorize(text, _Colors.BLUE)

def magenta(text: str) -> str:
    return _colorize(text, _Colors.MAGENTA)

def cyan(text: str) -> str:
    return _colorize(text, _Colors.CYAN)

def dim(text: str) -> str:
    return _colorize(text, _Colors.DIM)


# ── Convenience print functions ───────────────────────────────────────────

def success(msg: str) -> None:
    """Print a success message with a green checkmark."""
    print(f"  {green('[OK]')} {msg}")


def error(msg: str) -> None:
    """Print an error message with a red cross."""
    print(f"  {red('[FAIL]')} {msg}")


def warning(msg: str) -> None:
    """Print a warning message with a yellow exclamation."""
    print(f"  {yellow('[WARN]')} {msg}")


def info(msg: str) -> None:
    """Print an informational message with a blue info marker."""
    print(f"  {blue('[INFO]')} {msg}")


# ── Table formatting ──────────────────────────────────────────────────────

def print_table(
    headers: List[str],
    rows: List[List[str]],
    padding: int = 2,
) -> None:
    """
    Print a simple aligned table to stdout.

    Parameters
    ----------
    headers : List[str]
        Column header strings.
    rows : List[List[str]]
        Each inner list is a row of string cell values.
    padding : int
        Number of spaces between columns (default 2).
    """
    # Strip ANSI codes to compute real column widths
    def visible_len(s: str) -> int:
        import re
        return len(re.sub(r"\033\[[0-9;]*m", "", s))

    # Determine column widths
    col_widths = [visible_len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], visible_len(str(cell)))

    sep = " " * padding

    # Header row
    header_line = sep.join(
        h.ljust(col_widths[i]) for i, h in enumerate(headers)
    )
    print(bold(header_line))

    # Separator
    separator = sep.join("-" * col_widths[i] for i in range(len(headers)))
    print(dim(separator))

    # Data rows
    for row in rows:
        line = sep.join(
            str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
        )
        print(line)


# ── Progress indicator ────────────────────────────────────────────────────

class Spinner:
    """A lightweight, non-blocking spinner for long-running operations."""

    _FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str = "Working..."):
        self._message = message
        self._running = False
        self._step = 0

    def __enter__(self) -> "Spinner":
        self._running = True
        self._tick()
        return self

    def __exit__(self, *args) -> None:
        self._running = False
        # Clear the spinner line
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

    def _tick(self) -> None:
        if not self._running:
            return
        frame = self._FRAMES[self._step % len(self._FRAMES)]
        sys.stdout.write(f"\r  {cyan(frame)} {self._message}")
        sys.stdout.flush()
        self._step += 1
        # Schedule next frame (non-blocking, ~80ms interval)
        if self._running:
            threading = __import__("threading")
            threading.Timer(0.08, self._tick).start()

    def update(self, message: str) -> None:
        """Update the spinner message text."""
        self._message = message


# ── Section headers ───────────────────────────────────────────────────────

def print_header(title: str) -> None:
    """Print a prominent section header."""
    width = 60
    print()
    print(bold("=" * width))
    print(bold(f"  {title}"))
    print(bold("=" * width))
    print()


def print_subheader(title: str) -> None:
    """Print a minor section header."""
    print()
    print(bold(f"--- {title} ---"))
    print()
