# File for variables/configs - Less clutter in main file

# WinFunct Logo
LOGO = f"""
   ▒▓▓▓▓▓▓    ▓▓▓▓▓▓▓░   ▒▓▓▓▓▓▒░ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒  
  █████████ ░█████████▓ ██████████████████████████████████████████████████ 
  ▓█      █▒██       █▓▓█      █ █                  █                   █▓ 
   █░     ███        ▓██▓     █▓▓█             ░▒▒▒▓█░▒▒▒░        ▒▒▒▒▒▓█  
   █▓     ██         ▓█▓     ██ ██     ████████████████████     ░████████  
   ██     █▓         ▒█     ██  █▓     ██▓▓▓▓▓█▓         ▓█     ██         
   ██                      ▓█░ ▓█             █          ██     ██         
   ██          █▓          █▓  ██     █████████          █▒     █░         
   ▓█         ▓█▓         ██   █▓     █▓▓▓▓▓▓▓          ▓█     ▓█          
   ▓█        ▒██▓        ██   ▒█     ▓█                 ██     ██          
    █░       █▓▓█       ▓█    ██     ██   ╔════════╗    █░     █▓          
    ██████████ ▓█▓███████▓    ██▓▓█▓▓█▓   ║WinFunct║   ▓█▓▓▓█▓██           
     ▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓░     ▒▓▓▓▓▓▓▓    ╚════════╝    ▓▓▓▓▓▓▓            
"""

# WinFunct version number
VERSION_NUMBER = "1.662"

# Use the version number in different strings
VERSION = f"Use at your own risk and responsibility - v{VERSION_NUMBER}"
VERSION_SHORT = f"v{VERSION_NUMBER}"

# UI COLOR section
UI_COLOR = "#2f3128"  # General App/Tab/Button Background
BUTTON_BG_COLOR = "#575a4b"  # Background color for buttons
BUTTON_TEXT_COLOR = "#ffffff"  # Text color
BOTTOM_BORDER_COLOR = "#ff8f20"  # Bottom border color
VERSION_LABEL_TEXT = "#bf6000"  # Label text color

# UI STYLE section
BUTTON_STYLE = "raised"  # flat, solid, raised, sunken, ridge, groove

# noinspection SpellCheckingInspection
BORDER_WIDTH = "1"  # thiccness in pixel

# GitHub repo link
LINK = "https://github.com/df8819/WinFunct"

# The curl-command to copy to the clipboard
AdGuardClipBoard = 'curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v'

# Links for the "Link Opener" window
links = {
    "Dev Tools": {
        "Python": "https://www.python.org/downloads/",
        "Git": "https://git-scm.com/downloads",
        "GitHub Desktop": "https://desktop.github.com",
        "Visual Studio Code": "https://code.visualstudio.com/download",
        "PyCharm": "https://www.jetbrains.com/pycharm/download/?section=windows",
    },
    "Network Tools": {
        "WireShark": "https://www.wireshark.org/download.html",
        "Advanced IP Scanner": "https://www.advanced-ip-scanner.com/de/",
        "PuTTY (SSH)": "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html",
        "TCPView": "https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview",
        "NetManSet": "https://www.netsetman.com/en/freeware",
    },
    "System Utilities": {
        "Process Explorer": "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer",
        "HxD Hex Editor": "https://mh-nexus.de/en/programs.php",
        "HWInfo64": "https://www.hwinfo.com/download/",
        "MSI Afterburner": "https://www.msi.com/Landing/afterburner/graphics-cards",
        "WinDirStat": "https://sourceforge.net/projects/windirstat/",
        "Create answer files": "https://schneegans.de/windows/unattend-generator/",
        "StartIsBack Shell": "https://www.startisback.com/",
    },
    "Remote & Collaboration": {
        "TeamViewer": "https://www.teamviewer.com/de/download/windows/",
        "RustDesk": "https://github.com/rustdesk/rustdesk/releases/tag/1.2.3",
        "MS PowerToys": "https://github.com/microsoft/PowerToys/releases/tag/v0.75.1",
    },
    "Disk & Partition Tools": {
        "Etcher USB Creator": "https://etcher.balena.io",
        "Raspberry Pi Imager": "https://www.raspberrypi.com/software/",
        "Partition Manager": "https://www.paragon-software.com/free/pm-express/#features",
        "LinuxLive USB Creator": "https://www.linuxliveusb.com/downloads/?stable",
        "Rufus USB Creator": "https://rufus.ie/en/",
        "AnyBurn": "http://www.anyburn.com/download.php",
    },
    "Productivity": {
        "PicPick": "https://picpick.app/en/download/",
        "Notepad++": "https://notepad-plus-plus.org/downloads/v8.5.8/",
        "Total Commander": "https://www.ghisler.com/ddownload.htm",
        "Posy Cursors": "http://www.michieldb.nl/other/cursors",
        "Bitwarden": "https://bitwarden.com/download/",
        "FFMPEG GUI": "https://jeanslack.github.io/Videomass/Pages/Packages/Windows.html",
    },
    "Tutorials & Resources": {
        "MAS Script": "https://massgrave.dev/index.html",
        "AdGuard Home": "https://youtu.be/B2V_8M9cjYw?si=Z_AeA4hCFGiElOHB",
        "NSE Lab": "https://nse.digital",
    },
}

# Script for Website online status checker
batch_script = r"""
@echo off
setlocal enabledelayedexpansion

set website={{website_url}}

:check
for /f "tokens=*" %%a in ('curl -Is !website! -o nul -w "%%{http_code} %%{time_total} %%{remote_ip}"') do (
    set result=%%a
)

for /f "tokens=1,2,3" %%a in ("!result!") do (
    set status_code=%%a
    set response_time=%%b
    set server_ip=%%c
)

set domain=%website:~7%

echo.
echo ============ Website Status =============
if !status_code! equ 200 (
    echo Website is         ONLINE
) else if !status_code! equ 201 (
    echo Website is         ONLINE but -Created-
) else if !status_code! equ 202 (
    echo Website is         ONLINE but -Accepted-
) else if !status_code! equ 204 (
    echo Website is         ONLINE but -No Content-
) else if !status_code! equ 301 (
    echo Website is         ONLINE but -Moved Permanently-
) else if !status_code! equ 302 (
    echo Website is         ONLINE but -Found-
) else if !status_code! equ 303 (
    echo Website is         ONLINE but -See Other-
) else if !status_code! equ 304 (
    echo Website is         ONLINE but -Not Modified-
) else if !status_code! equ 307 (
    echo Website is         ONLINE but -Temporary Redirect-
) else if !status_code! equ 308 (
    echo Website is         ONLINE but -Permanent Redirect-
) else if !status_code! equ 400 (
    echo Website is         ONLINE but -Bad Request-
) else if !status_code! equ 401 (
    echo Website is         ONLINE but -Unauthorized-
) else if !status_code! equ 403 (
    echo Website is         ONLINE but -Forbidden-
) else if !status_code! equ 404 (
    echo Website is         ONLINE but -Page Not Found-
) else if !status_code! equ 405 (
    echo Website is         ONLINE but -Method Not Allowed-
) else if !status_code! equ 406 (
    echo Website is         ONLINE but -Not Acceptable-
) else if !status_code! equ 408 (
    echo Website is         ONLINE but -Request Timeout-
) else if !status_code! equ 410 (
    echo Website is         ONLINE but -Gone-
) else if !status_code! equ 429 (
    echo Website is         ONLINE but -Too Many Requests-
) else if !status_code! equ 500 (
    echo Website is         ONLINE but -Internal Server Error-
) else if !status_code! equ 501 (
    echo Website is         ONLINE but -Not Implemented-
) else if !status_code! equ 502 (
    echo Website is         ONLINE but -Bad Gateway-
) else if !status_code! equ 503 (
    echo Website is         ONLINE but -Service Unavailable-
) else if !status_code! equ 504 (
    echo Website is         ONLINE but -Gateway Timeout-
) else (
    echo Website is         OFFLINE
)

echo Domain/URL:        %website%
echo Server IP:         !server_ip!    
echo Status Code:       !status_code!
echo Response Time:     !response_time! seconds
echo Request Timestamp: %date% %time%
echo =========================================

if !status_code! equ 200 (
    pause
    exit /b 0
) else if !status_code! equ 201 (
    pause
    exit /b 201
) else if !status_code! equ 202 (
    pause
    exit /b 202
) else if !status_code! equ 204 (
    pause
    exit /b 204
) else if !status_code! equ 301 (
    pause
    exit /b 301
) else if !status_code! equ 302 (
    pause
    exit /b 302
) else if !status_code! equ 303 (
    pause
    exit /b 303
) else if !status_code! equ 304 (
    pause
    exit /b 304
) else if !status_code! equ 307 (
    pause
    exit /b 307
) else if !status_code! equ 308 (
    pause
    exit /b 308
) else if !status_code! equ 400 (
    pause
    exit /b 400
) else if !status_code! equ 401 (
    pause
    exit /b 401
) else if !status_code! equ 403 (
    pause
    exit /b 403
) else if !status_code! equ 404 (
    pause
    exit /b 404
) else if !status_code! equ 405 (
    pause
    exit /b 405
) else if !status_code! equ 406 (
    pause
    exit /b 406
) else if !status_code! equ 408 (
    pause
    exit /b 408
) else if !status_code! equ 410 (
    pause
    exit /b 410
) else if !status_code! equ 429 (
    pause
    exit /b 429
) else if !status_code! equ 500 (
    pause
    exit /b 500
) else if !status_code! equ 501 (
    pause
    exit /b 501
) else if !status_code! equ 502 (
    pause
    exit /b 502
) else if !status_code! equ 503 (
    pause
    exit /b 503
) else if !status_code! equ 504 (
    pause
    exit /b 504
) else (
    echo Checking again in 60 seconds...
    timeout /t 60 >nul
    goto check
)
                        """

# Option Buttons for Option Tab (UI element)
# Windows Management and Configuration Tools
windows_management_options = [
    ("Registry Editor", "regedit"),
    ("PC Manager", "compmgmt.msc"),
    ("Event Viewer", "eventvwr.msc"),
    ("Services Manager", "services.msc"),
    ("Group Policy", "gpedit.msc"),
    ("Programs/Features", "appwiz.cpl"),
    ("Windows Version", "winver"),
    ("Advanced Settings", "SystemPropertiesAdvanced"),
    ("User Accout Control", "useraccountcontrolsettings"),
    ("Disk Manager", "diskmgmt.msc"),
    ("Computer Name", "SystemPropertiesComputerName"),
    ("ODBC Manager", "odbcad32"),
    ("Shared Folders", "fsmgmt.msc"),
    ("Mobility Center", "mblctr"),
]

# Security and Networking Tools
security_and_networking_options = [
    ("Security Center", "start ms-settings:windowsdefender"),
    ("Security Policy", "secpol.msc"),
    ("Firewall Advanced", "wf.msc"),
    ("Network Sharing", "control /name Microsoft.NetworkAndSharingCenter"),
    ("Internet Options", "inetcpl.cpl"),
    ("Credential Manager", "control /name Microsoft.CredentialManager"),
    ("Windows Firewall", "firewall.cpl"),
    ("Network Adapters", "ncpa.cpl"),
    ("Remote Connections", "control /name Microsoft.RemoteAppAndDesktopConnections"),
    ("VPN Settings", "start ms-settings:network-vpn"),
    ("Wi-Fi Settings", "start ms-settings:network-wifi"),
    ("Ethernet Settings", "start ms-settings:network-ethernet"),
    ("Proxy Settings", "start ms-settings:network-proxy"),
]

# System Tools and Utilities
system_tools_options = [
    ("Edit Hosts File", "notepad C:\\Windows\\System32\\drivers\\etc\\hosts"),
    ("Task Manager", "taskmgr"),
    ("Control Panel", "control"),
    ("Device Manager", "devmgmt.msc"),
    ("Performance Monitor", "perfmon"),
    ("Resource Monitor", "resmon"),
    ("Device Pairing", "devicepairingwizard"),
    ("Windows Features", "optionalfeatures"),
    ("System Info", "msinfo32"),
]

# Remote Management and Virtualization Tools
remote_and_virtualization_options = [
    ("Remote Desktop", "mstsc"),
    ("RDP Settings", "start ms-settings:remotedesktop"),
    ("Hyper-V Manager", "C:\\Windows\\System32\\virtmgmt.msc"),
    ("Environment Vars", "rundll32.exe sysdm.cpl,EditEnvironmentVariables"),
]

# Troubleshooting and Optimization Tools
troubleshooting_and_optimization_options = [
    ("Reliability Monitor", "perfmon /rel"),
    ("Disk Cleanup", "cleanmgr"),
    ("System Restore", "rstrui"),
    ("Optimize Drives", "dfrgui"),
    ("Memory Diagnostics", "MdSched"),
    ("DirectX Diagnostics", "dxdiag"),
    ("System Config", "msconfig"),
    ("Windows Update", "start ms-settings:windowsupdate"),
]

# Shell commands
netsh_commands = [
    ("IP Configuration", "netsh interface ip show config"),
    ("Interface List", "netsh interface show interface"),
    ("IPv4 Interface", "netsh interface ipv4 show interface"),
    ("IPv6 Interface", "netsh interface ipv6 show interface"),
    ("IP Address Info", "netsh interface ip show addresses"),
    ("DNS Configuration", "netsh interface ip show dns"),
    ("Display DNS Cache", "ipconfig /displaydns"),
    ("Firewall State", "netsh advfirewall show currentprofile state"),
    ("Routing Table", "netsh interface ipv4 show route"),
    ("Wi-Fi Profiles", "netsh wlan show profiles"),
    ("Wi-Fi Settings", "netsh wlan show settings"),
    ("Wi-Fi Networks", "netsh wlan show networks"),
    ("Network Stats", "netstat -s"),
    ("ARP Scan", "powershell.exe arp -a"),
    ("Shutdown -i", "shutdown -i"),
]
