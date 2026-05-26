"""Network-related functionality."""
import re
import socket
import subprocess
import time
from typing import Optional

import psutil
import requests

from core.utils import decode_output


def check_internet(timeout: int = 5) -> list[tuple[bool, str, float]]:
    """Run connectivity checks. Returns list of (success, message, latency_ms)."""
    results = []
    checks = [
        ("Ping 8.8.8.8", _check_ping),
        ("Socket 8.8.8.8:53", _check_socket),
        ("HTTP google.com", _check_http),
    ]
    for name, func in checks:
        start = time.time()
        success, msg = func(timeout)
        latency = round((time.time() - start) * 1000, 2)
        results.append((success, msg, latency))
    return results


def _check_ping(timeout: int) -> tuple[bool, str]:
    try:
        subprocess.run(
            ["ping", "-n", "1", "-w", str(timeout * 1000), "8.8.8.8"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        return True, "Ping 8.8.8.8 successful"
    except subprocess.CalledProcessError:
        return False, "Ping 8.8.8.8 failed"


def _check_socket(timeout: int) -> tuple[bool, str]:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout).close()
        return True, "Socket 8.8.8.8:53 successful"
    except OSError:
        return False, "Socket 8.8.8.8:53 failed"


def _check_http(timeout: int) -> tuple[bool, str]:
    try:
        r = requests.get("http://www.google.com", timeout=timeout)
        if r.status_code == 200:
            return True, "HTTP google.com successful"
    except requests.RequestException:
        pass
    return False, "HTTP google.com failed"


def get_local_ip_info() -> str:
    """Get local network adapter info."""
    lines = ["═══ Local Network ═══\n"]
    for adapter, addresses in psutil.net_if_addrs().items():
        ipv4 = [a.address for a in addresses if a.family == 2]
        if ipv4:
            lines.append(f"  {adapter}: {', '.join(ipv4)}")
    return "\n".join(lines) if len(lines) > 1 else lines[0] + "  No adapters found."


def get_public_ip_info(timeout: int = 5) -> dict:
    """Fetch public IP info from multiple APIs with fallback."""
    apis = [
        ("https://ipapi.co/json/", _parse_ipapi),
        ("https://ip-api.com/json/", _parse_ipapi_alt),
        ("https://ipinfo.io/json", _parse_ipinfo),
    ]
    for url, parser in apis:
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": "WinFunct/2.0"})
            r.raise_for_status()
            return parser(r.json())
        except (requests.RequestException, KeyError, ValueError):
            continue
    return {"error": "Could not fetch public IP from any service."}


def _parse_ipapi(data: dict) -> dict:
    return {
        "ip": data.get("ip"), "isp": data.get("org"),
        "country": data.get("country_name"), "city": data.get("city"),
        "lat": data.get("latitude"), "lon": data.get("longitude"),
        "timezone": data.get("timezone"),
    }


def _parse_ipapi_alt(data: dict) -> dict:
    return {
        "ip": data.get("query"), "isp": data.get("isp"),
        "country": data.get("country"), "city": data.get("city"),
        "lat": data.get("lat"), "lon": data.get("lon"),
        "timezone": data.get("timezone"),
    }


def _parse_ipinfo(data: dict) -> dict:
    loc = data.get("loc", ",").split(",")
    return {
        "ip": data.get("ip"), "isp": data.get("org"),
        "country": data.get("country"), "city": data.get("city"),
        "lat": loc[0] if len(loc) == 2 else None,
        "lon": loc[1] if len(loc) == 2 else None,
        "timezone": data.get("timezone"),
    }


def get_wifi_profiles() -> list[str] | str:
    """Get list of Wi-Fi profile names."""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True, timeout=10
        )
        output = decode_output(result.stdout)
    except (subprocess.SubprocessError, OSError):
        return "Failed to query Wi-Fi profiles."

    from config import no_adapter_messages
    if any(msg in output for msg in no_adapter_messages):
        return "No Wi-Fi adapter detected."

    profiles = re.findall(r"All User Profile\s*:\s*(.+)", output)
    return [p.strip() for p in profiles if p.strip()] or "No Wi-Fi profiles found."


def get_wifi_password(profile: str) -> Optional[str]:
    """Extract password for a specific Wi-Fi profile."""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "profile", profile, "key=clear"],
            capture_output=True, timeout=10
        )
        output = decode_output(result.stdout)
        match = re.search(r"Key Content\s*[:：]\s*(.+)", output)
        return match.group(1).strip() if match else None
    except (subprocess.SubprocessError, OSError):
        return None


def get_netstat_connections() -> list[tuple]:
    """Get active network connections via netstat."""
    try:
        result = subprocess.check_output("netstat -b -n -o", shell=True, text=True, errors="replace")
    except subprocess.CalledProcessError:
        return []

    connections = []
    current_app = ""
    for line in result.splitlines():
        stripped = line.strip()
        if stripped.startswith(("TCP", "UDP")):
            parts = stripped.split()
            if len(parts) >= 4:
                state = parts[3] if parts[0] == "TCP" and len(parts) > 4 else ""
                if state == "TIME_WAIT":
                    continue
                pid = parts[-1]
                connections.append((parts[0], parts[1], parts[2], state, pid, current_app))
        elif "[" in line and "]" in line:
            match = re.findall(r"\[(.+?)\]", line)
            current_app = match[0] if match else ""
    return connections
