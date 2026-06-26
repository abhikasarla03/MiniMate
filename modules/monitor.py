"""
monitor.py
==========

System monitoring helpers powered by psutil. Each function returns
plain Python types so the GUI layer never has to know about psutil.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None  # type: ignore


def _require_psutil() -> None:
    if psutil is None:
        raise RuntimeError(
            "psutil is not installed. Run: pip install -r requirements.txt"
        )


def cpu_percent() -> float:
    """Return current CPU utilization as a percentage (0-100)."""
    _require_psutil()
    return float(psutil.cpu_percent(interval=None))


def ram_info() -> dict:
    """Return RAM usage information in GB and percent."""
    _require_psutil()
    vm = psutil.virtual_memory()
    return {
        "total_gb": round(vm.total / (1024 ** 3), 2),
        "used_gb":  round(vm.used  / (1024 ** 3), 2),
        "percent":  float(vm.percent),
    }


def disk_info(path: str = "/") -> dict:
    """Return disk usage for the given mount point."""
    _require_psutil()
    du = psutil.disk_usage(path)
    return {
        "total_gb": round(du.total / (1024 ** 3), 2),
        "used_gb":  round(du.used  / (1024 ** 3), 2),
        "percent":  float(du.percent),
    }


def battery_percent() -> Optional[float]:
    """Return battery percentage, or None when no battery is present."""
    _require_psutil()
    batt = psutil.sensors_battery()
    if batt is None:
        return None
    return float(batt.percent)


def battery_status() -> str:
    """Return a human-readable battery summary."""
    _require_psutil()
    batt = psutil.sensors_battery()
    if batt is None:
        return "No battery detected (desktop system)"
    plugged = "Charging" if batt.power_plugged else "On battery"
    return f"{batt.percent:.0f}% — {plugged}"


def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def current_date() -> str:
    return datetime.now().strftime("%A, %d %B %Y")


def system_summary() -> str:
    """Return a multi-line string describing the host system."""
    _require_psutil()
    import platform
    uname = platform.uname()
    boot = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, _ = divmod(rem, 60)
    return (
        f"System:    {uname.system} {uname.release}\n"
        f"Node:      {uname.node}\n"
        f"Machine:   {uname.machine}\n"
        f"Processor: {uname.processor or 'n/a'}\n"
        f"CPU cores: {psutil.cpu_count(logical=False)} physical / "
        f"{psutil.cpu_count(logical=True)} logical\n"
        f"Uptime:    {hours}h {minutes}m"
    )
