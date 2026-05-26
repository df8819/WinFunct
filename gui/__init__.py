"""WinFunct v2.000 - Windows Support Tool"""
import sys
import ctypes

from core.admin import ensure_admin
from config import LOGO


def setup_console():
    """Ensure a visible console window exists for status output."""
    if sys.platform != "win32":
        return
    kernel32 = ctypes.windll.kernel32
    if not kernel32.GetConsoleWindow():
        kernel32.AllocConsole()
    kernel32.SetConsoleOutputCP(65001)


def main():
    setup_console()
    print(LOGO)
    print("  Checking privileges...")

    if not ensure_admin():
        return

    print("  Running with admin privileges ✓")
    print("  Launching GUI...\n")

    from gui.app import Application
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
