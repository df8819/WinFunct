"""Shared utilities."""
import locale
import os
import subprocess
import sys
from pathlib import Path


def get_app_root() -> Path:
    """Get the application root directory."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_powershell_path() -> str:
    """Find the best available PowerShell executable."""
    candidates = [
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return "pwsh.exe"


def run_detached(command: str, shell: bool = True):
    """Run a command in a new detached process."""
    subprocess.Popen(command, shell=shell, creationflags=subprocess.CREATE_NEW_CONSOLE)


def decode_output(output_bytes: bytes) -> str:
    """Decode subprocess output trying multiple encodings."""
    for encoding in [locale.getpreferredencoding(), "utf-8", "cp1252", "cp850", "latin1"]:
        try:
            return output_bytes.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return output_bytes.decode("utf-8", errors="replace")


def open_folder(path: Path):
    """Open a folder in the system file manager."""
    os.startfile(str(path))
