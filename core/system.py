"""System information and management."""
import csv
import os
import subprocess
from pathlib import Path

import psutil
import wmi
import winreg

from core.utils import get_app_root


def get_system_info() -> dict:
    """Gather comprehensive system information via WMI."""
    c = wmi.WMI()
    info = {}

    for os_obj in c.Win32_OperatingSystem():
        info["OS"] = os_obj.Caption
        info["OS Version"] = os_obj.Version
        info["OS Build"] = os_obj.BuildNumber
        info["OS Architecture"] = os_obj.OSArchitecture

    for cpu in c.Win32_Processor():
        info["CPU"] = cpu.Name.strip()
        info["CPU Cores"] = cpu.NumberOfCores
        info["CPU Threads"] = cpu.ThreadCount
        info["CPU Max MHz"] = cpu.MaxClockSpeed

    total = sum(int(m.Capacity) for m in c.Win32_PhysicalMemory())
    info["RAM Total"] = f"{total / (1024**3):.1f} GB"
    info["RAM Modules"] = len(list(c.Win32_PhysicalMemory()))

    for disk in c.Win32_DiskDrive():
        info["Disk"] = disk.Model.strip()
        info["Disk Size"] = f"{int(disk.Size) / (1024**3):.0f} GB"

    for board in c.Win32_BaseBoard():
        info["Motherboard"] = f"{board.Manufacturer.strip()} {board.Product.strip()}"

    for gpu in c.Win32_VideoController():
        info["GPU"] = gpu.Name.strip()

    adapters = [a.Name.strip() for a in c.Win32_NetworkAdapter() if a.NetEnabled]
    info["Network Adapters"] = adapters

    info["Installed Software"] = get_installed_software()

    return info


def get_installed_software() -> list[str]:
    """Get list of installed software from registry."""
    software = set()
    keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", winreg.KEY_WOW64_64KEY),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", winreg.KEY_WOW64_32KEY),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0),
    ]
    for hive, path, flag in keys:
        try:
            with winreg.OpenKey(hive, path, 0, winreg.KEY_READ | flag) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if name and name.strip():
                                software.add(name.strip())
                    except (FileNotFoundError, OSError):
                        continue
        except OSError:
            continue
    return sorted(software)


def save_system_info_html(info: dict, path: Path):
    """Save system info as a styled HTML report."""
    html = [
        "<html><head><style>",
        "body{font-family:Segoe UI,Arial,sans-serif;margin:20px;background:#1e1e1e;color:#d4d4d4}",
        "table{border-collapse:collapse;width:100%}",
        "th,td{border:1px solid #444;padding:8px;text-align:left}",
        "th{background:#264f78;color:#fff}",
        "tr:nth-child(even){background:#2d2d2d}",
        "</style></head><body><h1>System Information</h1><table>",
        "<tr><th>Field</th><th>Value</th></tr>",
    ]
    for key, value in info.items():
        if isinstance(value, list):
            val = "<ul>" + "".join(f"<li>{v}</li>" for v in value) + "</ul>"
        else:
            val = str(value)
        html.append(f"<tr><td>{key}</td><td>{val}</td></tr>")
    html.append("</table></body></html>")
    path.write_text("\n".join(html), encoding="utf-8")


def save_system_info_csv(info: dict, path: Path):
    """Save system info as CSV for comparison."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Value"])
        for key, value in info.items():
            if isinstance(value, list):
                writer.writerow([key, ""])
                for item in value:
                    writer.writerow(["", item])
            else:
                writer.writerow([key, value])


def flush_dns():
    """Release/flush/renew IP configuration."""
    commands = [
        ("ipconfig /release", "Releasing IP..."),
        ("ipconfig /flushdns", "Flushing DNS..."),
        ("ipconfig /renew", "Renewing IP..."),
    ]
    for cmd, desc in commands:
        print(f"  {desc}")
        subprocess.run(f"cmd.exe /c {cmd}", shell=True)
    print("  Done.")


def restore_system_health():
    """Run DISM cleanup and restorehealth."""
    print("  Running DISM cleanup-image...")
    subprocess.run(["dism", "/online", "/cleanup-image", "/startcomponentcleanup"])
    print("  Running DISM restorehealth...")
    subprocess.run(["dism", "/online", "/cleanup-image", "/restorehealth"])


def clear_icon_cache():
    """Kill explorer, clear icon cache, restart explorer."""
    subprocess.run("taskkill /f /im explorer.exe", shell=True)
    local = Path(os.environ["LOCALAPPDATA"])
    cache_file = local / "IconCache.db"
    if cache_file.exists():
        cache_file.unlink(missing_ok=True)
    cache_dir = local / "Microsoft" / "Windows" / "Explorer"
    for f in cache_dir.glob("iconcache*"):
        f.unlink(missing_ok=True)
    subprocess.Popen("explorer.exe")


def open_autostart_locations():
    """Open Windows autostart folder locations."""
    locations = [
        Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup",
        Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp"),
        Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
    ]
    for loc in locations:
        if loc.exists():
            print(f"  Opening: {loc}")
            os.startfile(str(loc))
