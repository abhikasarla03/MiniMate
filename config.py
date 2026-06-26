"""
config.py
=========

Central configuration for MintMate: theme colors, fonts, sizing,
and shared constants. Tweak values here to re-skin the entire app.
"""

from __future__ import annotations

APP_NAME = "MintMate"
APP_TAGLINE = "Your Linux Mint Productivity Assistant"
APP_VERSION = "1.0.0"
APP_AUTHOR = "MintMate Team"

# Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
MIN_WIDTH = 1024
MIN_HEIGHT = 640

# CustomTkinter appearance
APPEARANCE_MODE = "dark"          # "dark" | "light" | "system"
COLOR_THEME = "dark-blue"          # built-in CTk theme

# Brand color palette (used for custom widgets and cards)
COLORS = {
    "bg":             "#0F1115",   # app background
    "sidebar":        "#13161D",   # sidebar background
    "surface":        "#181C25",   # card background
    "surface_hover":  "#1F2430",
    "surface_alt":    "#11141B",   # console background
    "border":         "#252A36",
    "text":           "#E6E8EC",
    "text_muted":     "#8A92A6",
    "primary":        "#3DDC97",   # mint green accent
    "primary_hover":  "#2EC586",
    "accent":         "#5B8DEF",   # secondary blue accent
    "accent_hover":   "#4A78D6",
    "warning":        "#F5A524",
    "danger":         "#F05D5E",
    "success":        "#3DDC97",
}

# Typography
FONT_FAMILY = "Segoe UI"           # falls back gracefully on Linux
FONT_MONO = "JetBrains Mono"

FONTS = {
    "title":   (FONT_FAMILY, 22, "bold"),
    "header":  (FONT_FAMILY, 16, "bold"),
    "body":    (FONT_FAMILY, 13, "normal"),
    "small":   (FONT_FAMILY, 11, "normal"),
    "caption": (FONT_FAMILY, 10, "normal"),
    "mono":    (FONT_MONO, 11, "normal"),
    "metric":  (FONT_FAMILY, 26, "bold"),
}

# Sidebar nav items: (id, label, icon-glyph)
NAV_ITEMS = [
    ("dashboard",  "Dashboard",     "▦"),
    ("apps",       "Applications",  "▶"),
    ("monitor",    "System Monitor", "◔"),
    ("utilities",  "Utilities",     "✦"),
    ("settings",   "Settings",      "⚙"),
    ("about",      "About",         "ⓘ"),
]

# How often the dashboard refreshes live stats (ms)
REFRESH_INTERVAL_MS = 1500
