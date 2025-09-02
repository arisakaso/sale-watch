from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from dotenv import load_dotenv


def _find_upwards(filename: str, start: Path | None = None) -> Path | None:
    """Search for a file upwards from start (or this file) and return the path if found."""
    p = (start or Path(__file__).resolve()).parent
    while True:
        candidate = p / filename
        if candidate.exists():
            return candidate
        if p.parent == p:
            return None
        p = p.parent


def load_env_local(filenames: Iterable[str] = (".env.local", ".env")) -> None:
    """Load environment variables from .env.local / .env if found up the directory tree.

    Existing environment variables are not overridden.
    """
    for name in filenames:
        path = _find_upwards(name)
        if path:
            # Do not override already-set env vars (e.g. CI secrets)
            load_dotenv(dotenv_path=path, override=False)
