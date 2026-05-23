"""
File operation utilities for AgentForge-CLI.

Provides safe file reading, writing, directory creation, and project
file discovery helpers. Uses only the Python standard library.
"""

import os
import shutil
import stat
from typing import List, Optional


def ensure_directory(path: str) -> None:
    """Create directory (and parents) if it does not already exist."""
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str) -> None:
    """
    Write *content* to *path*, creating parent directories as needed.

    Overwrites existing files. Uses UTF-8 encoding.
    """
    ensure_directory(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def read_file(path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    Read the entire contents of *path*.

    Returns None if the file does not exist or cannot be read.
    """
    try:
        with open(path, "r", encoding=encoding) as fh:
            return fh.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError):
        return None


def list_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """
    Recursively list files under *directory*.

    Parameters
    ----------
    directory : str
        Root directory to search.
    extensions : list of str, optional
        If provided, only return files ending with one of these suffixes
        (e.g. [".py", ".txt"]).

    Returns
    -------
    list of str
        Absolute file paths.
    """
    result: List[str] = []
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            if extensions is None or any(fname.endswith(ext) for ext in extensions):
                result.append(os.path.join(root, fname))
    return result


def find_project_root(path: str = ".") -> str:
    """
    Walk upward from *path* looking for common project markers.

    Recognised markers: setup.py, pyproject.toml, .git, requirements.txt.
    Returns the deepest directory containing a marker, or the current
    working directory if none is found.
    """
    current = os.path.abspath(path)
    markers = {"setup.py", "pyproject.toml", ".git", "requirements.txt"}

    while True:
        if any(os.path.exists(os.path.join(current, m)) for m in markers):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return current
        current = parent


def copy_tree(src: str, dst: str) -> None:
    """
    Recursively copy directory *src* to *dst*.

    Creates *dst* if it does not exist. Existing files in *dst* are
    overwritten.
    """
    if not os.path.exists(dst):
        shutil.copytree(src, dst)
    else:
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copy_tree(s, d)
            else:
                shutil.copy2(s, d)


def is_git_repo(path: str) -> bool:
    """Return True if *path* is inside a Git repository."""
    return os.path.exists(os.path.join(path, ".git"))


def has_file(path: str, filename: str) -> bool:
    """Return True if *filename* exists directly inside *path*."""
    return os.path.isfile(os.path.join(path, filename))


def get_python_files(directory: str) -> List[str]:
    """Return a list of all .py files under *directory*."""
    return list_files(directory, extensions=[".py"])
