"""
apps.py
=======

Launch external applications on Linux Mint (or any Linux desktop).

Each launcher tries a list of common executables and returns the
process. Launch failures raise RuntimeError with a helpful message
that the GUI surfaces in the output console.
"""

from __future__ import annotations

import shutil
import subprocess
from typing import Iterable


def _spawn(candidates: Iterable[str], friendly: str) -> str:
    """Try each candidate command until one is found on PATH."""
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
    raise RuntimeError(
        f"Could not launch {friendly}. None of these were found on PATH: "
        + ", ".join(c.split()[0] for c in candidates)
    )


def open_chrome() -> str:
    return _spawn(
        ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"],
        "Google Chrome",
    )


def open_firefox() -> str:
    return _spawn(["firefox"], "Firefox")


def open_terminal() -> str:
    return _spawn(
        ["gnome-terminal", "mate-terminal", "xfce4-terminal", "konsole",
         "tilix", "xterm"],
        "Terminal",
    )


def open_file_manager() -> str:
    return _spawn(
        ["nemo", "nautilus", "thunar", "dolphin", "pcmanfm", "caja"],
        "File Manager",
    )


def open_calculator() -> str:
    return _spawn(
        ["gnome-calculator", "mate-calc", "kcalc", "galculator", "qalculate-gtk"],
        "Calculator",
    )


def open_vscode() -> str:
    return _spawn(["code", "codium", "code-oss"], "VS Code")


def open_settings() -> str:
    return _spawn(
        ["cinnamon-settings", "gnome-control-center", "mate-control-center",
         "xfce4-settings-manager", "systemsettings5"],
        "System Settings",
    )


# Convenience registry used by the launcher grid.
LAUNCHERS = {
    "Google Chrome": open_chrome,
    "Firefox":       open_firefox,
    "Terminal":      open_terminal,
    "File Manager":  open_file_manager,
    "Calculator":    open_calculator,
    "VS Code":       open_vscode,
    "Settings":      open_settings,
}
