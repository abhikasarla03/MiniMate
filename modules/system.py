"""
system.py
=========

Command interpreter that maps textual commands typed in the GUI
to actions in the other modules.
"""

from __future__ import annotations

from typing import Callable, Dict

from . import apps, monitor, utilities


CommandResult = str  # human-readable status returned to the console


def _cmd_cpu() -> str:
    return f"CPU usage: {monitor.cpu_percent():.1f}%"


def _cmd_ram() -> str:
    r = monitor.ram_info()
    return f"RAM: {r['used_gb']:.2f} / {r['total_gb']:.2f} GB ({r['percent']:.1f}%)"


def _cmd_disk() -> str:
    d = monitor.disk_info("/")
    return f"Disk /: {d['used_gb']:.1f} / {d['total_gb']:.1f} GB ({d['percent']:.1f}%)"


def _cmd_battery() -> str:
    return f"Battery: {monitor.battery_status()}"


# Static (no-argument) commands
STATIC_COMMANDS: Dict[str, Callable[[], CommandResult]] = {
    "open chrome":     lambda: f"Opening Chrome... ({apps.open_chrome()})",
    "open firefox":    lambda: f"Opening Firefox... ({apps.open_firefox()})",
    "open terminal":   lambda: f"Opening Terminal... ({apps.open_terminal()})",
    "open files":      lambda: f"Opening File Manager... ({apps.open_file_manager()})",
    "open calculator": lambda: f"Opening Calculator... ({apps.open_calculator()})",
    "open vscode":     lambda: f"Opening VS Code... ({apps.open_vscode()})",
    "open settings":   lambda: f"Opening Settings... ({apps.open_settings()})",
    "open downloads":  utilities.open_downloads,
    "open documents":  utilities.open_documents,
    "open home":       utilities.open_home,
    "lock":            utilities.lock_screen,
    "shutdown":        utilities.shutdown_system,
    "restart":         utilities.restart_system,
    "screenshot":      utilities.take_screenshot,
    "trash":           utilities.empty_trash,
    "cpu":             _cmd_cpu,
    "ram":             _cmd_ram,
    "memory":          _cmd_ram,
    "disk":            _cmd_disk,
    "battery":         _cmd_battery,
    "sysinfo":         monitor.system_summary,
    "help":            lambda: HELP_TEXT,
}


HELP_TEXT = (
    "Available commands:\n"
    "  open chrome | firefox | terminal | files | calculator | vscode | settings\n"
    "  open downloads | documents | home\n"
    "  lock | shutdown | restart | screenshot | trash\n"
    "  cpu | ram | disk | battery | sysinfo\n"
    "  google <query>\n"
    "  clear  (clears the console)"
)


def run_command(command: str) -> CommandResult:
    """Interpret and execute a single command. Returns a status string.

    Raises RuntimeError for unknown commands or action failures.
    The special command "clear" is handled by the GUI; this function
    still returns a sentinel string so the caller can detect it.
    """
    raw = (command or "").strip()
    if not raw:
        raise RuntimeError("Empty command.")

    lower = raw.lower()

    if lower == "clear":
        return "__CLEAR__"

    if lower.startswith("google"):
        query = raw[len("google"):].strip(" :")
        return utilities.google_search(query)

    if lower in STATIC_COMMANDS:
        return STATIC_COMMANDS[lower]()

    raise RuntimeError(f"Unknown command: '{raw}'. Type 'help' for options.")
