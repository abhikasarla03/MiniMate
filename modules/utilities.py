"""
utilities.py
============

Desktop utility helpers: lock, shutdown, restart, screenshots,
folder shortcuts, web searches, etc.

All functions return a short status string for the output console
and raise RuntimeError on failure.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import urllib.parse
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Iterable


# --------------------------------------------------------------------------- #
# internal helpers
# --------------------------------------------------------------------------- #

def _run(candidates: Iterable[str], friendly: str) -> str:
    for cmd in candidates:
        parts = cmd.split()
        if shutil.which(parts[0]):
            subprocess.Popen(
                parts,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return parts[0]
    raise RuntimeError(f"No supported command found for: {friendly}")


def _open_path(path: Path) -> str:
    if not path.exists():
        raise RuntimeError(f"Path does not exist: {path}")
    if shutil.which("xdg-open"):
        subprocess.Popen(
            ["xdg-open", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return str(path)
    raise RuntimeError("xdg-open is not available on this system.")


# --------------------------------------------------------------------------- #
# power / session
# --------------------------------------------------------------------------- #

def lock_screen() -> str:
    _run(
        ["cinnamon-screensaver-command --lock",
         "gnome-screensaver-command --lock",
         "xdg-screensaver lock",
         "loginctl lock-session"],
        "lock screen",
    )
    return "Screen locked"


def shutdown_system() -> str:
    _run(["systemctl poweroff", "shutdown -h now"], "shutdown")
    return "Shutdown signal sent"


def restart_system() -> str:
    _run(["systemctl reboot", "shutdown -r now"], "restart")
    return "Restart signal sent"


# --------------------------------------------------------------------------- #
# screenshots
# --------------------------------------------------------------------------- #

def take_screenshot() -> str:
    pictures = Path.home() / "Pictures"
    pictures.mkdir(parents=True, exist_ok=True)
    out = pictures / f"mintmate_{datetime.now():%Y%m%d_%H%M%S}.png"

    if shutil.which("gnome-screenshot"):
        subprocess.run(["gnome-screenshot", "-f", str(out)], check=False)
    elif shutil.which("scrot"):
        subprocess.run(["scrot", str(out)], check=False)
    elif shutil.which("import"):
        subprocess.run(["import", "-window", "root", str(out)], check=False)
    else:
        raise RuntimeError(
            "Install one of: gnome-screenshot, scrot, or imagemagick."
        )
    return f"Screenshot saved to {out}"


# --------------------------------------------------------------------------- #
# common folders
# --------------------------------------------------------------------------- #

def open_downloads() -> str:
    return f"Opened {_open_path(Path.home() / 'Downloads')}"


def open_documents() -> str:
    return f"Opened {_open_path(Path.home() / 'Documents')}"


def open_home() -> str:
    return f"Opened {_open_path(Path.home())}"


# --------------------------------------------------------------------------- #
# trash / web
# --------------------------------------------------------------------------- #

def empty_trash() -> str:
    if shutil.which("trash-empty"):
        subprocess.Popen(["trash-empty"], start_new_session=True)
        return "Trash emptied (trash-empty)"
    trash = Path.home() / ".local/share/Trash"
    files = trash / "files"
    info = trash / "info"
    removed = 0
    for folder in (files, info):
        if folder.exists():
            for entry in folder.iterdir():
                try:
                    if entry.is_dir() and not entry.is_symlink():
                        shutil.rmtree(entry)
                    else:
                        entry.unlink()
                    removed += 1
                except OSError:
                    pass
    return f"Trash emptied ({removed} item(s) removed)"


def google_search(query: str) -> str:
    query = (query or "").strip()
    if not query:
        raise RuntimeError("Search query is empty.")
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    webbrowser.open(url, new=2)
    return f"Searching Google for: {query}"
