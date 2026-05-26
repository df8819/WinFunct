"""Disk operations."""
import subprocess

import psutil


def get_disk_info() -> str:
    """Get disk information."""
    lines = ["═══ Disk Information ═══\n"]

    try:
        out = subprocess.check_output(
            'powershell "Get-Disk | Format-Table -AutoSize Number, FriendlyName, @{Name=\'Size GB\'; Expression={[int]($_.Size/1GB)}}"',
            shell=True, text=True, timeout=15
        )
        lines.append(out.strip())
    except (subprocess.SubprocessError, OSError):
        lines.append("  Could not query physical disks.")

    lines.append("\n═══ Storage Metrics ═══\n")
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            lines.append(
                f"  {part.mountpoint}  "
                f"Total: {usage.total / (1024**3):.1f} GB  "
                f"Used: {usage.used / (1024**3):.1f} GB  "
                f"Free: {usage.free / (1024**3):.1f} GB  "
                f"({usage.percent}%)"
            )
        except OSError:
            continue
    return "\n".join(lines)


def get_available_drives() -> list[str]:
    """Get list of available drive letters with sizes."""
    drives = []
    for part in psutil.disk_partitions(all=False):
        if part.device and part.device[0].isalpha():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                drives.append(f"{part.device[0]}: ({usage.total / (1024**3):.1f} GB)")
            except OSError:
                continue
    return drives


def run_winsat_disk(drive_letter: str):
    """Run WinSAT disk speed test in a new elevated window."""
    cmd = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/c winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
    subprocess.Popen(cmd, shell=True)


def run_chkdsk(drive: str, options: str):
    """Run chkdsk in a new cmd window."""
    subprocess.Popen(f"start cmd /k chkdsk {drive} {options}", shell=True)
