"""Shared utilities."""
import ctypes
import locale
import os
import shutil
import subprocess
import sys
from ctypes import wintypes
from pathlib import Path


def get_app_root() -> Path:
    """Get the application root directory."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_powershell_path() -> str:
    """Find the best available PowerShell executable (absolute path)."""
    candidates = [
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return shutil.which("pwsh") or shutil.which("powershell") or candidates[0]


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

SE_ERR = {
    0: "OOM", 2: "FILE_NOT_FOUND", 3: "PATH_NOT_FOUND", 5: "ACCESSDENIED",
    8: "OOM", 11: "BAD_FORMAT", 26: "SHARE", 27: "ASSOCINCOMPLETE",
    28: "DDETIMEOUT", 29: "DDEFAIL", 30: "DDEBUSY", 31: "NOASSOC",
    32: "DLLNOTFOUND",
}


def shell_exec(verb: str, exe: str, args: str, hwnd=None) -> int:
    """ShellExecuteW wrapper. Returns the raw ret; <= 32 means failure."""
    shell32 = ctypes.WinDLL("shell32", use_last_error=True)
    shell32.ShellExecuteW.argtypes = (
        wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR,
        wintypes.LPCWSTR, wintypes.LPCWSTR, ctypes.c_int,
    )
    shell32.ShellExecuteW.restype = ctypes.c_ssize_t
    ret = shell32.ShellExecuteW(hwnd, verb, exe, args, None, 1)
    if ret <= 32:
        print(f"  ShellExecuteW ret={ret} ({SE_ERR.get(ret, '?')}) "
              f"GetLastError={ctypes.get_last_error()} exe={exe!r} args={args!r}")
    return ret