# Standard Library Imports
import csv
import ctypes
import hashlib
import logging
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time
from urllib.parse import urlparse

# Tkinter Imports
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import webbrowser
import winreg
# import ttkbootstrap as ttk
# from ttkbootstrap import Style

# Third-Party Imports
import requests
import wmi

# Local Imports
from HashStuffInt import HashStuff
from JChatInt import JChat
from SimplePWGenInt import SimplePWGen
from DonutInt import Donut
from ColorPickerInt import SimpleColorPicker

# Define the version once
VERSION_NUMBER = "1.647"

# Use the version number in different strings
VERSION = f"Use at your own risk and responsibility - v{VERSION_NUMBER}"
VERSION_SHORT = f"v{VERSION_NUMBER}"

UI_COLOR = "#f3f3f3"
BOTTOM_BORDER_COLOR = "#42a88c"  # Nice "Windows" blue #4791CC

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


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        log_message(f"Error checking admin status: {e}")
        return False


def log_message(message):
    with open("admin_log.txt", "a") as log_file:
        log_file.write(message + "\n")


def run_as_admin():
    if sys.platform == "win32":
        cmd = [sys.executable] + sys.argv
        cmd_line = ' '.join('"' + item.replace('"', '\\"') + '"' for item in cmd)
        try:
            log_message("Script is not running with admin rights. Trying to obtain them...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd_line, None, 1)
            sys.exit()  # Exit after trying to elevate privileges
        except Exception as e:
            log_message(f"Error re-running the script with admin rights: {e}")
    else:
        log_message("Current platform is not Windows, skipping admin check.")


def is_running_in_ide():
    # This function checks for common IDE-specific variables
    return any(ide_env in os.environ for ide_env in ["PYCHARM_HOSTED", "VSCode"])


def print_log():
    log_path = "admin_log.txt"
    if os.path.exists(log_path):
        with open(log_path, "r") as log_file:
            print(log_file.read())
        os.remove(log_path)


if __name__ == "__main__":
    # Bypass admin check if running in an IDE
    if not is_running_in_ide():
        if not is_admin():
            run_as_admin()
            # The script will exit here if not running as admin

    # Print log messages in the elevated terminal
    print_log()


def show_logo():
    print("""
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
""")


show_logo()

print(f"{VERSION_SHORT} >>> Now running with admin rights. Nice (⌐■_■)")


# Command functions
def execute_command(cmd):
    print(f"Executing: {cmd}")
    subprocess.Popen(cmd, shell=True)


# App Window
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resolution_main = "765x480"
        self.tabs = None
        self.checkbox_vars = None
        self.fun_frame = None
        self.options_frame = None
        self.create_user = None
        self.ip_text = None
        self.functions_frame = None
        self.bottom_frame = None
        self.geometry(self.resolution_main)
        self.title("Windows Functionalities (ﾉ◕◡◕)ﾉ*:･ﾟ✧")
        self.font_family = "Segoe UI Emoji"

        # Create a style for the main_frame background color
        style = ttk.Style()
        style.configure('Main.TFrame', background=f'{BOTTOM_BORDER_COLOR}')

        # Apply the style to the main_frame
        self.main_frame = ttk.Frame(self, style='Main.TFrame')

        # Remove padding if unnecessary or adjust as needed
        self.main_frame.pack(fill="both", expand=True)  # No padding here

        self.create_widgets()
        self.resizable(True, True)

        # Center the window after all widgets have been packed
        self.after(100, self.center_window)

    def center_window(self):
        # Using Tcl method to center
        self.eval('tk::PlaceWindow . center')

    def reset_ui(self):
        print("""UI reset.""")
        self.geometry(self.resolution_main)
        self.after(100, self.center_window)

    def open_chat(self):
        print("""Open JChat app.""")
        if tk.messagebox.askyesno("Open JChat",
                                  "This will open a chat-app GUI that requires an OpenAI API Key.\n\nSelect 'No' if you don't have your personal Key yet."):
            chat_window = tk.Toplevel(self)
            chat_window.title("JChat")
            JChat(chat_window)

    def open_pw_gen(self):
        print("""Open Password Generator app.""")
        pw_window = tk.Toplevel(self)
        pw_window.title("Password Generator")
        pw_window.attributes('-topmost', True)
        SimplePWGen(pw_window)

    def open_hash_stuff(self):
        print("""Open Hash Generator app.""")
        hash_window = tk.Toplevel(self)
        hash_window.title("Hash Generator")
        hash_window.attributes('-topmost', True)
        HashStuff(hash_window)

    def open_color_picker(self):
        print("""Open Color Picker app.""")
        color_picker_window = tk.Toplevel(self)
        color_picker_window.title("Color Picker")
        color_picker_window.attributes('-topmost', True)
        SimpleColorPicker(color_picker_window)

    def open_donut(self):
        print("""Open funny cmd ASCII Donut.""")
        donut = Donut()
        if sys.platform == 'win32':
            subprocess.Popen(['start', 'python', '-c', 'from DonutInt import Donut; Donut().run()'], shell=True)
        else:
            subprocess.Popen(['python', '-c', 'from DonutInt import Donut; Donut().run()'])

    def show_logo(self):
        show_logo()

    def open_app_root_folder(self):
        print("""Open root folder location.""")
        # Determine the directory of the executable or the script itself
        if getattr(sys, 'frozen', False):
            app_root = os.path.dirname(sys.executable)
        else:
            app_root = os.path.dirname(os.path.abspath(__file__))

        # Open the directory using the platform-specific command
        if sys.platform == 'win32':
            subprocess.Popen(f'explorer "{app_root}"')
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', app_root])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(['xdg-open', app_root])

    def open_ps_as_admin(self):
        print("""Open PowerShell window as admin.""")
        def run_command():
            try:
                subprocess.run('powershell Start-Process powershell -Verb runAs', shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PowerShell as admin: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def open_cmd_as_admin(self):
        print("""Open cmd window as admin.""")
        def run_command():
            try:
                subprocess.run('start cmd.exe /k cd C:\\ & title Command Prompt as Admin', shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Command Prompt as admin: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def open_autostart_locations(self):
        print("""Open Windows Auto-Start folders.""")
        # Folder locations
        user_startup_path = os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        all_users_startup_path = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp'

        # Open folder locations
        if os.path.exists(user_startup_path):
            os.startfile(user_startup_path)
        if os.path.exists(all_users_startup_path):
            os.startfile(all_users_startup_path)

    def show_ip_address(self):
        print("""Temporary showing IP address""")
        response = requests.get("https://ifconfig.me/ip")
        ip_address = response.text
        self.ip_text.delete(0, tk.END)
        self.ip_text.insert(tk.END, ip_address)

        # Schedule the removal of the IP address
        self.ip_text.after(3000, self.clear_ip_text)

    def clear_ip_text(self):
        self.ip_text.delete(0, tk.END)

    def show_wifi_networks(self):
        print("""Extracting Wifi profiles and passwords.""")
        try:
            cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], stderr=subprocess.STDOUT).decode("utf-8", "ignore")
            networks = re.findall(r"All User Profile\s*:\s*(.+)", cmd_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute netsh command: {e.output.decode('utf-8', 'ignore')}")
            return

        if networks:
            network_window = tk.Toplevel(self)
            network_window.title("Wi-Fi Networks")

            window_width = 420
            window_height = 380
            screen_width = network_window.winfo_screenwidth()
            screen_height = network_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            network_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            network_window.resizable(False, False)

            label_text = "Select a Wi-Fi Network from the list below to copy its password:"
            label = tk.Label(network_window, text=label_text)
            label.pack(pady=10)

            list_frame = tk.Frame(network_window)
            list_frame.pack(padx=10, pady=10, fill="both", expand=True)

            scrollbar = tk.Scrollbar(list_frame, orient="vertical")
            network_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, exportselection=False)

            scrollbar.config(command=network_listbox.yview)
            scrollbar.pack(side="right", fill="y")
            network_listbox.pack(side="left", fill="both", expand=True)

            for network in networks:
                network_listbox.insert(tk.END, network.strip())

            def ok_button_click():
                selected_index = network_listbox.curselection()
                if selected_index:
                    selected_network = network_listbox.get(selected_index[0])
                    self.show_wifi_password(selected_network)
                network_window.destroy()

            ok_button = ttk.Button(network_window, text="Ok", command=ok_button_click, width=10)
            ok_button.pack(side="left", padx=(50, 5), pady=10)

            def cancel_button_click():
                network_window.destroy()

            cancel_button = ttk.Button(network_window, text="Cancel", command=cancel_button_click, width=10)
            cancel_button.pack(side="right", padx=(5, 50), pady=10)
        else:
            tk.messagebox.showinfo("Wi-Fi Networks", "No Wi-Fi networks found.")

    def show_wifi_password(self, network):
        network = network.strip()
        try:
            cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network, "key=clear"],
                                                 stderr=subprocess.STDOUT).decode("utf-8", "ignore")
            password = re.search(r"Key Content\s*:\s*(.+)", cmd_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error",
                                 f"Failed to execute netsh command for network '{network}': {e.output.decode('utf-8', 'ignore')}")
            return

        if password:
            password_window = tk.Toplevel(self)
            password_window.title(f"Password for {network}")

            window_width = 320
            window_height = 120
            screen_width = password_window.winfo_screenwidth()
            screen_height = password_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            password_window.resizable(False, False)

            password_frame = tk.Frame(password_window)
            password_frame.pack(padx=20, pady=20)

            password_label = tk.Label(password_frame, text="Password:")
            password_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

            password_text = tk.Entry(password_frame, width=30)
            password_text.insert(0, password.group(1))
            password_text.grid(row=0, column=1, padx=5, pady=5)
            password_text.config(state="readonly")

            def copy_password():
                self.clipboard_clear()
                self.clipboard_append(password_text.get())
                self.update()

            button_frame = tk.Frame(password_frame)
            button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

            copy_button = ttk.Button(button_frame, text="Copy Password", command=copy_password)
            copy_button.pack(side="left", padx=10)

            def cancel_button_click():
                password_window.destroy()

            cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_button_click)
            cancel_button.pack(side="left", padx=10)
        else:
            messagebox.showinfo(f"Wi-Fi Password for {network}", "No password found.")

    def run_winsat_disk(self):
        print("""Running Disk speed test.""")
        def get_available_drives():
            drives = []
            for partition in psutil.disk_partitions(all=False):
                if partition.device and partition.device[0].isalpha():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        drives.append(f"{partition.device[0]}: ({usage.total / (1024 ** 3):.2f} GB)")
                    except Exception:
                        # Skip drives that can't be accessed
                        pass
            return drives

        def on_run():
            selected_drive = drive_combobox.get()

            if selected_drive == "Select a drive":
                messagebox.showwarning("No Drive Selected", "Please select a drive from the dropdown menu.")
                return

            drive_letter = selected_drive[0]  # Extract the drive letter from the selected option

            try:
                powershell_command = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/c winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
                subprocess.Popen(powershell_command, shell=True)
                top.destroy()  # Close the drive selection window
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while trying to run the WinSAT disk test: {str(e)}")

        # Create a top-level window for drive selection
        top = tk.Tk()
        top.title("WinSAT Disk Performance Test")
        top.geometry("380x130")

        # Center the window on the screen
        top.update_idletasks()  # Update "requested size" from geometry manager
        width = top.winfo_width()
        height = top.winfo_height()
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        top.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Create and pack a label
        label = ttk.Label(top, text="Select a drive to test:", padding=(10, 10))
        label.pack()

        # Create and pack the combobox for drive selection
        drive_combobox = ttk.Combobox(top, values=get_available_drives(), state="readonly", width=50)
        drive_combobox.pack(pady=10)
        drive_combobox.set("Select a drive")

        # Create and pack the run button
        run_button = ttk.Button(top, text="Run WinSAT Disk Test", command=on_run)
        run_button.pack(pady=10)

        # Start the Tkinter event loop
        top.mainloop()

    def run_website_checker(self):
        def on_run():
            website_url = self.website_entry.get().strip()

            # 1. Improved Input Validation
            if not website_url:
                messagebox.showwarning("No URL Provided", "Please enter a website URL.")
                return

            # Simple regex for URL validation
            url_pattern = re.compile(
                r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?'
                r'[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}'
                r'(:[0-9]{1,5})?(\/.*)?$'
            )
            if not url_pattern.match(website_url):
                messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
                return

            # Ensure the URL starts with http:// or https://
            website_url = 'https://' + website_url if not website_url.startswith(('http://', 'https://')) else website_url

            try:
                # Create a batch script for checking and monitoring
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bat') as temp_file:
                    check_website_script = temp_file.name

                    batch_script = f"""
@echo off
setlocal enabledelayedexpansion

set website={website_url}

:check
for /f "tokens=*" %%a in ('curl -Is !website! -o nul -w "%%{{http_code}} %%{{time_total}} %%{{remote_ip}}"') do (
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
) else if !status_code! equ 301 (
    echo Website is         ONLINE but -Moved Permanently-
) else if !status_code! equ 302 (
    echo Website is         ONLINE but -Temporary Redirect-
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
) else if !status_code! equ 500 (
    echo Website is         ONLINE but -Internal Server Error-
) else if !status_code! equ 503 (
    echo Website is         ONLINE but -Service Unavailable-
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
) else if !status_code! equ 301 (
    pause
    exit /b 0
) else if !status_code! equ 302 (
    pause
    exit /b 0
) else if !status_code! equ 307 (
    pause
    exit /b 0
) else if !status_code! equ 308 (
    pause
    exit /b 0
) else if !status_code! equ 400 (
    pause
    exit /b 0
) else if !status_code! equ 401 (
    pause
    exit /b 0
) else if !status_code! equ 403 (
    pause
    exit /b 0
) else if !status_code! equ 404 (
    pause
    exit /b 0
) else if !status_code! equ 500 (
    pause
    exit /b 0
) else if !status_code! equ 503 (
    pause
    exit /b 0
) else (
    echo Checking again in 60 seconds...
    timeout /t 60 >nul
    goto check
)
    """
                    temp_file.write(batch_script)

                # Execute the batch file in a new window
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/c', check_website_script], shell=True)

                # Schedule file deletion after 1 second
                self.top.after(1000, lambda: os.unlink(check_website_script))

                self.top.destroy()  # Close the input window

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Create a top-level window for the website URL input
        self.top = tk.Toplevel(self.master)
        self.top.title("Website Online State Checker")
        self.top.geometry("400x130")
        self.top.resizable(False, False)

        # Center the window on the screen
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Create and pack a label
        label = ttk.Label(self.top, text="Enter the website URL/IP to check (e.g., example.com):", padding=(10, 10))
        label.pack()

        # Create and pack the entry field for the website URL
        self.website_entry = ttk.Entry(self.top, width=50)
        self.website_entry.pack(pady=10)
        self.website_entry.focus_set()

        # Create and pack the run button
        run_button = ttk.Button(self.top, text="Check Website", command=on_run)
        run_button.pack(pady=10)

    def activate_win(self):
        user_response = messagebox.askyesno("Activate Microsoft Products",
                                            "This will open a PowerShell instance and run the MAS User Interface. Proceed?")
        if user_response:
            def run_command():
                command = ['powershell.exe', '-Command', 'irm https://get.activated.win | iex']
                subprocess.run(command, shell=True)

            # Run the command in a separate thread to avoid freezing the UI
            thread = threading.Thread(target=run_command)
            thread.start()
        else:
            print(f"\nCommand was cancelled.")

    def activate_wui(self):
        user_response = messagebox.askyesno("Open Windows Utility Improved",
                                            "This will open a PowerShell instance run Chris Titus Tech Windows Utility. Proceed?")
        if user_response:
            def run_command():
                command = ['powershell.exe', '-Command', 'irm christitus.com/win | iex']
                subprocess.run(command, shell=True)

            # Run the command in a separate thread to avoid freezing the UI
            thread = threading.Thread(target=run_command)
            thread.start()
        else:
            print(f"Command was cancelled.")

    def install_ffmpeg(self):
        user_response = messagebox.askyesno("Install FFMPEG",
                                            "This will open a PowerShell instance and run a FFMPEG install script. Proceed?")
        if user_response:
            def run_command():
                command = ['powershell.exe', '-Command', 'iex (irm ffmpeg.tc.ht)']
                subprocess.run(command, shell=True)

            # Run the command in a separate thread to avoid freezing the UI
            thread = threading.Thread(target=run_command)
            thread.start()
        else:
            print(f"\nCommand was cancelled.")

    def shutdown_i(self):
        print("""Opening Remote Shutdown Dialog.""")
        subprocess.run("shutdown -i", shell=True)

    def confirm_shutdown(self):
        # if tk.messagebox.askyesno("Shutdown", "Are you sure you want to shut down your PC?"):
        os.system("shutdown /s /t 1")

    def confirm_reboot(self):
        # if tk.messagebox.askyesno("Reboot", "Are you sure you want to reboot your PC?"):
        os.system("shutdown /r /t 1")

    def confirm_sleep(self):
        # if tk.messagebox.askyesno("Hibernate", "Are you sure you want to hibernate your PC?"):
        os.system("shutdown /h")

    def confirm_uefi(self):
        # if tk.messagebox.askyesno("UEFI Boot", "Are you sure you want to reboot directly into BIOS/UEFI?"):
        os.system("shutdown /r /fw /t 1")

    def run_powershell_command(self, command, return_output=False):
        with open("powershell_log.txt", "a") as log_file:
            log_file.write(f"Executing command: {command}\n")

            process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            stdout, stderr = process.communicate()

            # Log the output and any errors
            log_file.write("Standard Output:\n" + stdout)
            log_file.write("Standard Error:\n" + stderr)

            if return_output:
                return stdout, stderr

            return stderr == ""

    def uninstall_package(self, package_name, results):
        success = self.run_powershell_command(f"Get-AppxPackage {package_name} | Remove-AppxPackage")
        results[f"Removing {package_name}"] = "Succeeded" if success else "Failed"

    def uninstall_pwa(self, display_name, results):
        # Use Get-AppxPackage to find the full package name
        find_package_cmd = f"Get-AppxPackage -Name '*{display_name}*'"  # Added wildcard for better matching
        stdout, stderr = self.run_powershell_command(find_package_cmd, return_output=True)

        if stderr:
            # Log the error if the package can't be found
            results[f"Finding {display_name}"] = f"Failed: Package not found or other error. {stderr.strip()}"
            return

        # Parse the stdout to find the full package name (assuming the package is found)
        package_full_name = None
        for line in stdout.split('\n'):
            if "PackageFullName" in line:
                package_full_name = line.split(":")[-1].strip()
                break

        if package_full_name:
            # Now that we have the full package name, attempt to remove it
            remove_package_cmd = f"Remove-AppxPackage '{package_full_name}'"  # Removed '-Package' for correctness
            stdout, stderr = self.run_powershell_command(remove_package_cmd, return_output=True)

            # Log the results of the removal command
            result_text = f"Removing PWA {package_full_name}"  # Added 'PWA' for clarity
            results[result_text] = "Succeeded" if stderr == "" else f"Failed: {stderr.strip()}"
        else:
            results[f"Finding {display_name}"] = "Failed: Full package name not found in the output."

    def run_script_async(self, app_list, pwa_list):
        thread = threading.Thread(target=self.handle_uninstall, args=(app_list, pwa_list), daemon=True)
        thread.start()

    def handle_uninstall(self, app_list, pwa_list):
        uninstall_results = {}
        for app in app_list:
            stdout, stderr = self.run_powershell_command(f"Get-AppxPackage {app} | Remove-AppxPackage", return_output=True)
            uninstall_results[f"Removing {app}"] = "Succeeded" if stderr == "" else f"Failed: {stderr.strip()}"

        for pwa_display_name in pwa_list:
            # Search for the PWA by display name to get its details
            find_package_cmd = f"Get-AppxPackage -Name '*{pwa_display_name}*'"
            stdout, stderr = self.run_powershell_command(find_package_cmd, return_output=True)

            if stderr:
                # If there's an error, the package might not exist; log this case
                uninstall_results[
                    f"Finding {pwa_display_name}"] = f"Failed: Package not found or other error. {stderr.strip()}"
                continue

            # Parse stdout to find the full package name
            package_full_name = None
            for line in stdout.split('\n'):
                if "PackageFullName" in line:
                    package_full_name = line.split(":")[-1].strip()
                    break

            if package_full_name:
                # Use the derived full package name to uninstall the PWA
                remove_package_cmd = f"Remove-AppxPackage '{package_full_name}'"
                stdout, stderr = self.run_powershell_command(remove_package_cmd, return_output=True)
                result_text = f"Removing PWA {package_full_name}"
                uninstall_results[result_text] = "Succeeded" if stderr == "" else f"Failed: {stderr.strip()}"
            else:
                # This case may happen if the PWA was listed but not installed for the current user
                uninstall_results[f"Finding {pwa_display_name}"] = "Failed: Full package name not found in the output."

        self.on_script_complete(uninstall_results)

    def on_script_complete(self, uninstall_results):
        result_message = "The uninstallation process has completed. Here are the results:\n\n"
        for app, result in uninstall_results.items():
            result_message += f"{app}: {result}\n"

        messagebox.showinfo("Uninstall Completed", result_message)

    def renew_ip_config(self):
        if messagebox.askyesno("Renew IP Configuration",
                               "Are you sure you want to release/renew the IP config and flush DNS?"):
            def run_command():
                commands = [
                    ("ipconfig /release", "Releasing IP configuration..."),
                    ("ipconfig /flushdns", "Flushing DNS..."),
                    ("ipconfig /renew", "Renewing IP configuration...")
                ]

                for cmd, description in commands:
                    print(f"\n{'-' * 10} {description} {'-' * 10}")
                    full_cmd = f"cmd.exe /c {cmd}"
                    print(f"Executing command: {full_cmd}")
                    subprocess.run(full_cmd, shell=True)
                    print(f"Finished command: {cmd}")

                print(f"\n{'-' * 10} All commands completed {'-' * 10}")

            # Run the command in a separate thread to avoid freezing the UI
            thread = threading.Thread(target=run_command)
            thread.start()
        else:
            print(f"Command was cancelled.")

    def agh_curl(self):
        print("""Executing 'AdGuard Home' install helper.""")
        def on_link_click(event):
            webbrowser.open("https://github.com/AdguardTeam/AdGuardHome")

        def on_yes():
            AdGuardClipBoard = "curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v"
            subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(input=AdGuardClipBoard.encode())
            print("Command copied to clipboard")
            root.destroy()

        def on_no():
            print("Command execution canceled.")
            root.destroy()

        root = tk.Tk()
        root.title("Copy to Clipboard?")
        root.geometry("380x230")
        root.eval('tk::PlaceWindow . center')  # Center the window on the screen

        message = tk.Label(root, text=f"This will copy the curl-command:\n\ncurl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v\n\n to your clipboard to assist in setting up AdGuard Home on a device like a Raspberry. Proceed?", wraplength=280)
        message.pack(pady=10)

        link = tk.Label(root, text="AdGuard Home GitHub Repository", fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", on_link_click)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
        yes_button.pack(side=tk.LEFT, padx=5, pady=5)

        no_button = tk.Button(button_frame, text="No", command=on_no)
        no_button.pack(side=tk.LEFT, padx=5, pady=5)

        root.mainloop()

    def get_file_checksum(self):
        print("""Running file checksum helper.""")
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showinfo("Info", "No file selected.")
            return

        # Create a new window for algorithm selection
        algo_window = tk.Toplevel(self)
        algo_window.title("Compute File Checksum")
        algo_window.geometry("400x250")

        # Center the window
        algo_window.update_idletasks()
        width = algo_window.winfo_width()
        height = algo_window.winfo_height()
        x = (algo_window.winfo_screenwidth() // 2) - (width // 2)
        y = (algo_window.winfo_screenheight() // 2) - (height // 2)
        algo_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Create and pack a label
        label = ttk.Label(algo_window, text="Choose a checksum algorithm:")
        label.pack(pady=10)

        # Create a variable to hold the selected algorithm
        selected_algo = tk.StringVar()

        # Create a combobox for algorithm selection
        algorithms = ["MD5", "SHA1", "SHA256", "SHA384", "SHA512"]
        algo_combo = ttk.Combobox(algo_window, textvariable=selected_algo, values=algorithms, state="readonly")
        algo_combo.set("SHA256")  # Default value
        algo_combo.pack(pady=10)

        # Create a label to display the selected algorithm
        algo_label = ttk.Label(algo_window, text="")
        algo_label.pack(pady=5)

        # Create a ScrolledText widget to display the result
        result_text = scrolledtext.ScrolledText(algo_window, height=3, width=50, wrap=tk.WORD)
        result_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)
        result_text.config(state=tk.DISABLED)  # Make it read-only initially

        def run_checksum():
            algo = selected_algo.get()
            cmd = f'certutil -hashfile "{file_path}" {algo}'

            try:
                # Run the command and capture the output
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

                # Extract the checksum from the output
                checksum = result.stdout.split('\n')[1].strip()

                # Update the algorithm label
                algo_label.config(text=f"Selected algorithm: {algo}")

                # Display only the checksum in the text widget
                result_text.config(state=tk.NORMAL)
                result_text.delete('1.0', tk.END)
                result_text.insert(tk.END, checksum)
                result_text.config(state=tk.DISABLED)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"An error occurred while computing the checksum:\n{e.stderr}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

        # Create and pack a button
        button = ttk.Button(algo_window, text="Compute Checksum", command=run_checksum)
        button.pack(pady=10)

        # Make the window modal
        algo_window.transient(self)
        algo_window.grab_set()
        self.wait_window(algo_window)

    def get_installed_software(self):
        software_list = []
        logging.basicConfig(level=logging.INFO)

        def get_software_from_key(key, flag):
            try:
                access_flag = winreg.KEY_READ | flag
                with winreg.OpenKey(key, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, access_flag) as reg_key:
                    for i in range(winreg.QueryInfoKey(reg_key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(reg_key, i)
                            with winreg.OpenKey(reg_key, subkey_name) as subkey:
                                try:
                                    software_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if software_name and software_name.strip():
                                        software_list.append(software_name.strip())
                                except FileNotFoundError:
                                    pass
                                except WindowsError as e:
                                    logging.warning(f"Error reading subkey {subkey_name}: {str(e)}")
                        except WindowsError:
                            pass
            except WindowsError as e:
                logging.error(f"Error opening key {key}: {str(e)}")

        # Check both 32-bit and 64-bit registry keys
        get_software_from_key(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
        get_software_from_key(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
        get_software_from_key(winreg.HKEY_CURRENT_USER, 0)

        # Additional registry keys to check
        additional_keys = [
            r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for add_key in additional_keys:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, add_key, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as reg_key:
                    for i in range(winreg.QueryInfoKey(reg_key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(reg_key, i)
                            with winreg.OpenKey(reg_key, subkey_name) as subkey:
                                try:
                                    software_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if software_name and software_name.strip():
                                        software_list.append(software_name.strip())
                                except FileNotFoundError:
                                    pass
                        except WindowsError:
                            pass
            except WindowsError:
                pass

        # Add Microsoft Store apps
        try:
            apps_path = os.path.join(os.environ["ProgramFiles"], "WindowsApps")
            for item in os.listdir(apps_path):
                if os.path.isdir(os.path.join(apps_path, item)):
                    parts = item.split("_")
                    if len(parts) > 1:
                        software_list.append(parts[0])
        except Exception as e:
            logging.error(f"Error reading Microsoft Store apps: {str(e)}")

        # Remove duplicates and sort
        return sorted(set(software_list))

    def get_system_info(self):
        c = wmi.WMI()
        system_info = {}

        # Operating System Information
        for os in c.Win32_OperatingSystem():
            system_info['OS'] = os.Caption
            system_info['OS Version'] = os.Version
            system_info['OS Build'] = os.BuildNumber
            system_info['OS Architecture'] = os.OSArchitecture

        # CPU Details
        for processor in c.Win32_Processor():
            system_info['CPU Model'] = processor.Name.strip()
            system_info['CPU Cores'] = processor.NumberOfCores
            system_info['CPU Threads'] = processor.ThreadCount
            system_info['CPU Max Clock Speed'] = f"{processor.MaxClockSpeed} MHz"
            system_info['CPU Serial Number'] = processor.ProcessorId.strip()

        # RAM Details
        total_memory = sum(float(memory.Capacity) for memory in c.Win32_PhysicalMemory())
        memory_modules = [memory for memory in c.Win32_PhysicalMemory()]
        memory_serial_numbers = [memory.SerialNumber.strip() for memory in memory_modules if
                                 memory.SerialNumber.strip() not in ["", "00000000"]]
        system_info['Total RAM'] = f"{total_memory / (1024 ** 3):.2f} GB"
        system_info['RAM Modules'] = len(memory_modules)
        system_info['RAM Serial Numbers'] = memory_serial_numbers if memory_serial_numbers else ["Not Available"]

        # Storage Details
        for disk in c.Win32_DiskDrive():
            system_info['Hard Drive Model'] = disk.Model.strip()
            system_info['Hard Drive Size'] = f"{float(disk.Size) / (1024 ** 3):.2f} GB"
            system_info['Hard Drive Serial Number'] = disk.SerialNumber.strip()

        # Motherboard Details
        for board in c.Win32_BaseBoard():
            system_info['Motherboard Manufacturer'] = board.Manufacturer.strip()
            system_info['Motherboard Model'] = board.Product.strip()
            system_info['Motherboard Serial Number'] = board.SerialNumber.strip()

        # BIOS Details
        for bios in c.Win32_BIOS():
            system_info['BIOS Manufacturer'] = bios.Manufacturer.strip()
            system_info['BIOS Version'] = bios.Version.strip()
            system_info['BIOS Serial Number'] = bios.SerialNumber.strip()

        # Graphics Card Details
        for video_card in c.Win32_VideoController():
            system_info['Graphics Card'] = video_card.Name.strip()

        # Sound Controller Details
        for sound in c.Win32_SoundDevice():
            system_info['Sound Controller'] = sound.Name.strip()

        # Network Adapters
        adapters = [adapter.Name.strip() for adapter in c.Win32_NetworkAdapter() if adapter.NetEnabled]
        system_info['Network Adapters'] = adapters

        # Hardware General Details
        for computer in c.Win32_ComputerSystem():
            system_info['Computer Manufacturer'] = computer.Manufacturer.strip()
            system_info['Computer Model'] = computer.Model.strip()
            system_info['System Type'] = computer.SystemType.strip()
            system_info['Number of Processors'] = computer.NumberOfProcessors

        # Installed Software
        system_info['Installed Software'] = self.get_installed_software()

        return system_info

    def save_to_file(self, info, file_path):
        print("""Saving system info to .csv file.""")
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Field', 'Value'])
            for key, value in info.items():
                if isinstance(value, list):
                    if key == 'Installed Software':
                        # Write the software list with each entry on a new line
                        writer.writerow([key, ''])  # Write the key with an empty value
                        for software in value:
                            writer.writerow(['', software])  # Write each software on a new line with an empty key
                    else:
                        # For other lists, join elements into a single string separated by commas
                        writer.writerow([key, ', '.join(value)])
                else:
                    writer.writerow([key, value])

    def select_file(self):
        file_path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension='.csv',
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Choose a location to save the file"
        )
        return file_path

    def on_function_select1(self, event):
        selected1 = self.selected_function1.get()
        if selected1 == "Extract Sys Info":
            self.gather_and_save_info()
        elif selected1 == "Compare Sys Info":
            self.compare_system_info()
        elif selected1 == "Show single Sys":
            self.show_system_info()

    def on_function_select2(self, event):
        selected2 = self.selected_function2.get()
        if selected2 == "Active Connections":
            self.netstat_output()
        elif selected2 == "Threat Search":
            self.confirm_and_search()

    def gather_and_save_info(self):
        print("""Extracting system info.""")
        global info
        if tk.messagebox.askyesno("Extract", "This may take some time to extract data. Proceed?"):
            info = self.get_system_info()  # Gathers system info
            save_path = self.select_file()  # Opens the file selection dialog
            if save_path:
                self.save_to_file(info, save_path)  # Saves the info to the selected file
                messagebox.showinfo("Success", f"System information saved to {save_path}")
            else:
                messagebox.showinfo("Cancelled", "Operation cancelled by user")

    def compare_system_info(self):
        file_paths = filedialog.askopenfilenames(
            title="Select CSV files",
            filetypes=[("CSV Files", "*.csv")])

        if not file_paths:
            # messagebox.showinfo("Cancelled", "No files were selected.")
            return

        all_systems_info = [self.read_csv_file(path) for path in file_paths]

        differences = self.find_differences(all_systems_info)

        if differences:
            save_path = filedialog.asksaveasfilename(
                title="Save System Compare File",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                initialfile="SystemCompare.html")

            if save_path:
                self.write_differences_to_file(differences, save_path)
                messagebox.showinfo("Success", f"System comparison saved to {save_path}")
            else:
                messagebox.showinfo("Cancelled", "Save file operation was cancelled.")
        else:
            messagebox.showinfo("No Differences", "No differences found among the selected files.")

    def read_csv_file(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return file_path, {row['Field']: row['Value'] for row in reader}

    def find_differences(self, systems_info):
        # Get the union of keys from all systems
        all_keys = set().union(*(info[1].keys() for info in systems_info))
        differences = {field: {} for field in all_keys}

        for file_path, system in systems_info:
            for field in all_keys:
                for other_file_path, other_system in systems_info:
                    # If the field exists in both systems, and they are not equal, record the difference
                    if field in system and field in other_system and system[field] != other_system[field]:
                        if system[field] not in differences[field]:
                            differences[field][system[field]] = []
                        if other_system[field] not in differences[field]:
                            differences[field][other_system[field]] = []

                        differences[field][system[field]].append(file_path)
                        differences[field][other_system[field]].append(other_file_path)

        # Remove fields where no differences were found
        return {field: vals for field, vals in differences.items() if vals}

    def write_differences_to_file(self, differences, file_path):
        print("""Merging system info for comparison.""")
        with open(file_path, mode='w', encoding='utf-8') as htmlfile:
            # Write the beginning of the HTML file with updated styles
            htmlfile.write('<html><head><style>')
            htmlfile.write('body { background-color: #2b2b2b; color: #f0f0f0; font-family: Arial, sans-serif; }')
            htmlfile.write('table {border-collapse: separate; border-spacing: 0 10px; width: 100%;}')
            htmlfile.write('th, td {border: 1px solid #ddd; padding: 8px; background-color: #5b8ea6;}')
            htmlfile.write('th {padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #3a7ca5;}')
            htmlfile.write('tr:nth-child(even) {background-color: #f2f2f2; color: #333;}')
            htmlfile.write('</style></head><body>')
            htmlfile.write('<table>')
            htmlfile.write('<tr><th>Field</th><th>Value</th><th>Files</th></tr>')

            for field, values in differences.items():
                for value, files in values.items():
                    # Extract just the file names from the paths and remove the '.csv' extension
                    file_names = set(os.path.splitext(os.path.basename(file))[0] for file in files)  # Use a set to get unique filenames
                    file_names_with_count = ', '.join(sorted(file_names))  # Sort the filenames
                    # row_color = color_scheme.get(field, "#ffffff")
                    htmlfile.write(f'<tr><td>{field}</td><td>{value}</td><td>{file_names_with_count}</td></tr>')

            # End the HTML file
            htmlfile.write('</table></body></html>')

    def show_system_info(self):
        file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            # messagebox.showinfo("Cancelled", "No file was selected.")
            return

        system_info = self.read_single_csv(file_path)

        print("\nSystem Info before writing to HTML:")
        for key, value in system_info.items():
            print(f"{key}: {value}")

        save_path = filedialog.asksaveasfilename(
            title="Save System Info File",
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html")],
            initialfile="SystemInfo.html")

        if save_path:
            try:
                self.write_system_info_to_file(system_info, save_path)
                messagebox.showinfo("Success", f"System info saved to {save_path}")
            except PermissionError as e:
                messagebox.showerror("Permission Error", f"Permission denied: {str(e)}")
        else:
            messagebox.showinfo("Cancelled", "Save file operation was cancelled.")

    def read_single_csv(self, file_path):
        system_info = {}
        current_field = None

        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0]:  # Non-empty row with content in the first column
                    current_field = row[0]
                    if current_field == 'Installed Software':
                        system_info[current_field] = []
                    elif len(row) > 1:
                        system_info[current_field] = row[1]
                    else:
                        system_info[current_field] = ''
                elif current_field == 'Installed Software' and len(row) > 1:
                    system_info[current_field].append(row[1])
                elif current_field and len(row) > 1:
                    # Append to existing value if it's a continuation
                    system_info[current_field] += f", {row[1]}"

        print("Processed system_info:")
        for key, value in system_info.items():
            print(f"{key}: {value}")

        return system_info

    def write_system_info_to_file(self, system_info, file_path):
        print("""Creating system info file.""")
        with open(file_path, mode='w', encoding='utf-8') as htmlfile:
            htmlfile.write('<html><head><style>')
            htmlfile.write('body { background-color: #2b2b2b; color: #f0f0f0; font-family: Arial, sans-serif; }')
            htmlfile.write('table {border-collapse: separate; border-spacing: 0 10px; width: 100%;}')
            htmlfile.write('th, td {border: 1px solid #ddd; padding: 8px; background-color: #5b8ea6;}')
            htmlfile.write('th {padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #3a7ca5;}')
            htmlfile.write('tr:nth-child(even) {background-color: #f2f2f2; color: #333;}')
            htmlfile.write('</style></head><body>')
            htmlfile.write('<table>')
            htmlfile.write('<tr><th>Field</th><th>Value</th></tr>')

            for field, value in system_info.items():
                htmlfile.write(f'<tr><td>{field}</td><td>')
                if field == 'Installed Software' and isinstance(value, list):
                    htmlfile.write('<ul>')
                    for software in value:
                        htmlfile.write(f'<li>{software}</li>')
                    htmlfile.write('</ul>')
                else:
                    htmlfile.write(f'{value}')
                htmlfile.write('</td></tr>')

            htmlfile.write('</table></body></html>')

    def check_internet(self):
        print("""Running various 'is online?' checks.""")

        def run_checks():
            results = []
            methods = [
                ("Ping", '8.8.8.8'),
                ("Socket", ('8.8.8.8', 53)),
                ("HTTP", 'http://www.google.com')
            ]

            for method_name, target in methods:
                start_time = time.time()
                success, message = False, f"{method_name} failed"

                if method_name == "Ping":
                    try:
                        param = '-n' if sys.platform.lower() == 'win32' else '-c'
                        subprocess.run(['ping', param, '1', target],
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL,
                                       check=True)
                        success, message = True, f"{method_name} (8.8.8.8) successful"
                    except subprocess.CalledProcessError:
                        pass
                elif method_name == "Socket":
                    try:
                        socket.create_connection(target, timeout=3)
                        success, message = True, f"{method_name} (8.8.8.8 - Port 53) connection successful"
                    except socket.error:
                        pass
                elif method_name == "HTTP":
                    try:
                        response = requests.get(target, timeout=5)
                        if response.status_code == 200:
                            success, message = True, f"{method_name} (http://www.google.com) request successful"
                    except requests.RequestException:
                        pass

                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)  # Convert to ms
                results.append((success, message, latency))

            online = any(result[0] for result in results)
            status_message = "\n".join(f"{msg} \n(Latency: {lat} ms)\n" for _, msg, lat in results)

            if online:
                messagebox.showinfo("Internet Status", f"We're online :)\n\n{status_message}")
            else:
                messagebox.showwarning("Internet Status", f"We're offline :(\n\n{status_message}")

        # Run the internet checks in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_checks)
        thread.start()

    def netstat_output(self):
        print("""Executing Network Shell command to extract apps with active internet connection.""")
        try:
            # Ask user if they want to create the file
            if not messagebox.askyesno("Create File", "This will create the file 'netstat_exe_output.txt', which contains a list with all apps that have an active internet connection?"):
                return

            # Execute the netstat command and capture the output
            result = subprocess.check_output('netstat -b -n', shell=True).decode()

            # Define the file path
            file_path = os.path.join(os.path.dirname(__file__), 'netstat_exe_output.txt')

            # Write the command output to a file
            with open(file_path, 'w') as file:
                file.write(result)

            # Read and process the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Filter and format the content
            processed_lines = [re.findall(r'\[(.*?)]', line) for line in lines]
            processed_lines = [item for sublist in processed_lines for item in sublist]

            # Remove duplicates by converting the list to a set and back to a list
            unique_lines = list(set(processed_lines))

            # Save the processed content, now without duplicates
            with open(file_path, 'w') as file:
                for line in unique_lines:
                    file.write(line + '\n')

            messagebox.showinfo("Success", "'netstat_exe_output.txt' successfully created in the app's root folder.\n\n'Threat Search' will lookup each one in a separate Google search tab.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while executing the netstat command: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def search_app_info(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), 'netstat_exe_output.txt')
        search_base_url = "https://www.google.com/search?q="

        # Read the application names from the file
        with open(file_path, 'r') as file:
            app_list = [line.strip() for line in file if line.strip()]

        # Perform a search for each application
        for app in app_list:
            query = f"Is {app} dangerous?"
            webbrowser.open(search_base_url + query.replace(' ', '+'))

    def confirm_and_search(self):
        file_path = os.path.join(os.path.dirname(__file__), 'netstat_exe_output.txt')

        # Check if the file exists
        if not os.path.exists(file_path):
            messagebox.showinfo("File Not Found", f"netstat_exe_output.txt not found\n\nPlease click 'Active Connections' first and try again.")
            return

        response = messagebox.askyesno("Confirm Search", "Do you want to check scanned App information online?\n\nWARNING: This will open a new google search tab for every entry in netstat_exe_output.txt")
        if response:
            self.search_app_info(file_path)
        print("""Searching scanned apps online to check their trustworthiness.""")

    def git_pull(self):
        # Determine if we're running as a script or frozen executable
        if getattr(sys, 'frozen', False):
            # We're running in a PyInstaller bundle
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))  # Use default if _MEIPASS not present
            repo_path = os.path.dirname(sys.executable)
            print(f"""
╔═════════════════════════════════ERROR═════════════════════════════════════╗
║ You are running WinFunct from an .exe file.                               ║
║ Please clone the repository from GitHub via 'Get from GitHub' button      ║
║ and execute 'Run' to start the app to make use of the 'Update' function.  ║
║ Make sure "Git for Windows" and "Python 3.x" is installed!                ║
╚═══════════════════════════════════════════════════════════════════════════╝
            """)
            return False, "Cannot update when running from .exe"
        else:
            # We're running in a normal Python environment
            base_path = os.path.dirname(os.path.abspath(__file__))
            repo_path = os.getcwd()

        requirements_path = os.path.join(repo_path, 'requirements.txt')

        # Get the hash of requirements.txt before the pull
        before_pull_hash = self.file_hash(requirements_path) if os.path.exists(requirements_path) else None

        try:
            # Change to the repo directory before git operations
            os.chdir(repo_path)

            # Create and show progress window
            progress_window = self.create_progress_window("Updating...")

            # Execute 'git pull' with progress updates
            process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            output = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    output.append(line.strip())
                    self.update_progress(progress_window, f"Pulling updates: {line.strip()}")

            progress_window.destroy()

            result = process.communicate()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, "git pull", result[1])

            full_output = "\n".join(output)
            print(full_output)

            # Check if updates were actually applied
            if "Already up to date." not in full_output:
                print(f"Update detected. Notifying user...")
                self.notify_user_of_update(full_output)

                # Check if requirements.txt has changed by comparing hashes
                after_pull_hash = self.file_hash(requirements_path) if os.path.exists(requirements_path) else None
                if before_pull_hash != after_pull_hash:
                    print(f"requirements.txt has changed. Installing new requirements...")
                    self.install_requirements(requirements_path)
            else:
                print(f"No updates available.")

            return True, full_output
        except subprocess.CalledProcessError as e:
            print(f"Error during git pull: {e.stderr}")
            return False, e.stderr
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False, str(e)
        finally:
            # Change back to the original directory
            os.chdir(base_path)

    def file_hash(self, filepath):
        """Calculates the MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def install_requirements(self, requirements_path):
        """Installs the packages from requirements.txt using pip."""
        try:
            progress_window = self.create_progress_window("Installing Requirements")

            process = subprocess.Popen(["pip", "install", "-r", requirements_path], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)

            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    self.update_progress(progress_window, f"Installing: {line.strip()}")

            progress_window.destroy()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, "pip install", process.stderr.read())

            print(f"Requirements installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing requirements: {e.stderr}")

    def notify_user_of_update(self, update_info):
        """Notifies the user of the update with detailed information."""
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("Update Applied",
                            f"Updates have been applied. Please restart the application to use the latest version.\n\nUpdate details:\n{update_info}")
        root.destroy()

    def create_progress_window(self, title):
        """Creates a progress window with a label and indeterminate progress bar."""
        window = tk.Toplevel()
        window.title(title)
        window.geometry("300x100")

        # Make the window appear on top of other windows
        window.attributes('-topmost', True)

        # Withdraw the window to hide it before setting its position
        window.withdraw()

        # Calculate the center position
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = 300
        window_height = 100
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        # Set the position of the window
        window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        progress_label = tk.Label(window, text="Starting...")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(window, mode="indeterminate", length=200)
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Make the window visible again
        window.deiconify()

        window.update()
        return window

    def update_progress(self, window, message):
        """Updates the progress window with a new message."""
        if window.winfo_exists():
            window.children['!label'].config(text=message)
            window.update()

    def check_dependencies(self):
        """Check if Git and Python are installed and show a message box if not."""
        print(f"\nPlease select location.\n'WinFunct' Folder will be created & cloned at this location.")
        print(f"Checking dependencies:\n")
        dependencies = {
            "Git": ["git", "--version", "https://git-scm.com/downloads"],
            "Python": ["python", "--version", "https://www.python.org/downloads/"]
        }
        missing_deps = []

        for dep, commands in dependencies.items():
            try:
                result = subprocess.run(commands[:2], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"{dep} version: {result.stdout.strip()}")  # Improved: Strip extra whitespace
            except subprocess.CalledProcessError as e:
                print(f"Failed to run {commands[0]}: {e.stderr.strip()}")  # Improved: Strip extra whitespace
                missing_deps.append((dep, commands[2]))

        if missing_deps:
            self.notify_missing_dependencies(missing_deps)
            return False
        return True

    def notify_missing_dependencies(self, missing_deps):
        """Showing a message box with options to download missing dependencies."""
        message = "The following dependencies are missing:\n"
        for dep, _ in missing_deps:
            message += f"- {dep}\n"
        message += "Would you like to download them now?"

        if messagebox.askyesno("Missing Dependencies", message):
            for _, url in missing_deps:
                webbrowser.open(url)

    def run(self):
        """Check dependencies before proceeding."""
        if not self.check_dependencies():
            messagebox.showerror("Missing Dependencies", "Git and/or Python are not installed.")
            return

    def select_clone_directory(self):
        """Prompt user to select directory where the repo should be cloned."""
        root = tk.Tk()
        root.withdraw()  # Keep the root window from appearing
        directory = filedialog.askdirectory()  # Show dialog and return the path
        root.destroy()
        return directory if directory else None  # Return None if no directory selected

    def clone_repository(self, repo_url, clone_path):
        print("""Cloning repository.""")
        """Clone the repository into the selected path."""
        repo_name = repo_url.split('/')[-1][:-4]  # Extract repo name
        final_clone_path = os.path.join(clone_path, repo_name)

        try:
            subprocess.run(["git", "clone", repo_url, final_clone_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            messagebox.showinfo("Repository Cloned", f"Repository cloned successfully into {final_clone_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to clone repository: {e.stderr.strip()}")  # Improved: Strip extra whitespace

    def clone_repo_with_prompt(self):
        if not self.check_dependencies():
            messagebox.showerror("Missing Dependencies", "Git and/or Python are not installed.")
            return

        clone_path = self.select_clone_directory()
        if clone_path is None:
            # messagebox.showwarning("Clone Cancelled", "Repository clone cancelled. No directory selected.")
            return

        self.clone_repository("https://github.com/df8819/WinFunct.git", clone_path)

    def open_godmode(self):
        print("""Executing:\n'explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}' command in cmd\nto summon the Windows 'godmode' options window.""")
        def run_command():
            try:
                subprocess.run("explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}", shell=True)
            except Exception as e:
                print(f"Error: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def logoff_users(self):
        print("""Running 'quser' command to get list of logged-in users.""")
        try:
            # Use 'cp850' encoding which is common on Windows command line
            result = subprocess.run(['quser'], capture_output=True, text=True, encoding='cp850', errors='replace', shell=True)
            output = result.stdout
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run 'quser': {e}")
            return

        if output is None:
            messagebox.showerror("Error", "No output from 'quser'.")
            return

        # Parse the output to extract user information
        lines = output.strip().split('\n')
        users = []

        for line in lines[1:]:  # Skip the header line
            # Adjusted regex to capture usernames with spaces and special characters
            match = re.match(r'^\s*(.*?)\s+(\d+)\s+\w+', line)
            if match:
                username = match.group(1).strip()
                session_id = match.group(2)
                users.append((username, session_id))

        if not users:
            messagebox.showinfo("Info", "No users found.")
            return

        # Create a Tkinter window to display a listbox for user selection
        window = tk.Tk()
        window.title("Select Users to Log Off")

        # Set the initial window size
        window_width = 400
        window_height = 300
        window.geometry(f"{window_width}x{window_height}")

        # Center the window on the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        window.geometry(f"+{x_cordinate}+{y_cordinate}")

        # Create a frame to hold the Listbox and Scrollbar
        frame = ttk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a Listbox for multiple selection with a Scrollbar
        listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for username, session_id in users:
            listbox.insert(tk.END, f"{username} (Session ID: {session_id})")

        def on_submit():
            selected_indices = listbox.curselection()
            selected_users = [users[i] for i in selected_indices]

            if not selected_users:
                messagebox.showinfo("Info", "No users selected.")
                return

            confirmation = messagebox.askyesno("Confirm", f"Are you sure you want to log off {len(selected_users)} user(s)?")
            if not confirmation:
                return

            for username, session_id in selected_users:
                try:
                    subprocess.run(['logoff', session_id], shell=True, check=True)
                    print(f"Logged off: {username} (Session ID: {session_id})")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Failed to log off {username}: {e}")

            messagebox.showinfo("Success", f"Successfully logged off {len(selected_users)} user(s).")
            window.destroy()

        # Add submit and cancel buttons
        button_frame = ttk.Frame(window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        submit_button = ttk.Button(button_frame, text="Log Off Selected Users", command=on_submit)
        submit_button.pack(side=tk.LEFT, padx=(0, 5))

        cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
        cancel_button.pack(side=tk.RIGHT)

        window.mainloop()

    def open_links_window(self):
        print("""Open Link summary.""")
        window = tk.Toplevel(self)
        window.title("Download Links")
        window.resizable(True, True)

        main_frame = ttk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.checkbox_vars = {}

        for category, items in links.items():
            category_frame = ttk.LabelFrame(scrollable_frame, text=category)
            category_frame.pack(fill="x", expand=True, padx=10, pady=5)

            for i, (text, link) in enumerate(items.items()):
                var = tk.IntVar()
                checkbox = ttk.Checkbutton(category_frame, text=text, variable=var)
                checkbox.grid(row=i // 3, column=i % 3, sticky="w", padx=10, pady=3)
                self.checkbox_vars[link] = var

        button_frame = ttk.Frame(window)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Open Links", command=lambda: self.on_ok(window)).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=window.destroy).pack(side="right", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        window.update_idletasks()
        width = min(500, window.winfo_screenwidth() - 100)
        height = min(640, window.winfo_screenheight() - 100)
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_ok(self, window):
        for link, var in self.checkbox_vars.items():
            if var.get():
                webbrowser.open_new_tab(link)
        window.destroy()  # Close the window

    def create_widgets(self):
        style = ttk.Style()

        # Configure tab padding and general styles
        style.configure('TNotebook.Tab', padding=[10, 7])

        # Background color of all tabs
        # style.configure('TNotebook', background='#F0F8FF')

        self.tabs = ttk.Notebook(self.main_frame, style='TNotebook')

        # Create frames with different background colors
        self.functions_frame = ttk.Frame(self.tabs, style='Functions.TFrame')
        self.options_frame = ttk.Frame(self.tabs, style='Options.TFrame')
        self.fun_frame = ttk.Frame(self.tabs, style='Fun.TFrame')

        # Configure styles for each frame
        style.configure('Functions.TFrame', background=f'{UI_COLOR}')
        style.configure('Options.TFrame', background=f'{UI_COLOR}')
        style.configure('Fun.TFrame', background=f'{UI_COLOR}')

        self.tabs.add(self.functions_frame, text="Scripts")
        self.tabs.add(self.options_frame, text="Options")
        self.tabs.add(self.fun_frame, text="Misc")

        self.tabs.pack(fill="both", expand=True)

        # Options Notebook within the options tab
        options_notebook = ttk.Notebook(self.options_frame, style='TNotebook')  # Apply the style here

        # New Category Frames inside the Options tab with different background colors
        advanced_windows_settings_frame = ttk.Frame(options_notebook, style='Advanced.TFrame')
        system_tools_frame = ttk.Frame(options_notebook, style='SystemTools.TFrame')
        utilities_frame = ttk.Frame(options_notebook, style='Utilities.TFrame')
        tools_frame = ttk.Frame(options_notebook, style='Tools.TFrame')
        trouble_frame = ttk.Frame(options_notebook, style='Trouble.TFrame')
        netsh_frame = ttk.Frame(options_notebook, style='Netsh.TFrame')

        # Configure styles for each frame in the options notebook
        style.configure('Advanced.TFrame', background=f'{UI_COLOR}')
        style.configure('SystemTools.TFrame', background=f'{UI_COLOR}')
        style.configure('Utilities.TFrame', background=f'{UI_COLOR}')
        style.configure('Tools.TFrame', background=f'{UI_COLOR}')
        style.configure('Trouble.TFrame', background=f'{UI_COLOR}')
        style.configure('Netsh.TFrame', background=f'{UI_COLOR}')

        # Adding new frames to the options notebook
        options_notebook.add(advanced_windows_settings_frame, text='Management')
        options_notebook.add(system_tools_frame, text='Security & Network')
        options_notebook.add(utilities_frame, text='System Tools')
        options_notebook.add(tools_frame, text='RDP & Environment')
        options_notebook.add(trouble_frame, text='Trouble & Optimize')
        options_notebook.add(netsh_frame, text='Shell Commands')

        # Packing the notebook into the options_frame
        options_notebook.pack(fill='both', expand=True, padx=20, pady=20)

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
            ("System Name", "SystemPropertiesComputerName"),
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
        ]

        # Function to create buttons within a frame from a list of option tuples
        def create_option_buttons(frame, options_list):
            for i, option in enumerate(options_list):
                btn = ttk.Button(frame, text=option[0], command=lambda cmd=option[1]: execute_command(cmd), width=20)
                btn.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="we")

        # Create buttons in their distinct categories
        create_option_buttons(advanced_windows_settings_frame, windows_management_options)
        create_option_buttons(system_tools_frame, security_and_networking_options)
        create_option_buttons(utilities_frame, system_tools_options)
        create_option_buttons(tools_frame, remote_and_virtualization_options)
        create_option_buttons(trouble_frame, troubleshooting_and_optimization_options)
        create_option_buttons(netsh_frame, netsh_commands)

        version_label = tk.Label(
            self,
            text=VERSION,
            anchor="se",
            cursor="hand2",
            fg="#7a7a7a",
            # bg="#F0F8FF"  # Set background color here
        )
        version_label.pack(side="bottom", anchor="se", padx=5, pady=2)

        # Callback function for clicking the version label
        def open_link(event):
            webbrowser.open(LINK)

        # Bind the callback function to the version label
        version_label.bind("<Button-1>", open_link)

        # Script tab Buttons and Positions 1/2
        my_ip_btn = ttk.Button(self.functions_frame, text="Show my IP", command=self.show_ip_address, width=20)
        my_ip_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        self.ip_text = tk.Entry(self.functions_frame, width=20)
        self.ip_text.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        internet_btn = ttk.Button(self.functions_frame, text="Are we online?", command=self.check_internet, width=20)
        internet_btn.grid(row=0, column=2, padx=10, pady=5, sticky="we")

        cmd_btn = ttk.Button(self.functions_frame, text="admin cmd", command=self.open_cmd_as_admin, width=20)
        cmd_btn.grid(row=0, column=3, padx=10, pady=5, sticky="we")

        ps_btn = ttk.Button(self.functions_frame, text="admin PowerShell", command=self.open_ps_as_admin, width=20)
        ps_btn.grid(row=0, column=4, padx=10, pady=5, sticky="we")

        wifi_btn = ttk.Button(self.functions_frame, text="Wifi Passwords", command=self.show_wifi_networks, width=20)
        wifi_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        winsat_disk_btn = ttk.Button(self.functions_frame, text="Disk Speedtest", command=self.run_winsat_disk, width=20)
        winsat_disk_btn.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        clone_btn = ttk.Button(self.functions_frame, text="Get from GitHub", command=self.clone_repo_with_prompt, width=20)
        clone_btn.grid(row=1, column=2, padx=10, pady=5, sticky="we")

        renew_ip_config_btn = ttk.Button(self.functions_frame, text="Flush/Renew DNS", command=self.renew_ip_config, width=20)
        renew_ip_config_btn.grid(row=1, column=3, padx=10, pady=5, sticky="we")

        # Dropdown menu for similar functions - System Info Compare
        self.selected_function1 = tk.StringVar()
        self.function_dropdown1 = ttk.Combobox(
            self.functions_frame,
            textvariable=self.selected_function1,
            values=["Extract Sys Info", "Compare Sys Info", "Show single Sys"],
            state="readonly",
            width=20
        )
        self.function_dropdown1.grid(row=1, column=4, padx=10, pady=5, sticky="we")
        self.function_dropdown1.set("System Info")  # Set default text
        self.function_dropdown1.bind("<<ComboboxSelected>>", self.on_function_select1)

        # Dropdown menu for similar functions - Active internet connection apps
        self.selected_function2 = tk.StringVar()
        self.function_dropdown2 = ttk.Combobox(
            self.functions_frame,
            textvariable=self.selected_function2,
            values=["Active Connections", "Threat Search"],
            state="readonly",
            width=20
        )
        self.function_dropdown2.grid(row=2, column=4, padx=10, pady=5, sticky="we")
        self.function_dropdown2.set("App Connections")  # Set default text
        self.function_dropdown2.bind("<<ComboboxSelected>>", self.on_function_select2)

        # Script tab Buttons and Positions 2/2
        activate_wui_btn = ttk.Button(self.functions_frame, text="Open CTT Winutil", command=self.activate_wui, width=20)
        activate_wui_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        activate_win_btn = ttk.Button(self.functions_frame, text="Activate Win/Office", command=self.activate_win, width=20)
        activate_win_btn.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        agh_curl_btn = ttk.Button(self.functions_frame, text="AdGuard curl-copy", command=self.agh_curl, width=20)
        agh_curl_btn.grid(row=2, column=2, padx=10, pady=5, sticky="we")

        logoff_usr_btn = ttk.Button(self.functions_frame, text="Logoff user(s)", command=self.logoff_users, width=20)
        logoff_usr_btn.grid(row=2, column=3, padx=10, pady=5, sticky="we")

        open_links_btn = ttk.Button(self.functions_frame, text="Open Link Summary", command=self.open_links_window, width=20)
        open_links_btn.grid(row=3, column=0, padx=10, pady=5, sticky="we")

        autostart_btn = ttk.Button(self.functions_frame, text="Autostart locations", command=self.open_autostart_locations, width=20)
        autostart_btn.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        install_ffmpeg_btn = ttk.Button(self.functions_frame, text="Install/Update FFMPEG", command=self.install_ffmpeg, width=20)
        install_ffmpeg_btn.grid(row=3, column=2, padx=10, pady=5, sticky="we")

        shutdown_i_btn = ttk.Button(self.functions_frame, text="Execute shutdown -i", command=self.shutdown_i, width=20)
        shutdown_i_btn.grid(row=3, column=3, padx=10, pady=5, sticky="we")

        website_checker_btn = ttk.Button(self.functions_frame, text="Check website status", command=self.run_website_checker, width=20)
        website_checker_btn.grid(row=4, column=2, padx=10, pady=5, sticky="we")

        godmode_btn = ttk.Button(self.functions_frame, text="Windows Godmode", command=self.open_godmode, width=20)
        godmode_btn.grid(row=4, column=0, padx=10, pady=5, sticky="we")

        checksum_btn = ttk.Button(self.functions_frame, text="Verify file checksum", command=self.get_file_checksum, width=20)
        checksum_btn.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        # Fun Notebook within the fun tab
        fun_notebook = ttk.Notebook(self.fun_frame, style='TNotebook')

        # New Category Frames inside the Fun tab with different background colors
        apps_frame = ttk.Frame(fun_notebook, style='Apps.TFrame')
        fun_stuff_frame = ttk.Frame(fun_notebook, style='FunStuff.TFrame')

        # Configure styles for each frame in the fun notebook
        style.configure('Apps.TFrame', background=f'{UI_COLOR}')
        style.configure('FunStuff.TFrame', background=f'{UI_COLOR}')

        # Adding new frames to the fun notebook
        fun_notebook.add(apps_frame, text='Apps')
        fun_notebook.add(fun_stuff_frame, text='Fun Stuff')

        # Packing the notebook into the fun_frame
        fun_notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Function to create buttons within a frame from a list of option tuples
        def create_fun_buttons(frame, buttons_list):
            for i, button in enumerate(buttons_list):
                btn = ttk.Button(frame, text=button[0], command=button[1], width=20)
                btn.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="we")

        # Define buttons for Apps frame
        apps_buttons = [
            ("Password Generator", self.open_pw_gen),
            ("Color Picker", self.open_color_picker),
        ]

        # Define buttons for Fun Stuff frame
        fun_stuff_buttons = [
            ("JChat GUI", self.open_chat),
            ("Hash Generator", self.open_hash_stuff),
            ("Funny ASCII Donut", self.open_donut),
            ("WinFunct Logo", self.show_logo)
        ]

        # Create buttons in their distinct categories
        create_fun_buttons(apps_frame, apps_buttons)
        create_fun_buttons(fun_stuff_frame, fun_stuff_buttons)

        # Bottom frame with a different background color
        self.bottom_frame = ttk.Frame(self.main_frame, style='Bottom.TFrame')
        style.configure('Bottom.TFrame', background=f'{UI_COLOR}')
        self.bottom_frame.pack(fill="x", padx=5, pady=5)

        # Left-aligned buttons
        shutdown_btn = ttk.Button(self.bottom_frame, text="Shutdown", command=self.confirm_shutdown, width=20)
        shutdown_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        reboot_btn = ttk.Button(self.bottom_frame, text="Reboot", command=self.confirm_reboot, width=20)
        reboot_btn.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        uefi_btn = ttk.Button(self.bottom_frame, text="Reboot to BIOS/UEFI", command=self.confirm_uefi, width=20)
        uefi_btn.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        sleep_btn = ttk.Button(self.bottom_frame, text="Enter Hibernation", command=self.confirm_sleep, width=20)
        sleep_btn.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Spacer label to fill the space between left and right groups
        spacer = tk.Label(self.bottom_frame, background=f'{UI_COLOR}')
        spacer.grid(row=0, column=2, rowspan=2, sticky="we")
        self.bottom_frame.columnconfigure(2, weight=1)

        # Right-aligned buttons
        reset_ui_btn = ttk.Button(self.bottom_frame, text="Reset App UI", command=self.reset_ui, width=20)
        reset_ui_btn.grid(row=0, column=5, padx=5, pady=5, sticky="we")

        root_btn = ttk.Button(self.bottom_frame, text="Open Root Folder", command=self.open_app_root_folder, width=20)
        root_btn.grid(row=1, column=4, padx=5, pady=5, sticky="we")

        exit_btn = ttk.Button(self.bottom_frame, text="Exit", command=self.quit, width=20)
        exit_btn.grid(row=1, column=5, padx=5, pady=5, sticky="we")

        update_btn = ttk.Button(self.bottom_frame, text="Update WinFunct", command=self.git_pull, width=20)
        update_btn.grid(row=0, column=4, padx=5, pady=5, sticky="we")


app = Application()
app.mainloop()
