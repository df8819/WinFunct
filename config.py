# File for variables/configs - Less clutter in main file
pass
# WinFunct Logo
LOGO = f"""   ▒▓▓▓▓▓▓    ▓▓▓▓▓▓▓░   ▒▓▓▓▓▓▒░ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒  
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
     ▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓░     ▒▓▓▓▓▓▓▓    ╚════════╝    ▓▓▓▓▓▓▓            """

# WinFunct version number
VERSION_NUMBER = "1.702"

# Use the version number in different strings
VERSION = f"Use at your own risk and responsibility - v{VERSION_NUMBER}"
VERSION_SHORT = f"v{VERSION_NUMBER}"

# UI COLOR section
UI_COLOR = "#e4e4e4"  # General App/Tab/Button Background
BUTTON_BG_COLOR = "#d4d4d4"  # Background color for buttons
BUTTON_TEXT_COLOR = "#000000"  # Text color
BOTTOM_BORDER_COLOR = "#5b5b5b"  # Bottom border color
VERSION_LABEL_TEXT = "#5f5f5f"  # Label text color

# UI STYLE section
BUTTON_STYLE = "solid"  # flat, solid, raised, sunken, ridge, groove
# noinspection SpellCheckingInspection
BORDER_WIDTH = "2"  # thiccness in pixel

# GitHub repo link
WINFUNCT_LINK = "https://github.com/df8819/WinFunct"
ADGUARD_LINK = "https://github.com/AdguardTeam/AdGuardHome"

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
        "NerdFonts": "https://www.nerdfonts.com/font-downloads",
    },
    "Network Tools": {
        "WireShark": "https://www.wireshark.org/download.html",
        "Advanced IP Scanner": "https://www.advanced-ip-scanner.com/de/",
        "PuTTY (SSH)": "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html",
        "MobaXterm": "https://mobaxterm.mobatek.net/download.html",
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
        "StartAllBack Shell": "https://www.startallback.com/",
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
        "Drive SnapShot": "http://drivesnapshot.de/de/index.htm",
    },
    "Productivity": {
        "PicPick": "https://picpick.app/en/download/",
        "Notepad++": "https://notepad-plus-plus.org/downloads/v8.5.8/",
        "Notepad++ Dark Theme": "https://github.com/60ss/Npp-1-Dark",
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
# noinspection SpellCheckingInspection
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

:: Use an array/map approach for status codes
set "status_200=ONLINE"
set "status_201=ONLINE but -Created-"
set "status_202=ONLINE but -Accepted-"
set "status_204=ONLINE but -No Content-"
set "status_301=ONLINE but -Moved Permanently-"
set "status_302=ONLINE but -Found-"
set "status_303=ONLINE but -See Other-"
set "status_304=ONLINE but -Not Modified-"
set "status_307=ONLINE but -Temporary Redirect-"
set "status_308=ONLINE but -Permanent Redirect-"
set "status_400=ONLINE but -Bad Request-"
set "status_401=ONLINE but -Unauthorized-"
set "status_403=ONLINE but -Forbidden-"
set "status_404=ONLINE but -Page Not Found-"
set "status_405=ONLINE but -Method Not Allowed-"
set "status_406=ONLINE but -Not Acceptable-"
set "status_408=ONLINE but -Request Timeout-"
set "status_410=ONLINE but -Gone-"
set "status_429=ONLINE but -Too Many Requests-"
set "status_500=ONLINE but -Internal Server Error-"
set "status_501=ONLINE but -Not Implemented-"
set "status_502=ONLINE but -Bad Gateway-"
set "status_503=ONLINE but -Service Unavailable-"
set "status_504=ONLINE but -Gateway Timeout-"

:: Display status using the array
if defined status_!status_code! (
    call echo Website is         %%status_!status_code!%%
) else (
    echo Website is         OFFLINE
)

echo Domain/URL:        %website%
echo Server IP:         !server_ip!    
echo Status Code:       !status_code!
echo Response Time:     !response_time! seconds
echo Request Timestamp: %date% %time%
echo =========================================

:: Check if status code is defined and exit with corresponding code
if defined status_!status_code! (
    pause
    exit /b !status_code!
) else (
    echo Checking again in 60 seconds...
    timeout /t 60 >nul
    goto check
)
                        """

# Option Buttons for Option Tab (UI element)
# System Management Tools
system_management_options = [
    # Core System Management
    ("Control Panel", "control"),
    ("Disk Manager", "diskmgmt.msc"),
    ("PC Manager", "compmgmt.msc"),
    ("Programs/Features", "appwiz.cpl"),
    ("Services Manager", "services.msc"),
    ("Task Manager", "taskmgr"),

    # System Information
    ("Computer Name", "SystemPropertiesComputerName"),
    ("System Info", "msinfo32"),
    ("Windows Version", "winver"),

    # User Management
    ("Group Policy", "gpedit.msc"),
    ("Shared Folders", "fsmgmt.msc"),
    ("User Account Control", "useraccountcontrolsettings"),
]

# Network & Security Tools
network_security_options = [
    # Network Management
    ("Ethernet Settings", "start ms-settings:network-ethernet"),
    ("Network Adapters", "ncpa.cpl"),
    ("Network Sharing", "control /name Microsoft.NetworkAndSharingCenter"),
    ("VPN Settings", "start ms-settings:network-vpn"),
    ("Wi-Fi Settings", "start ms-settings:network-wifi"),

    # Security Tools
    ("Credential Manager", "control /name Microsoft.CredentialManager"),
    ("Password Manager", "rundll32.exe keymgr.dll,KRShowKeyMgr"),
    ("Firewall Advanced", "wf.msc"),
    ("Security Center", "start ms-settings:windowsdefender"),
    ("Security Policy", "secpol.msc"),
    ("Windows Firewall", "firewall.cpl"),
    ("Internet Options", "control inetcpl.cpl"),

    # Remote Access
    ("RDP Settings", "start ms-settings:remotedesktop"),
    ("Remote Connections", "control /name Microsoft.RemoteAppAndDesktopConnections"),
    ("Remote Desktop", "mstsc"),
]

# Troubleshooting Tools
troubleshooting_options = [
    # System Diagnostics
    ("DirectX Diagnostics", "dxdiag"),
    ("Event Viewer", "eventvwr.msc"),
    ("Performance Monitor", "perfmon"),
    ("Reliability Monitor", "perfmon /rel"),
    ("Resource Monitor", "resmon"),

    # System Recovery
    ("System Config", "msconfig"),
    ("System Restore", "rstrui"),
    ("Windows Update", "start ms-settings:windowsupdate"),

    # Optimization
    ("Device Manager", "devmgmt.msc"),
    ("Disk Cleanup", "cleanmgr"),
    ("Memory Diagnostics", "MdSched"),
    ("Optimize Drives", "dfrgui"),
]

# Advanced Tools
advanced_tools_options = [
    # System Configuration
    ("Advanced Settings", "SystemPropertiesAdvanced"),
    ("Environment Variables", "rundll32.exe sysdm.cpl,EditEnvironmentVariables"),
    ("Registry Editor", "regedit"),
    ("Windows Features", "optionalfeatures"),

    # Development & Special Tools
    ("Edit Hosts File", "notepad C:\\Windows\\System32\\drivers\\etc\\hosts"),
    ("Hyper-V Manager", "C:\\Windows\\System32\\virtmgmt.msc"),
    ("Mobility Center", "mblctr"),
    ("ODBC Manager", "odbcad32"),

    # Network Diagnostics Commands
    ("ARP Scan", "powershell.exe arp -a"),
    ("DNS Configuration", "netsh interface ip show dns"),
    ("IP Configuration", "netsh interface ip show config"),
    ("Network Stats", "netstat -s"),
    ("Boot Loader Info", "bcdedit"),
]

# --- DISK INFO ---
chkdsk_help_content = """
Parameter                      Description
==========================================================================================================
<volume>                       Specifies the drive letter (followed by a colon), mount point,
                               or volume name. Example: "C:"
----------------------------------------------------------------------------------------------------------
[ [<path>]<filename> ]         Use with FAT and FAT32 only. Specifies the location and
                               name of a file or set of files that you want chkdsk to check
                               for fragmentation. You can use the ? and * wildcard characters
                               to specify multiple files.
----------------------------------------------------------------------------------------------------------
/f                             Fixes errors on the disk. The disk must be locked. If chkdsk
                               cannot lock the drive, a message appears that asks you if you
                               want to check the drive the next time you restart the computer.
----------------------------------------------------------------------------------------------------------
/v                             Displays the name of each file in every directory as the disk
                               is checked.
----------------------------------------------------------------------------------------------------------
/r                             Locates bad sectors and recovers readable information. The disk
                               must be locked. /r includes the functionality of /f, with the
                               additional analysis of physical disk errors.
----------------------------------------------------------------------------------------------------------
/x                             Forces the volume to dismount first, if necessary. All open
                               handles to the drive are invalidated. /x also includes the
                               functionality of /f.
----------------------------------------------------------------------------------------------------------
/i                             Use with NTFS only. Performs a less vigorous check of index
                               entries, which reduces the amount of time required to run chkdsk.
----------------------------------------------------------------------------------------------------------
/c                             Use with NTFS only. Does not check cycles within the folder
                               structure, which reduces the amount of time required to run chkdsk.
----------------------------------------------------------------------------------------------------------
/l[:<size>]                    Use with NTFS only. Changes the log file size to the size you
                               type. If you omit the size parameter, /l displays the current size.
----------------------------------------------------------------------------------------------------------
/b                             Use with NTFS only. Clears the list of bad clusters on the volume
                               and rescans all allocated and free clusters for errors.
                               /b includes the functionality of /r.
                               Use this parameter after imaging a volume to a new hard disk drive.
----------------------------------------------------------------------------------------------------------
/scan                          Use with NTFS only. Runs an online scan on the volume.
----------------------------------------------------------------------------------------------------------
/forceofflinefix               Use with NTFS only (must be used with /scan). Bypass all online
                               repair; all defects found are queued for offline repair (for example,
                               chkdsk /spotfix).
----------------------------------------------------------------------------------------------------------
/perf                          Use with NTFS only (must be used with /scan). Uses more system
                               resources to complete a scan as fast as possible. This may have a
                               negative performance impact on other tasks running on the system.
----------------------------------------------------------------------------------------------------------
/spotfix                       Use with NTFS only. Runs spot fixing on the volume.
----------------------------------------------------------------------------------------------------------
/sdcleanup                     Use with NTFS only. Garbage collect unneeded security descriptor data
                               (implies /f).
----------------------------------------------------------------------------------------------------------
/offlinescanandfix             Runs an offline scan and fix on the volume.
----------------------------------------------------------------------------------------------------------
/freeorphanedchains            Use with FAT/FAT32/exFAT only. Frees any orphaned cluster chains instead
                               of recovering their contents.
----------------------------------------------------------------------------------------------------------
/markclean                     Use with FAT/FAT32/exFAT only. Marks the volume clean if no corruption was
                               detected, even if /f was not specified.
----------------------------------------------------------------------------------------------------------
/?                             Displays help at the command prompt.
"""

ping_help_content = """
Parameter                      Description
==========================================================================================================
<target>                       Specifies the destination, which can be an IP address or a hostname.
                               Example: "example.com" or "192.168.1.1"
----------------------------------------------------------------------------------------------------------
-n <count>                     Specifies the number of echo requests to send. The default is 4.
                               Example: "-n 10"
----------------------------------------------------------------------------------------------------------
-l <size>                      Sends packets of a specified size. The default is 32 bytes.
                               Example: "-l 64"
----------------------------------------------------------------------------------------------------------
-f                             Sets the Don't Fragment flag in the packet (IPv4-only).
                               Prevents packets from being fragmented by routers.
----------------------------------------------------------------------------------------------------------
-i <TTL>                       Sets the Time To Live field in the packet header, indicating the maximum
                               number of hops the packet can traverse.
                               Example: "-i 128"
----------------------------------------------------------------------------------------------------------
-v <TOS>                       Specifies the Type of Service (IPv4-only). This parameter is deprecated
                               and has no effect on modern networks.
----------------------------------------------------------------------------------------------------------
-r <count>                     Records route for count hops (IPv4-only). The count must be between 1 and 9.
                               Example: "-r 5"
----------------------------------------------------------------------------------------------------------
-s <count>                     Timestamp for count hops (IPv4-only).
                               Example: "-s 4"
----------------------------------------------------------------------------------------------------------
-w <timeout>                   Waits for each reply within a specified timeout in milliseconds.
                               Example: "-w 1000" for a 1-second timeout.
----------------------------------------------------------------------------------------------------------
-t                             Pings the specified host until stopped. Use Ctrl+C to stop.
----------------------------------------------------------------------------------------------------------
-a                             Resolves addresses to hostnames.
----------------------------------------------------------------------------------------------------------
-4                             Forces ping to use IPv4.
----------------------------------------------------------------------------------------------------------
-6                             Forces ping to use IPv6.
----------------------------------------------------------------------------------------------------------
/?                             Displays help at the command prompt.
"""
# --- DISK INFO END ---
pass
# --- WIFI PASSWORDS ---
no_adapter_messages = [
    "There is no wireless interface on the system",  # English
    "Es gibt keine drahtlose Schnittstelle im System",  # German
    "Il n'y a pas d'interface sans fil sur le système",  # French
    "No hay interfaz inalámbrica en el sistema",  # Spanish
    "システムにワイヤレス インターフェイスがありません",  # Japanese
    "系统中没有无线接口",  # Chinese Simplified
    "系統中沒有無線介面",  # Chinese Traditional
    "시스템에 무선 인터페이스가 없습니다",  # Korean
    "Não há interface sem fio no sistema",  # Portuguese
    "Non c'è un'interfaccia wireless sul sistema",  # Italian
    "Er is geen draadloze interface op het systeem",  # Dutch
    "Det finns inget trådlöst gränssnitt på systemet",  # Swedish
    "Системе не имеет беспроводного интерфейса",  # Russian
    "Systemet har ingen trådløs grænseflade",  # Danish
    "Системата няма безжичен интерфейс",  # Bulgarian
    "Συστήματος δεν έχει ασύρματη διεπαφή",  # Greek
    "Sistemde kablosuz arabirim yok",  # Turkish
    "Nu există interfață wireless pe sistem",  # Romanian
    "Nincs vezeték nélküli interfész a rendszeren",  # Hungarian
    "Systém nemá bezdrátové rozhraní",  # Czech
    "System nie ma interfejsu bezprzewodowego",  # Polish
    "Systemet har ingen trådløst grensesnitt",  # Norwegian
    "Järjestelmässä ei ole langatonta liitäntää",  # Finnish
    "Nav bezvadu interfeisa sistēmā",  # Latvian
    "Süsteemis pole juhtmevaba liidest",  # Estonian
    "Sistemoje nėra belaidžio tinklo sąsajos",  # Lithuanian
    "Không có giao diện không dây trên hệ thống",  # Vietnamese
    "ระบบไม่มีอินเทอร์เฟซไร้สาย",  # Thai
    "Sistem tidak memiliki antarmuka nirkabel",  # Indonesian
    "Walang wireless interface sa system",  # Filipino
    "سیستم هیچ رابط بی‌سیمی ندارد",  # Persian
    "لا يوجد واجهة لاسلكية على النظام",  # Arabic
    "אין ממשק אלחוטי במערכת"  # Hebrew
]

profile_headers = [
    r"Profile\s*[:：]",  # English
    r"Profil\s*[:：]",  # German/French
    r"Perfil\s*[:：]",  # Spanish/Portuguese
    r"プロファイル\s*[:：]",  # Japanese
    r"配置文件\s*[:：]",  # Chinese Simplified
    r"設定檔案\s*[:：]",  # Chinese Traditional
    r"프로파일\s*[:：]",  # Korean
    r"Profilo\s*[:：]",  # Italian
    r"Profiel\s*[:：]",  # Dutch
    r"Profil\s*[:：]",  # Swedish/Danish/Norwegian
    r"Профиль\s*[:：]",  # Russian
    r"Προφίλ\s*[:：]",  # Greek
    r"Profil\s*[:：]",  # Turkish
    r"Profil\s*[:：]",  # Romanian
    r"Profil\s*[:：]",  # Hungarian
    r"Profil\s*[:：]",  # Czech
    r"Profil\s*[:：]",  # Polish
    r"Profiili\s*[:：]",  # Finnish
    r"Profils\s*[:：]",  # Latvian
    r"Profiil\s*[:：]",  # Estonian
    r"Profilis\s*[:：]",  # Lithuanian
    r"Hồ sơ\s*[:：]",  # Vietnamese
    r"โปรไฟล์\s*[:：]",  # Thai
    r"Profil\s*[:：]",  # Indonesian
    r"Profile\s*[:：]",  # Filipino
    r"پروفایل\s*[:：]",  # Persian
    r"ملف التعريف\s*[:：]",  # Arabic
    r"פרופיל\s*[:：]",  # Hebrew
    r"Perfíl\s*[:：]",  # Galician
    r"Profilis\s*[:：]",  # Lithuanian
    r"Profilis\s*[:：]",  # Latvian
    r"Profiil\s*[:：]",  # Estonian
    r"Profil\s*[:：]",  # Croatian
    r"Профіль\s*[:：]",  # Ukrainian
    r"Профил\s*[:：]",  # Bulgarian
    r"Prófíll\s*[:：]",  # Icelandic
    r"Profiel\s*[:：]",  # Afrikaans
    r"Próifíl\s*[:：]",  # Irish
    r"Proffil\s*[:：]",  # Welsh
    r"Profilo\s*[:：]",  # Maltese
    r"Profil\s*[:：]",  # Albanian
    r"Профил\s*[:：]",  # Macedonian
    r"Профил\s*[:：]",  # Serbian
    r"Profil\s*[:：]"   # Slovak
]
# --- WIFI PASSWORDS END ---
