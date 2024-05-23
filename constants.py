# Version of the app
VERSION = "Use at your own risk and responsibility - v1.342"

# GitHub repo link
LINK = "https://github.com/df8819/WinFunct"

# The curl-command to copy to the clipboard
command = 'curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s ' \
          '-- -v'

# List of non-essential apps to uninstall
apps_to_uninstall = [
    "Microsoft.SkypeApp",
    "Microsoft.Todos",
    "Microsoft.Microsoft3DViewer",
    "Microsoft.Messaging",
    "Microsoft.Office.Sway",
    "Microsoft.OneConnect",
    "Microsoft.People",
    "Microsoft.Print3D",
    "Microsoft.GetHelp",
    "Microsoft.Getstarted",
    "Microsoft.BingWeather",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.XboxSpeechToTextOverlay",
    "Microsoft.YourPhone",
    "Microsoft.ZuneMusic",
    "Microsoft.ZuneVideo",
    "Microsoft.MinecraftUWP",
    "Microsoft.BingNews",
    "Microsoft.BingFinance",
    "Microsoft.BingSports",
    "Microsoft.BingTravel",
    "Microsoft.BingHealthAndFitness",
    "Microsoft.BingFoodAndDrink",
    "Microsoft.BingDictionary",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.Office.SkypeforBusiness",
    "Microsoft.Windows.CommunicationApps",
    "Microsoft.Windows.MixedReality",
    "Microsoft.Xbox.TCUI"
]

# List of unnecessary PWA shortcuts to unregister
pwas_to_unregister = [
    "Microsoft.TikTok",
    "Microsoft.CandyCrushSaga",
    "Microsoft.Office.Online",
    "Microsoft.StorePurchaseApp",
    "Microsoft.XboxConsoleCompanion",
    "Microsoft.WindowsMaps",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.SkypeApp",
    "Microsoft.OneNote",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.3DViewer",
    "Microsoft.Office.Sway",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.GetHelp",
    "Microsoft.GrooveMusic",
    "Microsoft.MinecraftEducationEdition",
    # Add other unnecessary PWA shortcuts here
]

links = {
    "Dev Tools": {
        "Python": "https://www.python.org/downloads/",
        "Git": "https://git-scm.com/downloads",
        "GitHub Desktop": "https://desktop.github.com",
        "Visual Studio": "https://code.visualstudio.com/download",
        "PyCharm": "https://www.jetbrains.com/pycharm/download/?section=windows",
        "UPX": "https://github.com/upx/upx/releases",
        "AirCrack": "https://www.aircrack-ng.org",
        "Wifi-Cracker": "https://github.com/trevatk/Wifi-Cracker",
        "Rust/Cargo": "https://rustup.rs",
        "Rufus": "https://rufus.ie/en/",
        "SoapUI": "https://www.soapui.org/downloads/soapui/",
        "Win X Server": "https://sourceforge.net/projects/vcxsrv/",
        "HxD": "https://mh-nexus.de/de/downloads.php?product=HxD20",
        "Process Explorer": "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer",
        "TCPView": "https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview",
    },

    "Utilities": {
        "TeamViewer": "https://www.teamviewer.com/de/download/windows/",
        "RustDesk": "https://github.com/rustdesk/rustdesk/releases/tag/1.2.3",
        "MS PowerToys": "https://github.com/microsoft/PowerToys/releases/tag/v0.75.1",
        "PicPick": "https://picpick.app/en/download/",
        "HWInfo64": "https://www.hwinfo.com/download/",
        "MSI Afterburner": "https://www.msi.com/Landing/afterburner/graphics-cards",
        "WinDirStat": "https://sourceforge.net/projects/windirstat/",
        "Advanced IP Scanner": "https://www.advanced-ip-scanner.com/de/",
        "Raspberry Pi Imager": "https://www.raspberrypi.com/software/",
        "PuTTY (SSH)": "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html",
        "Notepad++": "https://notepad-plus-plus.org/downloads/v8.5.8/",
        "Partition Manager": "https://www.paragon-software.com/free/pm-express/#features",
        "Win10 Creation Tool": "https://www.microsoft.com/de-de/software-download/windows10",
        "WireShark": "https://www.wireshark.org/download.html",
        "Total Commander": "https://www.ghisler.com/ddownload.htm",
    },

    "Tutorials": {
        "MAS/IDM Script": "https://massgrave.dev/index.html",
        "AdGuard Home": "https://youtu.be/B2V_8M9cjYw?si=Z_AeA4hCFGiElOHB",
        "NSE Lab": "https://nse.digital",
        "Wifi-Hack": "https://hackernoon.com/how-to-hack-wifi-like-a-pro-hacker",
    },
    # Add more categories and items as needed
}

windows_management_options = [
    ("RegEdit", "regedit"),
    ("PC Mgr", "compmgmt.msc"),
    ("Event Vwr", "eventvwr.msc"),
    ("Services", "services.msc"),
    ("Group Policy", "gpedit.msc"),
    ("Programs", "appwiz.cpl"),
    ("Win Ver.", "winver"),
    ("Adv. Sys Set.", "SystemPropertiesAdvanced"),
    ("User Acc Ctrl", "useraccountcontrolsettings"),
    ("Disk Mgr", "diskmgmt.msc"),
    ("Local Users", "lusrmgr.msc"),
    ("Sys Prop Name", "SystemPropertiesComputerName"),
    ("ODBC Sources", "odbcad32"),
    ("PrintMgmt", "printmanagement.msc"),
    ("Shared Folders", "fsmgmt.msc"),
    ("Mobility Ctr", "mblctr"),
]

# Security and Networking Tools
security_and_networking_options = [
    ("Sec. Center", "start ms-settings:windowsdefender"),
    ("Sec. Policy", "secpol.msc"),
    ("FW Advanced", "wf.msc"),
    ("Net. Sharing", "control /name Microsoft.NetworkAndSharingCenter"),
    ("Internet Opt.", "inetcpl.cpl"),
    ("Cred. Mgr", "control /name Microsoft.CredentialManager"),
    ("Firewall", "firewall.cpl"),
    ("Net. Adapt.", "ncpa.cpl"),
    ("DNS Cache", "ipconfig /displaydns"),
    ("Remote Conn", "control /name Microsoft.RemoteAppAndDesktopConnections"),
    ("VPN Set.", "start ms-settings:network-vpn"),
    ("Wi-Fi Set.", "start ms-settings:network-wifi"),
    ("Ethernet Set.", "start ms-settings:network-ethernet"),
    ("Dial-up Set.", "start ms-settings:network-dialup"),
    ("Proxy Set.", "start ms-settings:network-proxy"),
]

# System Tools and Utilities
system_tools_options = [
    ("Hosts File", "notepad C:\\Windows\\System32\\drivers\\etc\\hosts"),
    ("Task Mgr", "taskmgr"),
    ("Ctrl Panel", "control"),
    ("Device Mgr", "devmgmt.msc"),
    ("Perf Mon.", "perfmon"),
    ("Res. Mon.", "resmon"),
    ("Dev. Pairing", "devicepairingwizard"),
    ("Win Features", "optionalfeatures"),
    ("Sys Info", "msinfo32"),
]

# Remote Management and Virtualization Tools
remote_and_virtualization_options = [
    ("RDP", "mstsc"),
    ("Hyper-V Mgr", "virtmgmt.msc"),
    ("Env. Var.", "rundll32.exe sysdm.cpl,EditEnvironmentVariables"),
    ("RDP Set", "start ms-settings:remotedesktop"),
    ("Remote Assist", "msra"),
]

# Troubleshooting and Optimization Tools
troubleshooting_and_optimization_options = [
    ("RelMon", "perfmon /rel"),
    ("Disk Cleanup", "cleanmgr"),
    ("Sys Restore", "rstrui"),
    ("Troubleshoot", "msdt"),
    ("Opt Drives", "dfrgui"),
    ("Mem Diag", "MdSched"),
    ("DirectX Diag", "dxdiag"),
    ("Sys Config", "msconfig"),
    ("Win Update", "start ms-settings:windowsupdate"),
    ("Update Hist", "start ms-settings:windowsupdate-history"),
    ("Update Opt", "start ms-settings:windowsupdate-options"),
]

netsh_commands = [
    ("IP Config", "netsh interface ip show config"),
    ("Interf.", "netsh interface show interface"),
    ("IPv4 Interf.", "netsh interface ipv4 show interface"),
    ("IPv6 Interf.", "netsh interface ipv6 show interface"),
    ("IP Addr.", "netsh interface ip show addresses"),
    ("DNS Servers", "netsh interface ip show dns"),
    ("FW State", "netsh advfirewall show currentprofile state"),
    ("FW Config", "netsh advfirewall firewall show rule name=all"),
    ("Rout. Table", "netsh interface ipv4 show route"),
    ("Wirel. Prof.", "netsh wlan show profiles"),
    ("Wirel. Set.", "netsh wlan show settings"),
    ("Wirel. Netw.", "netsh wlan show networks"),
    ("Netw. Stats", "netstat -s"),
]
