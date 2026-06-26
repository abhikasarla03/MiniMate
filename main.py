"""
MintMate - Linux Desktop Productivity Assistant
================================================

Entry point for the MintMate application.

Run:
    python main.py
"""

from __future__ import annotations

import sys
import traceback

from gui import MintMateApp


def main() -> int:
    """Launch the MintMate application.

    Returns the process exit code.
    """
    try:
        app = MintMateApp()
        app.mainloop()
        return 0
    except KeyboardInterrupt:
        print("\n[MintMate] Interrupted by user.")
        return 0
    except Exception:  # pragma: no cover - top-level safety net
        print("[MintMate] Fatal error:", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
