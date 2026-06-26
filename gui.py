"""
gui.py
======

CustomTkinter user interface for MintMate.

The UI is organised around a single MintMateApp window that hosts:
- a sidebar navigation,
- a header bar with the app title and live clock,
- a swappable content area (Dashboard, Applications, Monitor,
  Utilities, Settings, About),
- a command input box,
- an output console,
- a status bar.

The GUI layer never touches the OS directly; everything goes through
the modules/ package.
"""

from __future__ import annotations

from datetime import datetime
from tkinter import StringVar
from typing import Callable, Dict

import customtkinter as ctk

import config
from modules import apps, monitor, system, utilities


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def _card(parent, **kwargs) -> ctk.CTkFrame:
    """A rounded, bordered surface used throughout the UI."""
    return ctk.CTkFrame(
        parent,
        fg_color=config.COLORS["surface"],
        border_color=config.COLORS["border"],
        border_width=1,
        corner_radius=14,
        **kwargs,
    )


# =========================================================================== #
# Reusable widgets
# =========================================================================== #

class MetricCard(ctk.CTkFrame):
    """A dashboard card showing one large metric."""

    def __init__(self, master, title: str, icon: str = "•"):
        super().__init__(
            master,
            fg_color=config.COLORS["surface"],
            border_color=config.COLORS["border"],
            border_width=1,
            corner_radius=14,
        )
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 4))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text=title, font=config.FONTS["small"],
            text_color=config.COLORS["text_muted"], anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header, text=icon, font=(config.FONT_FAMILY, 16),
            text_color=config.COLORS["primary"],
        ).grid(row=0, column=1, sticky="e")

        self._value_var = StringVar(value="—")
        ctk.CTkLabel(
            self, textvariable=self._value_var,
            font=config.FONTS["metric"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=18)

        self._sub_var = StringVar(value="")
        ctk.CTkLabel(
            self, textvariable=self._sub_var,
            font=config.FONTS["small"],
            text_color=config.COLORS["text_muted"], anchor="w",
        ).grid(row=2, column=0, sticky="w", padx=18, pady=(2, 8))

        self._progress = ctk.CTkProgressBar(
            self, height=6, corner_radius=4,
            progress_color=config.COLORS["primary"],
            fg_color=config.COLORS["surface_alt"],
        )
        self._progress.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 16))
        self._progress.set(0)

    def update_metric(self, value: str, subtitle: str = "", progress: float | None = None) -> None:
        self._value_var.set(value)
        self._sub_var.set(subtitle)
        if progress is None:
            self._progress.grid_remove()
        else:
            self._progress.grid()
            self._progress.set(max(0.0, min(1.0, progress)))


class ActionButton(ctk.CTkButton):
    """A consistent, modern action button used in launcher / utilities grids."""

    def __init__(self, master, text: str, command: Callable[[], None],
                 icon: str = "•", danger: bool = False):
        fg = config.COLORS["danger"] if danger else config.COLORS["surface_hover"]
        hover = "#D14B4C" if danger else config.COLORS["border"]
        text_color = "white" if danger else config.COLORS["text"]

        super().__init__(
            master,
            text=f"  {icon}   {text}",
            command=command,
            anchor="w",
            height=44,
            corner_radius=10,
            fg_color=fg,
            hover_color=hover,
            text_color=text_color,
            font=config.FONTS["body"],
            border_width=0,
        )


# =========================================================================== #
# Pages
# =========================================================================== #

class BasePage(ctk.CTkScrollableFrame):
    """Shared scrollable container with consistent padding."""

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=config.COLORS["bg"],
            scrollbar_button_color=config.COLORS["border"],
            scrollbar_button_hover_color=config.COLORS["surface_hover"],
        )
        self.grid_columnconfigure(0, weight=1)


# ---------- Dashboard ------------------------------------------------------- #

class DashboardPage(BasePage):
    def __init__(self, master, app: "MintMateApp"):
        super().__init__(master)
        self.app = app

        # Welcome card
        welcome = _card(self)
        welcome.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 16))
        welcome.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            welcome, text=f"Welcome back 👋",
            font=config.FONTS["title"], text_color=config.COLORS["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            welcome,
            text="Here's a live snapshot of your system. Use the sidebar or type "
                 "a command below to get things done.",
            font=config.FONTS["body"], text_color=config.COLORS["text_muted"],
            anchor="w", justify="left", wraplength=900,
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 18))

        # Metric grid
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="nsew", padx=4)
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1, uniform="metric")

        self.card_cpu     = MetricCard(grid, "CPU Usage",   "◉")
        self.card_ram     = MetricCard(grid, "Memory",      "▣")
        self.card_disk    = MetricCard(grid, "Disk (/)",    "◈")
        self.card_battery = MetricCard(grid, "Battery",     "⚡")
        self.card_time    = MetricCard(grid, "Time",        "◷")
        self.card_date    = MetricCard(grid, "Date",        "◫")

        cards = [
            self.card_cpu, self.card_ram, self.card_disk,
            self.card_battery, self.card_time, self.card_date,
        ]
        for i, card in enumerate(cards):
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=8, pady=8)

        # Quick actions
        actions = _card(self)
        actions.grid(row=2, column=0, sticky="ew", padx=4, pady=(16, 8))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            actions, text="Quick Actions", font=config.FONTS["header"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 8))

        action_grid = ctk.CTkFrame(actions, fg_color="transparent")
        action_grid.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 16))
        for c in range(4):
            action_grid.grid_columnconfigure(c, weight=1, uniform="qa")

        quick = [
            ("Chrome",     "🌐", lambda: app.safe_run("Opening Chrome", apps.open_chrome)),
            ("Terminal",   "▶_", lambda: app.safe_run("Opening Terminal", apps.open_terminal)),
            ("Files",      "🗂", lambda: app.safe_run("Opening File Manager", apps.open_file_manager)),
            ("Screenshot", "▣",  lambda: app.safe_run("Taking screenshot", utilities.take_screenshot)),
            ("Lock",       "🔒", lambda: app.safe_run("Locking screen", utilities.lock_screen)),
            ("VS Code",    "</>",lambda: app.safe_run("Opening VS Code", apps.open_vscode)),
            ("Home",       "🏠", lambda: app.safe_run("Opening Home", utilities.open_home)),
            ("Sysinfo",    "ⓘ", lambda: app.log(monitor.system_summary())),
        ]
        for i, (label, icon, cmd) in enumerate(quick):
            ActionButton(action_grid, label, cmd, icon=icon).grid(
                row=i // 4, column=i % 4, padx=6, pady=6, sticky="ew"
            )

    def refresh(self) -> None:
        # CPU
        cpu = monitor.cpu_percent()
        self.card_cpu.update_metric(f"{cpu:.0f}%", "Real-time utilization", cpu / 100)

        # RAM
        ram = monitor.ram_info()
        self.card_ram.update_metric(
            f"{ram['percent']:.0f}%",
            f"{ram['used_gb']:.1f} / {ram['total_gb']:.1f} GB",
            ram["percent"] / 100,
        )

        # Disk
        disk = monitor.disk_info("/")
        self.card_disk.update_metric(
            f"{disk['percent']:.0f}%",
            f"{disk['used_gb']:.0f} / {disk['total_gb']:.0f} GB",
            disk["percent"] / 100,
        )

        # Battery
        pct = monitor.battery_percent()
        if pct is None:
            self.card_battery.update_metric("N/A", "No battery detected", None)
        else:
            self.card_battery.update_metric(
                f"{pct:.0f}%", monitor.battery_status(), pct / 100
            )

        # Time / Date
        self.card_time.update_metric(monitor.current_time(), "Local time", None)
        self.card_date.update_metric(
            datetime.now().strftime("%d %b"), monitor.current_date(), None
        )


# ---------- Applications ---------------------------------------------------- #

class AppsPage(BasePage):
    def __init__(self, master, app: "MintMateApp"):
        super().__init__(master)

        header = _card(self)
        header.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 16))
        ctk.CTkLabel(
            header, text="Application Launcher",
            font=config.FONTS["title"], text_color=config.COLORS["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(
            header,
            text="One-click launchers for the apps you use the most.",
            font=config.FONTS["body"], text_color=config.COLORS["text_muted"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

        grid = _card(self)
        grid.grid(row=1, column=0, sticky="ew", padx=4)
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1, uniform="apps")

        icons = {
            "Google Chrome": "🌐", "Firefox": "🦊", "Terminal": "▶_",
            "File Manager": "🗂", "Calculator": "🧮", "VS Code": "</>",
            "Settings": "⚙",
        }
        for i, (name, fn) in enumerate(apps.LAUNCHERS.items()):
            ActionButton(
                grid, name,
                command=lambda n=name, f=fn: app.safe_run(f"Opening {n}", f),
                icon=icons.get(name, "•"),
            ).grid(row=i // 3, column=i % 3, padx=12, pady=12, sticky="ew")


# ---------- System Monitor -------------------------------------------------- #

class MonitorPage(BasePage):
    def __init__(self, master, app: "MintMateApp"):
        super().__init__(master)
        self.app = app

        header = _card(self)
        header.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 16))
        ctk.CTkLabel(
            header, text="System Monitor",
            font=config.FONTS["title"], text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(
            header,
            text="Live CPU, memory, and storage metrics with progress bars.",
            font=config.FONTS["body"], text_color=config.COLORS["text_muted"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

        bars = _card(self)
        bars.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 16))
        bars.grid_columnconfigure(1, weight=1)

        self._rows: Dict[str, tuple] = {}
        for i, label in enumerate(["CPU", "Memory", "Disk", "Battery"]):
            ctk.CTkLabel(
                bars, text=label, font=config.FONTS["body"],
                text_color=config.COLORS["text"], anchor="w", width=80,
            ).grid(row=i, column=0, sticky="w", padx=20, pady=10)

            bar = ctk.CTkProgressBar(
                bars, height=10, corner_radius=6,
                progress_color=config.COLORS["primary"],
                fg_color=config.COLORS["surface_alt"],
            )
            bar.set(0)
            bar.grid(row=i, column=1, sticky="ew", padx=10, pady=10)

            val = ctk.CTkLabel(
                bars, text="—", font=config.FONTS["body"],
                text_color=config.COLORS["text_muted"], width=120, anchor="e",
            )
            val.grid(row=i, column=2, sticky="e", padx=20, pady=10)

            self._rows[label] = (bar, val)

        info = _card(self)
        info.grid(row=2, column=0, sticky="ew", padx=4)
        ctk.CTkLabel(
            info, text="System Information", font=config.FONTS["header"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 6))

        self._info_label = ctk.CTkLabel(
            info, text="Loading…", font=config.FONTS["mono"],
            text_color=config.COLORS["text_muted"], justify="left", anchor="w",
        )
        self._info_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

    def refresh(self) -> None:
        cpu = monitor.cpu_percent()
        ram = monitor.ram_info()
        disk = monitor.disk_info("/")
        bat = monitor.battery_percent()

        bar, val = self._rows["CPU"];     bar.set(cpu / 100);          val.configure(text=f"{cpu:.1f}%")
        bar, val = self._rows["Memory"];  bar.set(ram["percent"] / 100); val.configure(text=f"{ram['used_gb']:.1f} / {ram['total_gb']:.1f} GB")
        bar, val = self._rows["Disk"];    bar.set(disk["percent"] / 100); val.configure(text=f"{disk['used_gb']:.0f} / {disk['total_gb']:.0f} GB")
        bar, val = self._rows["Battery"]
        if bat is None:
            bar.set(0); val.configure(text="N/A")
        else:
            bar.set(bat / 100); val.configure(text=f"{bat:.0f}%")

        try:
            self._info_label.configure(text=monitor.system_summary())
        except RuntimeError as exc:
            self._info_label.configure(text=str(exc))


# ---------- Utilities ------------------------------------------------------- #

class UtilitiesPage(BasePage):
    def __init__(self, master, app: "MintMateApp"):
        super().__init__(master)

        header = _card(self)
        header.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 16))
        ctk.CTkLabel(
            header, text="Desktop Utilities",
            font=config.FONTS["title"], text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(
            header,
            text="System actions and shortcuts. Power options are highlighted.",
            font=config.FONTS["body"], text_color=config.COLORS["text_muted"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

        # Folder + screenshot shortcuts
        grid = _card(self)
        grid.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 16))
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1, uniform="util")

        actions = [
            ("Take Screenshot", "▣",  lambda: app.safe_run("Taking screenshot", utilities.take_screenshot), False),
            ("Open Downloads",  "⬇",  lambda: app.safe_run("Opening Downloads", utilities.open_downloads), False),
            ("Open Documents",  "📄", lambda: app.safe_run("Opening Documents", utilities.open_documents), False),
            ("Open Home",       "🏠", lambda: app.safe_run("Opening Home",      utilities.open_home), False),
            ("Empty Trash",     "🗑", lambda: app.safe_run("Emptying trash",    utilities.empty_trash), False),
            ("System Info",     "ⓘ", lambda: app.log(monitor.system_summary()), False),
        ]
        for i, (label, icon, cmd, danger) in enumerate(actions):
            ActionButton(grid, label, cmd, icon=icon, danger=danger).grid(
                row=i // 3, column=i % 3, padx=12, pady=12, sticky="ew"
            )

        # Search card
        search = _card(self)
        search.grid(row=2, column=0, sticky="ew", padx=4, pady=(0, 16))
        search.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            search, text="Search Google", font=config.FONTS["header"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 6))

        row = ctk.CTkFrame(search, fg_color="transparent")
        row.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))
        row.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            row, placeholder_text="Type a query and press Enter…",
            height=40, corner_radius=10,
            fg_color=config.COLORS["surface_alt"],
            border_color=config.COLORS["border"],
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda _e: self._do_search(app))

        ctk.CTkButton(
            row, text="Search", height=40, corner_radius=10,
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            text_color="#0B0F17", font=config.FONTS["body"],
            command=lambda: self._do_search(app),
        ).grid(row=0, column=1)

        # Power card
        power = _card(self)
        power.grid(row=3, column=0, sticky="ew", padx=4)
        for c in range(3):
            power.grid_columnconfigure(c, weight=1, uniform="pwr")
        ctk.CTkLabel(
            power, text="Power", font=config.FONTS["header"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(16, 6))

        power_actions = [
            ("Lock Screen", "🔒", lambda: app.safe_run("Locking screen", utilities.lock_screen), False),
            ("Restart",     "↻",  lambda: app.safe_run("Restarting system", utilities.restart_system), True),
            ("Shutdown",    "⏻",  lambda: app.safe_run("Shutting down", utilities.shutdown_system), True),
        ]
        for i, (label, icon, cmd, danger) in enumerate(power_actions):
            ActionButton(power, label, cmd, icon=icon, danger=danger).grid(
                row=1, column=i, padx=12, pady=(0, 16), sticky="ew"
            )

    def _do_search(self, app: "MintMateApp") -> None:
        query = self.search_entry.get()
        app.safe_run(f"Google search: {query}", lambda: utilities.google_search(query))
        self.search_entry.delete(0, "end")


# ---------- Settings -------------------------------------------------------- #

class SettingsPage(BasePage):
    def __init__(self, master, app: "MintMateApp"):
        super().__init__(master)

        card = _card(self)
        card.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card, text="Settings", font=config.FONTS["title"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(16, 12))

        # Appearance
        ctk.CTkLabel(
            card, text="Appearance mode", font=config.FONTS["body"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        mode = ctk.CTkOptionMenu(
            card, values=["dark", "light", "system"],
            command=ctk.set_appearance_mode,
            fg_color=config.COLORS["surface_hover"],
            button_color=config.COLORS["primary"],
            button_hover_color=config.COLORS["primary_hover"],
        )
        mode.set(config.APPEARANCE_MODE)
        mode.grid(row=1, column=1, sticky="w", padx=20, pady=10)

        # UI scaling
        ctk.CTkLabel(
            card, text="Interface scaling", font=config.FONTS["body"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        scale = ctk.CTkOptionMenu(
            card, values=["80%", "90%", "100%", "110%", "120%"],
            command=lambda v: ctk.set_widget_scaling(int(v.rstrip('%')) / 100),
            fg_color=config.COLORS["surface_hover"],
            button_color=config.COLORS["primary"],
            button_hover_color=config.COLORS["primary_hover"],
        )
        scale.set("100%")
        scale.grid(row=2, column=1, sticky="w", padx=20, pady=10)

        # Refresh rate (informational)
        ctk.CTkLabel(
            card,
            text=f"Live stats refresh every {config.REFRESH_INTERVAL_MS} ms "
                 "(edit config.py to change).",
            font=config.FONTS["small"],
            text_color=config.COLORS["text_muted"], anchor="w",
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 16))


# ---------- About ----------------------------------------------------------- #

class AboutPage(BasePage):
    def __init__(self, master, app: "MintMateApp"):
        super().__init__(master)
        card = _card(self)
        card.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=f"{config.APP_NAME}",
            font=(config.FONT_FAMILY, 34, "bold"),
            text_color=config.COLORS["primary"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 2))

        ctk.CTkLabel(
            card, text=config.APP_TAGLINE, font=config.FONTS["header"],
            text_color=config.COLORS["text"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        about_text = (
            f"Version {config.APP_VERSION}\n\n"
            "MintMate is a modern productivity assistant for Linux Mint that\n"
            "combines a polished CustomTkinter interface with real system\n"
            "monitoring, application launching, and desktop utilities.\n\n"
            "Built with Python, CustomTkinter, and psutil.\n"
            "Architected for future expansion: voice commands, text-to-speech,\n"
            "AI chatbot integration, plugins, theming, notifications, and\n"
            "global keyboard shortcuts."
        )
        ctk.CTkLabel(
            card, text=about_text, font=config.FONTS["body"],
            text_color=config.COLORS["text_muted"], anchor="w", justify="left",
        ).grid(row=2, column=0, sticky="w", padx=24, pady=(0, 24))


# =========================================================================== #
# Main application window
# =========================================================================== #

class MintMateApp(ctk.CTk):
    """Top-level CustomTkinter window for MintMate."""

    def __init__(self) -> None:
        ctk.set_appearance_mode(config.APPEARANCE_MODE)
        ctk.set_default_color_theme(config.COLOR_THEME)
        super().__init__(fg_color=config.COLORS["bg"])

        self.title(f"{config.APP_NAME} — {config.APP_TAGLINE}")
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.minsize(config.MIN_WIDTH, config.MIN_HEIGHT)

        # 2-column layout: sidebar | main
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()

        # Pages
        self.pages: Dict[str, BasePage] = {
            "dashboard": DashboardPage(self.page_holder, self),
            "apps":      AppsPage(self.page_holder, self),
            "monitor":   MonitorPage(self.page_holder, self),
            "utilities": UtilitiesPage(self.page_holder, self),
            "settings":  SettingsPage(self.page_holder, self),
            "about":     AboutPage(self.page_holder, self),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        self.current_page_id = "dashboard"
        self._show("dashboard")

        self.log(f"{config.APP_NAME} v{config.APP_VERSION} started.")
        self.log("Type 'help' in the command box for a list of commands.")

        # Start the live-refresh loop
        self.after(200, self._tick)

    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #

    def _build_sidebar(self) -> None:
        sb = ctk.CTkFrame(
            self, width=240, corner_radius=0,
            fg_color=config.COLORS["sidebar"],
        )
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)

        # Logo
        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.grid(row=0, column=0, sticky="ew", padx=20, pady=(22, 18))
        logo.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            logo, text="◆", font=(config.FONT_FAMILY, 28, "bold"),
            text_color=config.COLORS["primary"],
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            logo, text=config.APP_NAME,
            font=(config.FONT_FAMILY, 20, "bold"),
            text_color=config.COLORS["text"],
        ).grid(row=0, column=1, sticky="w", padx=(10, 0))

        ctk.CTkFrame(sb, height=1, fg_color=config.COLORS["border"]).grid(
            row=1, column=0, sticky="ew", padx=16, pady=(0, 10)
        )

        # Nav buttons
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        for i, (key, label, glyph) in enumerate(config.NAV_ITEMS):
            btn = ctk.CTkButton(
                sb,
                text=f"  {glyph}    {label}",
                anchor="w",
                height=42,
                corner_radius=10,
                fg_color="transparent",
                hover_color=config.COLORS["surface_hover"],
                text_color=config.COLORS["text_muted"],
                font=config.FONTS["body"],
                command=lambda k=key: self._show(k),
            )
            btn.grid(row=2 + i, column=0, sticky="ew", padx=12, pady=3)
            self.nav_buttons[key] = btn

        # Footer
        footer = ctk.CTkLabel(
            sb, text=f"v{config.APP_VERSION}",
            font=config.FONTS["caption"],
            text_color=config.COLORS["text_muted"],
        )
        footer.grid(row=99, column=0, sticky="s", pady=14)
        sb.grid_rowconfigure(98, weight=1)

    def _build_main(self) -> None:
        main = ctk.CTkFrame(self, fg_color=config.COLORS["bg"], corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)   # page area
        main.grid_rowconfigure(3, weight=0)   # console

        # Header
        header = ctk.CTkFrame(
            main, fg_color=config.COLORS["sidebar"],
            corner_radius=0, height=64,
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_propagate(False)

        self.header_title = ctk.CTkLabel(
            header, text="Dashboard",
            font=(config.FONT_FAMILY, 18, "bold"),
            text_color=config.COLORS["text"], anchor="w",
        )
        self.header_title.grid(row=0, column=0, sticky="w", padx=24, pady=18)

        self.header_clock = ctk.CTkLabel(
            header, text="",
            font=config.FONTS["body"],
            text_color=config.COLORS["text_muted"], anchor="e",
        )
        self.header_clock.grid(row=0, column=1, sticky="e", padx=24, pady=18)

        # Page holder
        self.page_holder = ctk.CTkFrame(main, fg_color=config.COLORS["bg"])
        self.page_holder.grid(row=1, column=0, sticky="nsew", padx=20, pady=16)
        self.page_holder.grid_columnconfigure(0, weight=1)
        self.page_holder.grid_rowconfigure(0, weight=1)

        # Command bar
        cmd_card = _card(main)
        cmd_card.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 8))
        cmd_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            cmd_card, text="❯", font=(config.FONT_MONO, 16, "bold"),
            text_color=config.COLORS["primary"],
        ).grid(row=0, column=0, padx=(16, 6), pady=10)

        self.command_entry = ctk.CTkEntry(
            cmd_card,
            placeholder_text="Type a command (e.g. open chrome, cpu, google python)…",
            height=38, corner_radius=8,
            fg_color=config.COLORS["surface_alt"],
            border_color=config.COLORS["border"],
            font=config.FONTS["mono"],
        )
        self.command_entry.grid(row=0, column=1, sticky="ew", padx=(2, 8), pady=10)
        self.command_entry.bind("<Return>", lambda _e: self._on_command())

        ctk.CTkButton(
            cmd_card, text="Run", width=80, height=38, corner_radius=8,
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            text_color="#0B0F17", font=config.FONTS["body"],
            command=self._on_command,
        ).grid(row=0, column=2, padx=(0, 8), pady=10)

        ctk.CTkButton(
            cmd_card, text="Clear", width=80, height=38, corner_radius=8,
            fg_color=config.COLORS["surface_hover"],
            hover_color=config.COLORS["border"],
            text_color=config.COLORS["text"], font=config.FONTS["body"],
            command=self.clear_console,
        ).grid(row=0, column=3, padx=(0, 16), pady=10)

        # Console
        console_card = _card(main)
        console_card.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 8))
        console_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            console_card, text="Output Console", font=config.FONTS["small"],
            text_color=config.COLORS["text_muted"], anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(10, 0))

        self.console = ctk.CTkTextbox(
            console_card, height=160, corner_radius=8,
            fg_color=config.COLORS["surface_alt"],
            text_color=config.COLORS["text"],
            font=config.FONTS["mono"],
            border_color=config.COLORS["border"], border_width=1,
            wrap="word",
        )
        self.console.grid(row=1, column=0, sticky="nsew", padx=12, pady=(6, 12))
        self.console.configure(state="disabled")

        # Status bar
        status = ctk.CTkFrame(
            main, fg_color=config.COLORS["sidebar"], height=28, corner_radius=0,
        )
        status.grid(row=4, column=0, sticky="ew")
        status.grid_columnconfigure(1, weight=1)
        status.grid_propagate(False)

        self.status_left = ctk.CTkLabel(
            status, text="● Ready", font=config.FONTS["caption"],
            text_color=config.COLORS["success"], anchor="w",
        )
        self.status_left.grid(row=0, column=0, sticky="w", padx=14)

        self.status_right = ctk.CTkLabel(
            status,
            text=f"{config.APP_NAME} v{config.APP_VERSION}",
            font=config.FONTS["caption"],
            text_color=config.COLORS["text_muted"], anchor="e",
        )
        self.status_right.grid(row=0, column=2, sticky="e", padx=14)

    # ------------------------------------------------------------------ #
    # Navigation & logging
    # ------------------------------------------------------------------ #

    def _show(self, page_id: str) -> None:
        if page_id not in self.pages:
            return
        self.pages[page_id].tkraise()
        self.current_page_id = page_id

        # update nav button styles
        for key, btn in self.nav_buttons.items():
            if key == page_id:
                btn.configure(
                    fg_color=config.COLORS["surface_hover"],
                    text_color=config.COLORS["primary"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=config.COLORS["text_muted"],
                )

        title = next(
            (label for k, label, _ in config.NAV_ITEMS if k == page_id),
            page_id.capitalize(),
        )
        self.header_title.configure(text=title)

    def log(self, message: str) -> None:
        """Append a timestamped line to the output console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f"[{timestamp}] {message}\n"
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")

    def clear_console(self) -> None:
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self.log("Console cleared.")

    def set_status(self, text: str, color: str | None = None) -> None:
        self.status_left.configure(
            text=text, text_color=color or config.COLORS["success"]
        )

    # ------------------------------------------------------------------ #
    # Command + actions
    # ------------------------------------------------------------------ #

    def safe_run(self, label: str, action: Callable[[], str]) -> None:
        """Run an action, log success/failure, and update the status bar."""
        try:
            self.log(f"{label}…")
            result = action()
            if result:
                self.log(str(result))
            self.set_status("● Ready", config.COLORS["success"])
        except Exception as exc:
            self.log(f"ERROR: {exc}")
            self.set_status("● Error", config.COLORS["danger"])

    def _on_command(self) -> None:
        raw = self.command_entry.get().strip()
        if not raw:
            return
        self.command_entry.delete(0, "end")
        self.log(f"> {raw}")
        try:
            result = system.run_command(raw)
            if result == "__CLEAR__":
                self.clear_console()
                return
            self.log(result)
            self.set_status("● Ready", config.COLORS["success"])
        except Exception as exc:
            self.log(f"ERROR: {exc}")
            self.set_status("● Error", config.COLORS["danger"])

    # ------------------------------------------------------------------ #
    # Live refresh loop
    # ------------------------------------------------------------------ #

    def _tick(self) -> None:
        # Update clock
        self.header_clock.configure(
            text=f"{monitor.current_date()}   •   {monitor.current_time()}"
        )

        # Refresh current page if it knows how
        page = self.pages.get(self.current_page_id)
        if page is not None and hasattr(page, "refresh"):
            try:
                page.refresh()  # type: ignore[attr-defined]
            except Exception as exc:
                self.log(f"Refresh error: {exc}")

        self.after(config.REFRESH_INTERVAL_MS, self._tick)
