"""Admin privilege elevation for Windows."""
import ctypes
import os
import sys
import subprocess


def is_admin() -> bool:
    """Check if current process has admin rights."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except OSError:
        return False


def _check_admin_via_groups() -> bool:
    """Fallback: check admin via whoami /groups."""
    try:
        output = subprocess.check_output(
            "whoami /groups", shell=True, text=True, errors="replace"
        )
        return "S-1-16-12288" in output
    except subprocess.CalledProcessError:
        return False


def _relaunch_elevated() -> bool:
    """Re-launch current process with elevation."""
    try:
        if getattr(sys, "frozen", False):
            executable = sys.executable
            params = " ".join(f'"{a}"' for a in sys.argv[1:])
        else:
            executable = sys.executable
            script = os.path.abspath(sys.argv[0])
            params = f'"{script}" ' + " ".join(f'"{a}"' for a in sys.argv[1:])

        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, params, None, 1
        )
        return ret > 32
    except Exception as e:
        print(f"  Error elevating: {e}")
        return False


def ensure_admin() -> bool:
    """Ensure we're running as admin. Re-launches elevated if not.
    Returns True if we should continue, False if we should exit.
    """
    if is_admin() or _check_admin_via_groups():
        return True

    print("  Requesting administrative privileges...")
    if _relaunch_elevated():
        sys.exit(0)
    else:
        print("  ✗ Failed to obtain admin privileges.")
        return True
