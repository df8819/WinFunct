# Standard Library Imports
import base64
import csv
import ctypes
import hashlib
import json
import logging
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

# Tkinter Imports
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import webbrowser
import winreg

# Third-Party Imports
import requests
import wmi
from win32com.client import Dispatch
import winshell

# noinspection PyUnresolvedReferences
# Local Imports
from config import (
    LOGO, VERSION_NUMBER, VERSION, VERSION_SHORT,
    UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR, BOTTOM_BORDER_COLOR, VERSION_LABEL_TEXT,
    BUTTON_STYLE, BORDER_WIDTH,
    WINFUNCT_LINK, AdGuardClipBoard, ADGUARD_LINK,
    links, batch_script, chkdsk_help_content, ping_help_content,
    windows_management_options, security_and_networking_options,
    system_tools_options, remote_and_virtualization_options,
    troubleshooting_and_optimization_options, netsh_commands
)
from HashStuffInt import HashStuff
from JChatInt import JChat
from SimplePWGenInt import SimplePWGen
from DonutInt import Donut
from ColorPickerInt import SimpleColorPicker
from UISelectorInt import UISelector


# ---------------------------------- START WITH ADMIN RIGHTS / SHOW LOGO / LOAD THEME ----------------------------------


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except WindowsError:
        return False


def check_admin_cmd():
    try:
        output = subprocess.check_output('whoami /groups', shell=True).decode('cp850', errors='replace')
        return "S-1-16-12288" in output
    except subprocess.CalledProcessError:
        return False


def log_message(message):
    with open("admin_log.txt", "a") as log_file:
        log_file.write(message + "\n")


def run_as_admin():
    if sys.platform == "win32":
        cmd = [sys.executable] + sys.argv
        escaped_cmd = [item.replace('"', '\\"') for item in cmd]
        cmd_line = ' '.join(f'"{item}"' for item in escaped_cmd)
        try:
            log_message("Initial checks completed. Running as intended...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd_line, None, 1)
        except Exception as e:
            log_message(f"Error re-running the script with admin rights: {e}")


def is_running_in_ide():
    return any(ide_env in os.environ for ide_env in ["PYCHARM_HOSTED", "VSCode"])


def print_log():
    log_path = "admin_log.txt"
    if os.path.exists(log_path):
        with open(log_path, "r") as log_file:
            print(log_file.read())
        os.remove(log_path)


if __name__ == "__main__":
    if not is_running_in_ide():
        if not (is_admin() or check_admin_cmd()):
            print("Not running with administrative privileges...")
            run_as_admin()
            sys.exit()
        else:
            print("Running with admin rights...")
            print_log()
    else:
        print_log()


def show_logo():
    print(LOGO)


show_logo()
print("Awaiting user input (⌐■_■)")


# Command functions
def execute_command(cmd):
    print(f"Executing: {cmd}")
    subprocess.Popen(cmd, shell=True)


def load_theme_from_file():
    try:
        with open('last_selected_theme.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# ---------------------------------- START WITH ADMIN RIGHTS / SHOW LOGO / LOAD THEME END ----------------------------------


# Main App Window
# noinspection PyTypeChecker,RegExpRedundantEscape,PyMethodMayBeStatic,PyUnusedLocal,PyShadowingNames,PyAttributeOutsideInit,SpellCheckingInspection,PyGlobalUndefined,PyUnboundLocalVariable
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.load_last_selected_theme()

        self.resolution_main = "845x450"
        self.geometry(self.resolution_main)
        self.title("Windows Functionalities (ﾉ◕◡◕)ﾉ*:･ﾟ✧")
        self.configure(bg=UI_COLOR)

        # Create the main_frame with tk.Frame
        self.main_frame = tk.Frame(self, bg=BOTTOM_BORDER_COLOR)
        self.main_frame.pack(fill="both", expand=True)
        self.resizable(True, True)
        self.create_widgets()

        # Load the last selected theme after the main UI is initialized & Center window
        self.after(100, self.load_last_selected_theme)
        self.after(100, self.center_window)

        # Declare variables that will be assigned values later in the program's execution
        self.tabs = None
        self.checkbox_vars = None
        self.fun_frame = None
        self.options_frame = None
        self.create_user = None
        self.ip_text = None
        self.functions_frame = None
        self.bottom_frame = None

    def center_window(self):
        # Using Tcl method to center
        self.eval('tk::PlaceWindow . center')

    def reset_ui(self):
        print("""UI reset.""")
        self.geometry(self.resolution_main)
        self.after(100, self.center_window)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # To make sure the clipboard is updated

    # ----------------------------------DROPDOWN SECTION-------------------------------------------------

    def on_function_select1(self, *args):
        selected1 = self.selected_function1.get()
        actions = {
            "[1] Extract Sys Info": lambda: self.gather_and_save_info(),
            "[2] Compare Sys Info": lambda: self.compare_system_info()
        }
        if selected1 in actions:
            self.function_dropdown1.after(0, actions[selected1])
            self.function_dropdown1.after(0, lambda: self.selected_function1.set("*System Info*"))

    # def on_function_select2(self, *args):
    #     selected2 = self.selected_function2.get()
    #     actions = {
    #         "[1] NEW OPTION": lambda: self.xxxxxxx(),
    #     }
    #     if selected2 in actions:
    #         self.function_dropdown2.after(0, actions[selected2])
    #         self.function_dropdown2.after(0, lambda: self.selected_function2.set("*WHATEV*"))

    def on_function_select3(self, *args):
        selected3 = self.selected_function3.get()
        actions = {
            "[1] Simple God mode": lambda: self.open_godmode(),
            "[2] Super God mode": lambda: self.open_super_godmode()
        }
        if selected3 in actions:
            self.function_dropdown3.after(0, actions[selected3])
            self.function_dropdown3.after(0, lambda: self.selected_function3.set("*God Mode*"))

    def on_function_select4(self, *args):
        selected4 = self.selected_function4.get()
        actions = {
            "[1] cmd": lambda: self.open_cmd_as_admin(),
            "[2] PowerShell": lambda: self.open_ps_as_admin()
        }
        if selected4 in actions:
            self.function_dropdown4.after(0, actions[selected4])
            self.function_dropdown4.after(0, lambda: self.selected_function4.set("*Admin Shells*"))

    def on_function_select5(self, *args):
        selected5 = self.selected_function5.get()
        actions = {
            "[1] PC online status": lambda: self.check_internet(),
            "[2] Website online status": lambda: self.run_website_checker(),
            "[3] Current IP info": lambda: self.show_ip_info(),
            "[4] Apps with internet connection": lambda: self.netstat_output(),
            "[5] Execute <ping> command": lambda: self.show_ping_info()
        }
        if selected5 in actions:
            self.function_dropdown5.after(0, actions[selected5])
            self.function_dropdown5.after(0, lambda: self.selected_function5.set("*IP & Online Status*"))

    def on_function_select6(self, *args):
        selected6 = self.selected_function6.get()
        actions = {
            "[1] CTT Winutils": lambda: self.activate_wui(),
            "[2] Activate Win/Office": lambda: self.activate_win(),
            "[3] Install/Upd. FFMPEG": lambda: self.install_ffmpeg()
        }
        if selected6 in actions:
            self.function_dropdown6.after(0, actions[selected6])
            self.function_dropdown6.after(0, lambda: self.selected_function6.set("*Interactive Shells*"))

    def on_function_select7(self, *args):
        selected7 = self.selected_function7.get()
        actions = {
            "[1] Disk Speedtest": lambda: self.run_winsat_disk(),
            "[2] Show Disk Info": lambda: self.show_disk_info()
        }
        if selected7 in actions:
            self.function_dropdown7.after(0, actions[selected7])
            self.function_dropdown7.after(0, lambda: self.selected_function7.set("*Disk Operations*"))

    def on_function_select8(self, *args):
        selected8 = self.selected_function8.get()
        actions = {
            "[1] Theme Selector": lambda: self.open_theme_selector(),
            "[2] Reset UI": lambda: self.reset_ui()
        }
        if selected8 in actions:
            self.function_dropdown8.after(0, actions[selected8])
            self.function_dropdown8.after(0, lambda: self.selected_function8.set("GUI Options"))

    # ----------------------------------DROPDOWN SECTION END---------------------------------------------
    # ----------------------------------THEME SELECTOR FOR MAIN APP----------------------------------

    def load_last_selected_theme(self):
        global UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR, BOTTOM_BORDER_COLOR, VERSION_LABEL_TEXT
        try:
            with open('last_selected_theme.json', 'r') as file:
                theme = json.load(file)
                UI_COLOR = theme['UI_COLOR']
                BUTTON_BG_COLOR = theme['BUTTON_BG_COLOR']
                BUTTON_TEXT_COLOR = theme['BUTTON_TEXT_COLOR']
                BOTTOM_BORDER_COLOR = theme['BOTTOM_BORDER_COLOR']
                VERSION_LABEL_TEXT = theme['VERSION_LABEL_TEXT']
                self.current_theme = theme
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, use default theme
            pass

    def save_theme_to_file(self, theme_data):
        with open('last_selected_theme.json', 'w') as file:
            json.dump(theme_data, file)

    def load_theme_from_file(self):
        try:
            with open('last_selected_theme.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def open_theme_selector(self):
        if not os.path.exists("UI_themes.json"):
            download_theme = messagebox.askyesno("Download Theme", "The UI_themes.json file was not found. Do you want to download it?")
            if download_theme:
                self.download_theme_file()

        self.current_theme = {
            "UI_COLOR": UI_COLOR,
            "BUTTON_BG_COLOR": BUTTON_BG_COLOR,
            "BUTTON_TEXT_COLOR": BUTTON_TEXT_COLOR,
            "BOTTOM_BORDER_COLOR": BOTTOM_BORDER_COLOR,
            "VERSION_LABEL_TEXT": VERSION_LABEL_TEXT
        }

        UISelector(self, self.current_theme, self.update_theme)

    def download_theme_file(self):
        url = "https://raw.githubusercontent.com/df8819/WinFunct/main/UI_themes.json"
        response = requests.get(url)
        if response.status_code == 200:
            with open("UI_themes.json", "wb") as file:
                file.write(response.content)
        else:
            messagebox.showerror("Download Error", "Failed to download the UI_themes.json file.")

    def update_ui(self, new_theme):
        self.main_frame.configure(bg=new_theme["BOTTOM_BORDER_COLOR"])

    def update_theme(self, new_theme):
        global UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR, BOTTOM_BORDER_COLOR, VERSION_LABEL_TEXT

        UI_COLOR = new_theme['UI_COLOR']
        BUTTON_BG_COLOR = new_theme['BUTTON_BG_COLOR']
        BUTTON_TEXT_COLOR = new_theme['BUTTON_TEXT_COLOR']
        BOTTOM_BORDER_COLOR = new_theme['BOTTOM_BORDER_COLOR']
        VERSION_LABEL_TEXT = new_theme['VERSION_LABEL_TEXT']

        self.current_theme = new_theme
        self.save_theme_to_file(new_theme)
        self.apply_theme()

    def apply_theme(self):
        self.configure(bg=UI_COLOR)
        self.main_frame.configure(bg=BOTTOM_BORDER_COLOR)
        # Apply theme to other widgets as needed
        self.update_ui(self.current_theme)

        def update_widget_colors(widget):
            if isinstance(widget, tk.Button):
                widget.configure(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=UI_COLOR)
            elif isinstance(widget, tk.OptionMenu):
                widget.configure(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
                widget["menu"].configure(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)

            for child in widget.winfo_children():
                update_widget_colors(child)

        update_widget_colors(self)

        # Update ttk styles
        style = ttk.Style()
        style.configure('TNotebook', background=UI_COLOR)
        style.configure('TNotebook.Tab', background=BUTTON_BG_COLOR, foreground=BUTTON_TEXT_COLOR)
        style.map('TNotebook.Tab', background=[('selected', UI_COLOR)])
        style.configure('TFrame', background=UI_COLOR)
        style.configure('TButton', background=BUTTON_BG_COLOR, foreground=BUTTON_TEXT_COLOR)

        # Update the version label
        if hasattr(self, 'version_label'):
            self.version_label.configure(fg=VERSION_LABEL_TEXT, bg=UI_COLOR)

        self.update_idletasks()

        # ----------------------------------THEME SELECTOR FOR MAIN APP END----------------------------------
    # ----------------------------------OPEN BUILT IN APPS----------------------------------

    def open_chat(self):
        print("""Open JChat app.""")
        if tk.messagebox.askyesno("Open JChat",
                                  "This will open a chat-app GUI that requires an OpenAI API Key.\n\nSelect 'No' if you don't have your personal Key yet."):
            chat_window = tk.Toplevel(self)
            chat_window.title("JChat")
            JChat(chat_window, UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR)

    def open_pw_gen(self):
        print("""Open Password Generator app.""")
        pw_window = tk.Toplevel(self)
        pw_window.title("Password Generator")
        pw_window.attributes('-topmost', True)
        SimplePWGen(pw_window, UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR)

    def open_hash_stuff(self):
        print("""Open Hash Generator app.""")
        hash_window = tk.Toplevel(self)
        hash_window.title("Hash Generator")
        hash_window.attributes('-topmost', True)
        HashStuff(hash_window, UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR)

    def open_color_picker(self):
        print("""Open Color Picker app.""")
        color_picker_window = tk.Toplevel(self)
        color_picker_window.title("Color Picker")
        color_picker_window.attributes('-topmost', True)
        SimpleColorPicker(color_picker_window, UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR)

    def open_donut(self):
        print("""Open funny cmd ASCII Donut.""")
        donut = Donut()
        if sys.platform == 'win32':
            subprocess.Popen(['start', 'python', '-c', 'from DonutInt import Donut; Donut().run()'], shell=True)
        else:
            subprocess.Popen(['python', '-c', 'from DonutInt import Donut; Donut().run()'])

    # ----------------------------------OPEN BUILT IN APPS END----------------------------------

    def show_logo(self):
        show_logo()

    def open_app_root_folder(self):
        print("Open root folder location.")
        app_root = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

        if sys.platform == 'win32':
            os.startfile(app_root)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', app_root])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(['xdg-open', app_root])

    def open_ps_as_admin(self):
        print("Open PowerShell window as admin.")

        def check_internet_connection():
            try:
                requests.get("https://www.google.com", timeout=5)
                return True
            except (requests.ConnectionError, requests.Timeout):
                return False

        def check_pwsh_installed():
            try:
                result = subprocess.run(["where", "pwsh"], capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            except subprocess.TimeoutExpired:
                messagebox.showerror("Error", "Timeout while checking for PowerShell 7.")
                return False
            except FileNotFoundError:
                return False

        def install_pwsh():
            if not check_internet_connection():
                messagebox.showerror("Error", "No internet connection. Cannot install PowerShell 7.")
                return False

            try:
                subprocess.run(["winget", "install", "--id", "Microsoft.Powershell", "--source", "winget"], check=True,
                               timeout=300)
                return True
            except subprocess.TimeoutExpired:
                messagebox.showerror("Error", "PowerShell 7 installation timed out.")
                return False
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to install PowerShell 7: {e}")
                return False
            except FileNotFoundError:
                messagebox.showerror("Error", "Winget not found. Cannot install PowerShell 7.")
                return False

        def run_command(use_pwsh):
            try:
                if getattr(sys, 'frozen', False):
                    exe_dir = os.path.dirname(sys.executable)
                    ps_command = f'Set-Location "{exe_dir}"'
                else:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    ps_command = f'Set-Location "{script_dir}"'

                encoded_command = base64.b64encode(ps_command.encode('utf-16le')).decode('ascii')

                if use_pwsh:
                    subprocess.run(
                        f'pwsh -Command "Start-Process pwsh -Verb RunAs -ArgumentList \'-NoExit -EncodedCommand {encoded_command}\'"',
                        shell=True, timeout=30)
                else:
                    subprocess.run(
                        f'powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \'-NoExit -EncodedCommand {encoded_command}\'"',
                        shell=True, timeout=30)
            except subprocess.TimeoutExpired:
                messagebox.showerror("Error", "Timeout while opening PowerShell window.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PowerShell as admin: {e}")

        def threaded_run(use_pwsh):
            thread = threading.Thread(target=run_command, args=(use_pwsh,))
            thread.start()

        if check_pwsh_installed():
            threaded_run(True)
        else:
            user_choice = messagebox.askyesno("PowerShell 7 Not Found",
                                              "PowerShell 7 is not installed. Do you want to install it via winget?")
            if user_choice:
                if install_pwsh():
                    messagebox.showinfo("Installation Successful", "PowerShell 7 has been installed successfully.")
                    threaded_run(True)
                else:
                    messagebox.showwarning("Installation Failed",
                                           "Failed to install PowerShell 7. Opening PowerShell 5.1 instead.")
                    threaded_run(False)
            else:
                messagebox.showinfo("Using PowerShell 5.1", "Opening PowerShell 5.1 instead.")
                threaded_run(False)

    def open_cmd_as_admin(self):
        print("""Open cmd window as admin.""")

        def run_command():
            try:
                if getattr(sys, 'frozen', False):
                    # Running as a PyInstaller executable
                    exe_dir = os.path.dirname(sys.executable)
                    cmd_command = f'start cmd.exe /k cd "{exe_dir}" & title Command Prompt as Admin'
                else:
                    # Running as a script
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    cmd_command = f'start cmd.exe /k cd "{script_dir}" & title Command Prompt as Admin'

                subprocess.run(cmd_command, shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Command Prompt as admin: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def create_ctt_shortcut(self):
        # Define the path for the shortcut
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "CTT-WinUtil.lnk")

        # Define the PowerShell command to be executed
        powershell_command = (
            "Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command iwr -useb https://christitus.com/win | iex' -Verb RunAs"
        )

        # Create a shell object
        shell = Dispatch('WScript.Shell')

        # Create a shortcut object
        shortcut = shell.CreateShortCut(shortcut_path)

        # Set the target path to PowerShell
        shortcut.TargetPath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

        # Set the arguments for the PowerShell command
        shortcut.Arguments = f'-NoProfile -ExecutionPolicy Bypass -Command "{powershell_command}"'

        # Set the working directory (optional)
        shortcut.WorkingDirectory = desktop

        # Set the icon location (optional)
        shortcut.IconLocation = "%SystemRoot%\\system32\\shell32.dll, 5"

        # Save the shortcut
        shortcut.save()

    def restore_health(self):
        print("Restoring System Health")
        thread = threading.Thread(target=self._restore_health_thread)
        thread.start()

    def _restore_health_thread(self):
        try:
            # Run first command
            subprocess.run(["dism", "/online", "/cleanup-image", "/startcomponentcleanup"], check=True)

            # Run second command
            subprocess.run(["dism", "/online", "/cleanup-image", "/restorehealth"], check=True)

            # Prompt user for third command
            self._prompt_sfc_scan()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def _prompt_sfc_scan(self):
        if messagebox.askyesno("SFC Scan",
                               "Do you want to run 'sfc /scannow'?\n\nSFC is the System File Checker that repairs missing or corrupted files."):
            try:
                subprocess.run(["sfc", "/scannow"], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"An error occurred during SFC scan: {str(e)}")

    def create_backup_window(self):
        backup_window = tk.Toplevel()
        backup_window.title("System Backup Options")
        backup_window.configure(bg=UI_COLOR)
        backup_window.geometry("400x100")

        # Configure grid columns to be equal width
        backup_window.grid_columnconfigure(0, weight=1)
        backup_window.grid_columnconfigure(1, weight=1)

        # Create and configure label
        label = tk.Label(backup_window, text="Create one of the following:",
                         bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Create buttons
        restore_point_btn = tk.Button(backup_window, text="Restore Point",
                                      command=lambda: os.startfile(os.path.join(os.environ['WINDIR'],
                                                                                'system32',
                                                                                'SystemPropertiesProtection.exe')),
                                      bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                      width=20)
        restore_point_btn.grid(row=1, column=0, padx=5, pady=10)

        system_image_btn = tk.Button(backup_window, text="System Image",
                                     command=lambda: subprocess.run(
                                         ["control.exe", "/name", "Microsoft.BackupAndRestore"]),
                                     bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                     width=20)
        system_image_btn.grid(row=1, column=1, padx=5, pady=10)

        # Center the window
        backup_window.update_idletasks()
        width = backup_window.winfo_width()
        height = backup_window.winfo_height()
        x = (backup_window.winfo_screenwidth() // 2) - (width // 2)
        y = (backup_window.winfo_screenheight() // 2) - (height // 2)
        backup_window.geometry(f'+{x}+{y}')

    def open_autostart_locations(self):
        print("Open Windows (Auto)-Start locations.")

        # Folder locations
        locations = [
            (os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'),
             "User Startup Folder"),
            ('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp', "All Users Startup Folder"),
            (os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs'),
             "User Start Menu Programs"),
            ('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs', "All Users Start Menu Programs")
        ]

        # Open folder locations
        for path, description in locations:
            if os.path.exists(path):
                print(f"Opening {description}: {path}")
                os.startfile(path)
            else:
                print(f"{description} not found: {path}")

    def show_ip_info(self):
        print("Showing IP information")

        # Create a new window
        ip_window = tk.Toplevel(self)
        ip_window.title("IP Information")
        ip_window.configure(bg=BUTTON_BG_COLOR)

        # Set window size and position
        window_width, window_height = 420, 680
        screen_width = ip_window.winfo_screenwidth()
        screen_height = ip_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        ip_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Create a text widget to display IP information
        ip_info_text = scrolledtext.ScrolledText(ip_window, wrap=tk.WORD, width=40, height=10,
                                                 bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                                 insertbackground=BUTTON_TEXT_COLOR)
        ip_info_text.pack(expand=True, fill='both', padx=10, pady=10)

        max_retries = 5
        retry_delay = 1
        max_delay = 2

        ip_info = ""

        # Fetch local IP information
        try:
            ip_info += "============= Local ============\n"
            adapters = psutil.net_if_addrs()
            for adapter, addresses in adapters.items():
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        ip_address = addr.address
                        ip_info += f"{adapter}:\n{ip_address}\n\n"
        except Exception as e:
            ip_info += f"Error fetching local IP information: {str(e)}\n\n"

        # Fetch and display internet IP information with retries
        for attempt in range(max_retries):
            try:
                ip_info += "\n============= Internet =============\n"
                response = requests.get("https://ipapi.co/json/")
                data = response.json()

                ip_info += f"Public IP:     {data['ip']}\n"
                ip_info += f"ISP:           {data.get('org', 'N/A')}\n"
                ip_info += f"Country:       {data['country_name']}\n"
                ip_info += f"Region:        {data['region']}\n"
                ip_info += f"City:          {data['city']}\n"
                ip_info += f"Postal Code:   {data.get('postal', 'N/A')}\n\n"

                ip_info += "\n============ Topology =============\n"

                ip_info += f"Latitude:      {data['latitude']}\n"
                ip_info += f"Longitude:     {data['longitude']}\n"
                ip_info += f"Timezone:      {data['timezone']}\n\n"

                ip_info += "\n============= Additional Info =============\n"

                ip_info += f"Country Code:  {data['country']}\n"
                ip_info += f"Currency:      {data.get('currency', 'N/A')}\n"
                ip_info += f"Languages:     {data.get('languages', 'N/A')}\n"

                break  # If successful, break out of the retry loop
            except KeyError as e:
                if str(e) == "'ip'" and attempt < max_retries - 1:
                    print(f"Error fetching IP information: {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, max_delay)  # Limit the maximum delay to 2 seconds
                else:
                    ip_info += f"\nError fetching internet IP information: {str(e)}\n"
                    break
            except Exception as e:
                ip_info += f"\nError fetching internet IP information: {str(e)}\n"
                break

        ip_info_text.insert(tk.END, ip_info)
        ip_info_text.config(state='disabled')

    # ----------------------------------QUICK ACCESS MANAGER-------------------------------------------------
    def quick_access_manager(self):
        qa_window = tk.Toplevel(self)
        qa_window.title("Quick Access Manager")
        qa_window.geometry("400x120")
        qa_window.configure(bg=UI_COLOR)

        # Center the window
        def center_window(window):
            window.update_idletasks()
            width = window.winfo_width()
            height = window.winfo_height()
            x = (window.winfo_screenwidth() // 2) - (width // 2)
            y = (window.winfo_screenheight() // 2) - (height // 2)
            window.geometry(f'{width}x{height}+{x}+{y}')

        def export_quick_access():
            source_file = os.path.join(os.path.expanduser("~"),
                                       "AppData", "Roaming",
                                       "Microsoft", "Windows",
                                       "Recent", "AutomaticDestinations",
                                       "f01b4d95cf55d32a.automaticDestinations-ms")

            export_path = filedialog.asksaveasfilename(
                initialfile="f01b4d95cf55d32a.automaticDestinations-ms",
                defaultextension="",  # Remove .ms default extension
                filetypes=[("Automatic Destinations Files", "*.automaticDestinations-ms")],
                title="Export Quick Access Destinations"
            )

            if export_path:
                try:
                    # Ensure the filename is exactly as we want
                    if not export_path.endswith(".automaticDestinations-ms"):
                        # If user somehow changed the extension, force the correct one
                        export_path = os.path.splitext(export_path)[0] + ".automaticDestinations-ms"

                    shutil.copy2(source_file, export_path)
                    messagebox.showinfo("Export Successful",
                                        f"Quick Access destinations exported to:\n{export_path}")
                    qa_window.after(250, qa_window.destroy)
                except Exception as e:
                    messagebox.showerror("Export Error", str(e))

        def import_quick_access():
            import_path = filedialog.askopenfilename(
                filetypes=[
                    ("Automatic Destinations Files", "*.automaticDestinations-ms"),
                    ("All Files", "*.*")
                ],
                title="Import Quick Access Destinations"
            )

            if import_path:
                destination_folder = os.path.join(os.path.expanduser("~"),
                                                  "AppData", "Roaming",
                                                  "Microsoft", "Windows",
                                                  "Recent", "AutomaticDestinations")
                destination_file = os.path.join(destination_folder,
                                                "f01b4d95cf55d32a.automaticDestinations-ms")

                # Corrected file extension validation
                correct_extension = '.automaticDestinations-ms'
                if not import_path.lower().endswith(correct_extension.lower()):
                    messagebox.showerror("Import Error",
                                         f"Please select a valid Automatic Destinations file\n"
                                         f"(*.{correct_extension})")
                    return

                if os.path.exists(destination_file):
                    overwrite = messagebox.askyesno(
                        "File Exists",
                        "An existing Quick Access file was found. Do you want to overwrite it?"
                    )
                    if not overwrite:
                        return

                try:
                    shutil.copy2(import_path, destination_file)
                    messagebox.showinfo("Import Successful",
                                        "Quick Access destinations imported successfully.")
                    subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], shell=True)
                    subprocess.run(['start', 'explorer.exe'], shell=True)
                    qa_window.after(250, qa_window.destroy)
                except Exception as e:
                    messagebox.showerror("Import Error", str(e))

        # Label for the window
        qa_label = tk.Label(qa_window, text="Export or Import your Quick Access Shortcuts with ease.",
                            bg=UI_COLOR,
                            fg=BUTTON_TEXT_COLOR)
        qa_label.pack(pady=20)

        button_frame = tk.Frame(qa_window, bg=UI_COLOR)
        button_frame.pack(pady=10)

        # Export button
        export_button = tk.Button(button_frame,
                                  text="Export Quick Access",
                                  command=export_quick_access,
                                  bg=BUTTON_BG_COLOR,
                                  fg=BUTTON_TEXT_COLOR,
                                  activebackground=UI_COLOR,
                                  activeforeground=BUTTON_TEXT_COLOR,
                                  borderwidth=BORDER_WIDTH,
                                  relief=BUTTON_STYLE)
        export_button.pack(side=tk.LEFT, padx=10)

        # Import button
        import_button = tk.Button(button_frame,
                                  text="Import Quick Access",
                                  command=import_quick_access,
                                  bg=BUTTON_BG_COLOR,
                                  fg=BUTTON_TEXT_COLOR,
                                  activebackground=UI_COLOR,
                                  activeforeground=BUTTON_TEXT_COLOR,
                                  borderwidth=BORDER_WIDTH,
                                  relief=BUTTON_STYLE)
        import_button.pack(side=tk.LEFT, padx=10)

        center_window(qa_window)

        qa_window.grab_set()

    # ----------------------------------QUICK ACCESS MANAGER END-------------------------------------------------
    # ----------------------------------DISK INFO-------------------------------------------------

    def show_disk_info(self):
        print("Showing Disk Information")
        # Create a new window
        disk_window = tk.Toplevel(self)
        disk_window.title("Disk Information")
        disk_window.configure(bg=BUTTON_BG_COLOR)

        # Set window size and position
        window_width, window_height = 615, 685
        screen_width = disk_window.winfo_screenwidth()
        screen_height = disk_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        disk_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Create a text widget to display disk information
        disk_info_text = scrolledtext.ScrolledText(disk_window, wrap=tk.WORD, width=60, height=20, bg=UI_COLOR,
                                                   fg=BUTTON_TEXT_COLOR, insertbackground=BUTTON_TEXT_COLOR)
        disk_info_text.pack(expand=True, fill='both', padx=10, pady=10)

        def bytes_to_gb(byte_value):
            return round(byte_value / (1024 ** 3), 2)

        def fetch_disk_info():
            try:
                disks_cmd = 'powershell "Get-Disk | Format-Table -AutoSize Number, FriendlyName, @{Name=\\"Size, Gb\\"; Expression={[int]($_.Size/1GB)}}"'
                disks_output = subprocess.check_output(disks_cmd, shell=True, text=True)

                cleaned_lines = [line.strip() for line in disks_output.split('\n') if line.strip()]
                cleaned_output = '\n'.join(cleaned_lines)

                disk_info = """
        ╔══════════════════════════════════════════════════════╗
        ║                   Disk Information                   ║
        ╚══════════════════════════════════════════════════════╝

"""
                disk_info += cleaned_output + "\n\n"

                # Add system storage metrics
                disk_info += """
        ╔══════════════════════════════════════════════════════╗
        ║                   Storage Metrics                    ║
        ╚══════════════════════════════════════════════════════╝
"""
                readable_disks = []
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        readable_disks.append(
                            f"\nDrive {partition.mountpoint:<8}"
                            f"\nTotal: {bytes_to_gb(usage.total):>8} GB"
                            f"\nUsed: {bytes_to_gb(usage.used):>8} GB"
                            f"\nFree: {bytes_to_gb(usage.free):>8} GB"
                            f"\nUsage: {usage.percent:>5}%"
                        )
                    except Exception:
                        continue  # Ignore unreadable disks

                if readable_disks:
                    disk_info += '\n'.join(readable_disks) + '\n\n'
                else:
                    disk_info += "No readable disks found.\n"

                # Schedule update on the main thread
                disk_window.after(0, lambda: update_disk_info(disk_info))
            except Exception as e:
                error_message = f"Error fetching disk information: {str(e)}"

                # Collect still readable disks
                readable_disks_info = "\nReadable Disks:"
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        readable_disks_info += (
                            f"\nDrive {partition.mountpoint:<8}"
                            f"\nTotal: {bytes_to_gb(usage.total):>8} GB"
                            f"\nUsed: {bytes_to_gb(usage.used):>8} GB"
                            f"\nFree: {bytes_to_gb(usage.free):>8} GB"
                            f"\nUsage: {usage.percent:>5}%"
                        )
                    except:
                        continue  # Ignore unreadable disks

                full_error_message = f"{error_message}\n{readable_disks_info}\n"

                # Schedule update on the main thread
                disk_window.after(0, lambda: update_disk_info(full_error_message))

        def update_disk_info(info):
            disk_info_text.config(state='normal')
            disk_info_text.delete('1.0', tk.END)
            disk_info_text.insert(tk.END, info)
            disk_info_text.config(state='disabled')

        def run_sfc_scannow():
            if messagebox.askyesno("Confirmation", "Are you sure you want to run 'sfc /scannow'?"):
                subprocess.Popen('start cmd /k sfc /scannow', shell=True)

        def run_chkdsk(drive_letter, options):
            if messagebox.askyesno("Confirmation", f"Are you sure you want to run 'chkdsk {drive_letter} {options}'?"):
                subprocess.Popen(f'start cmd /k chkdsk {drive_letter} {options}', shell=True)

        def show_chkdsk_help():
            help_window = tk.Toplevel(disk_window)
            help_window.title("CHKDSK Parameters")
            help_window.configure(bg=BUTTON_BG_COLOR)

            # Set window size and position
            window_width, window_height = 925, 760
            screen_width = help_window.winfo_screenwidth()
            screen_height = help_window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            help_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

            help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=80, height=25,
                                                  bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                                  insertbackground=BUTTON_TEXT_COLOR)
            help_text.pack(expand=True, fill='both', padx=10, pady=10)
            help_text.insert(tk.END, chkdsk_help_content)  # Ensure this variable is imported correctly
            help_text.config(state='disabled')

        # Create a frame for the buttons
        button_frame = tk.Frame(disk_window, bg=BUTTON_BG_COLOR)
        button_frame.pack(pady=5)

        # Create grid layout for buttons and entry fields
        refresh_btn = tk.Button(button_frame, text="Refresh all Disks", width=20,
                                command=lambda: threading.Thread(target=fetch_disk_info).start(),
                                bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        refresh_btn.grid(row=1, column=0, padx=(5, 50), pady=5)

        chkdsk_btn = tk.Button(button_frame, text="Execute CheckDisk", width=20,
                               command=lambda: threading.Thread(
                                   target=lambda: run_chkdsk(chkdsk_drive_entry.get(),
                                                             chkdsk_options_entry.get())).start(),
                               bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        chkdsk_btn.grid(row=0, column=1, padx=5, pady=5)

        drive_label = tk.Label(button_frame, text="Drive Letter:", width=10,
                               bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        drive_label.grid(row=0, column=2, padx=5, pady=5)

        chkdsk_drive_entry = tk.Entry(button_frame, width=20)
        chkdsk_drive_entry.insert(0, "C:")
        chkdsk_drive_entry.grid(row=0, column=3, padx=5, pady=5)

        sfc_btn = tk.Button(button_frame, text="System File Checker", width=20,
                            command=lambda: threading.Thread(target=run_sfc_scannow).start(),
                            bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        sfc_btn.grid(row=0, column=0, padx=(5, 50), pady=5)

        help_btn = tk.Button(button_frame, text="Argument Helper", width=20,
                             command=lambda: threading.Thread(target=show_chkdsk_help).start(),
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        help_btn.grid(row=1, column=1, padx=5, pady=5)

        arguments_label = tk.Label(button_frame, text="Arguments:", width=10,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        arguments_label.grid(row=1, column=2, padx=5, pady=5)

        chkdsk_options_entry = tk.Entry(button_frame, width=20)
        chkdsk_options_entry.insert(0, "/f /r /x")
        chkdsk_options_entry.grid(row=1, column=3, padx=5, pady=5)

        # Automatically fetch and display the initial disk info when the window opens.
        threading.Thread(target=fetch_disk_info).start()

    # ----------------------------------DISK INFO END-------------------------------------------------
    # ----------------------------------PING COMMAND-------------------------------------------------

    def show_ping_info(self):
        print("Showing Ping Command Window")

        # Create a new window
        ping_window = tk.Toplevel(self)
        ping_window.title("Ping Command")
        ping_window.configure(bg=BUTTON_BG_COLOR)

        # Set window size and position
        window_width, window_height = 475, 100
        screen_width = ping_window.winfo_screenwidth()
        screen_height = ping_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        ping_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        def run_ping_command(target, options):
            # if messagebox.askyesno("Confirmation", f"Are you sure you want to run 'ping {target} {options}'?"):
                subprocess.Popen(f'start cmd /k ping {target} {options}', shell=True)

        def show_ping_help():
            help_window = tk.Toplevel(ping_window)
            help_window.title("Ping Parameters")
            help_window.configure(bg=BUTTON_BG_COLOR)

            # Set window size and position
            window_width, window_height = 925, 690
            screen_width = help_window.winfo_screenwidth()
            screen_height = help_window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            help_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

            help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=80, height=25,
                                                  bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                                  insertbackground=BUTTON_TEXT_COLOR)
            help_text.pack(expand=True, fill='both', padx=10, pady=10)
            help_text.insert(tk.END, ping_help_content)  # Ensure this variable is imported correctly
            help_text.config(state='disabled')

        # Create a frame for the buttons and entry fields
        button_frame = tk.Frame(ping_window, bg=BUTTON_BG_COLOR)
        button_frame.pack(pady=5)

        # Create grid layout for buttons and entry fields
        ping_btn = tk.Button(button_frame, text="Execute Ping", width=15,
                             command=lambda: threading.Thread(
                                 target=lambda: run_ping_command(ping_target_entry.get(),
                                                                 ping_options_entry.get())).start(),
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        ping_btn.grid(row=0, column=0, padx=(5, 75), pady=(15, 5))

        help_btn = tk.Button(button_frame, text="Argument Helper", width=15,
                             command=lambda: threading.Thread(target=show_ping_help).start(),
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        help_btn.grid(row=1, column=0, padx=(5, 75), pady=5)

        target_label = tk.Label(button_frame, text="Target:", width=10,
                                bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        target_label.grid(row=0, column=1, padx=5, pady=5)

        ping_target_entry = tk.Entry(button_frame, width=20)
        ping_target_entry.insert(0, "192.168.1.1")
        ping_target_entry.grid(row=0, column=2, padx=5, pady=5)

        options_label = tk.Label(button_frame, text="Arguments:", width=10,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        options_label.grid(row=1, column=1, padx=5, pady=5)

        ping_options_entry = tk.Entry(button_frame, width=20)
        ping_options_entry.insert(0, "-n 4 -l 32")
        ping_options_entry.grid(row=1, column=2, padx=5, pady=5)

    # ----------------------------------PING COMMAND END-------------------------------------------------
    # ----------------------------------WIFI PASSWORD EXTRACTION-------------------------------------------------

    def decode_output(self, output_bytes):
        encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'cp850']
        for encoding in encodings:
            try:
                return output_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        return output_bytes.decode('utf-8', errors='ignore')

    def get_wifi_profiles(self):
        commands = [
            ["netsh", "wlan", "show", "profile"],
            ["netsh", "wlan", "show", "profiles"],
            ["netsh", "wlan", "show", "interfaces"],
            ["netsh", "wlan", "show", "networks", "mode=bssid"]
        ]

        for cmd in commands:
            try:
                output = subprocess.check_output(
                    cmd,
                    stderr=subprocess.STDOUT,
                    timeout=10,
                    shell=True
                )
                output_text = self.decode_output(output)
                if "Profile" in output_text:
                    return output_text
            except:
                continue
        return None

    def show_wifi_networks(self):
        print("""Extracting Wifi profiles.""")
        try:
            cmd_output = self.get_wifi_profiles()
            if not cmd_output:
                messagebox.showerror("Error", "Could not retrieve WiFi profiles")
                return

            networks = re.findall(
                r"(?:Profile|Profil|Perfil|プロファイル|配置文件)\s*[:：]\s*([^\r\n]+)"
,
                cmd_output
            )

        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Command timed out. Network service might be unresponsive.")
            return
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute netsh command: {e.output.decode('utf-8', 'ignore')}")
            return

        if networks:
            network_window = tk.Toplevel(self)
            network_window.title("Wi-Fi Networks")
            network_window.configure(bg=UI_COLOR)

            window_width = 420
            window_height = 380
            screen_width = network_window.winfo_screenwidth()
            screen_height = network_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            network_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            network_window.resizable(False, False)

            label_text = "Select a Wi-Fi Network from the list to extract its information:"
            label = tk.Label(network_window, text=label_text, bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
            label.pack(pady=10)

            list_frame = tk.Frame(network_window, bg=UI_COLOR)
            list_frame.pack(padx=10, pady=10, fill="both", expand=True)

            scrollbar = tk.Scrollbar(list_frame, orient="vertical")
            network_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, exportselection=False,
                                         bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)

            scrollbar.config(command=network_listbox.yview)
            scrollbar.pack(side="right", fill="y")
            network_listbox.pack(side="left", fill="both", expand=True)

            for network in networks:
                network_listbox.insert(tk.END, network.strip())

            def extract_single_password():
                selected_index = network_listbox.curselection()
                if not selected_index:
                    messagebox.showwarning("No Selection", "Please select a network.")
                    return

                selected_network = network_listbox.get(selected_index).strip()

                try:
                    cmd_output = subprocess.check_output(
                        ["netsh", "wlan", "show", "profile", selected_network, "key=clear"],
                        stderr=subprocess.STDOUT
                    )
                    cmd_output = self.decode_output(cmd_output)
                    password_match = re.search(r"Key Content\s*:\s*([^\r\n]+)", cmd_output)

                    if password_match:
                        password_text = password_match.group(1).rstrip("\r")
                        self.clipboard_clear()  # Clear clipboard
                        self.clipboard_append(password_text)  # Copy password to clipboard
                        messagebox.showinfo("Success", f"Password for '{selected_network}' copied to clipboard.")
                    else:
                        messagebox.showinfo("No Password", f"No password found for '{selected_network}'.")

                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error",
                                         f"Failed to execute command for {selected_network}: {e.output.decode('utf-8', 'ignore')}")

            # Add the <Single> button to the window
            single_button = tk.Button(
                network_window, text="<Single>", command=extract_single_password,
                width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE
            )
            single_button.pack(side="left", padx=(5, 5), pady=10)

            def cancel_button_click():
                network_window.destroy()

            cancel_button = tk.Button(network_window, text="Cancel", command=cancel_button_click, width=10,
                                      bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                      relief=BUTTON_STYLE)
            cancel_button.pack(side="right", padx=(5, 5), pady=10)

            def extract_all_passwords():
                ssid_passwords = {}
                for network in networks:
                    network_profile = network.strip()
                    try:
                        cmd_output = subprocess.check_output(
                            ["netsh", "wlan", "show", "profile", network_profile, "key=clear"],
                            stderr=subprocess.STDOUT)
                        cmd_output = self.decode_output(cmd_output)
                        password = re.search(r"Key Content\s*:\s*([^\r\n]+)"
, cmd_output)
                        if password:
                            password_text = password.group(1).rstrip("\r")
                            ssid_passwords[network_profile] = password_text
                    except subprocess.CalledProcessError as e:
                        messagebox.showerror("Error", f"Failed to execute command for {network}: {e.output.decode('utf-8', 'ignore')}")
                        return

                if ssid_passwords:
                    hostname = socket.gethostname()
                    default_filename = f"pwlist_{hostname}.json"
                    file_path = filedialog.asksaveasfilename(defaultextension='.json', initialfile=default_filename,
                                                             filetypes=[("JSON Files", '*.json'), ("All Files", '*.*')])
                    if file_path:
                        with open(file_path, 'w') as json_file:
                            json.dump(ssid_passwords, json_file, indent=4)
                else:
                    messagebox.showinfo("No Passwords", "No passwords found to extract.")

            extract_all_button = tk.Button(network_window, text="<All>", command=extract_all_passwords,
                                           width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                           relief=BUTTON_STYLE)
            extract_all_button.pack(side="left", padx=(5, 5), pady=10)

            def fast_extract_passwords():
                ssid_passwords = {}
                for network in networks:
                    network_profile = network.strip()
                    try:
                        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network_profile, "key=clear"], stderr=subprocess.STDOUT)
                        cmd_output = self.decode_output(cmd_output)
                        password = re.search(r"Key Content\s*:\s*([^\r\n]+)"
, cmd_output)
                        if password:
                            password_text = password.group(1).rstrip("\r")
                            ssid_passwords[network_profile] = password_text
                    except subprocess.CalledProcessError as e:
                        messagebox.showerror("Error", f"Failed to execute command for {network}: {e.output.decode('utf-8', 'ignore')}")
                        return

                if ssid_passwords:
                    hostname = socket.gethostname()
                    if getattr(sys, 'frozen', False):
                        # Running as a packaged executable
                        executable_path = sys.executable
                        executable_dir = os.path.dirname(executable_path)
                        file_path = os.path.join(executable_dir, f"pwlist_{hostname}.json")
                    else:
                        # Running as a script
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        file_path = os.path.join(script_dir, f"pwlist_{hostname}.json")

                    with open(file_path, 'w') as json_file:
                        json.dump(ssid_passwords, json_file, indent=4)
                else:
                    messagebox.showinfo("No Passwords", "No passwords found to extract.")

            fast_extract_button = tk.Button(network_window, text="<Auto>", command=fast_extract_passwords,
                                            width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                            relief=BUTTON_STYLE)
            fast_extract_button.pack(side="left", padx=(5, 5), pady=10)

        else:
            tk.messagebox.showinfo("Wi-Fi Networks", "No Wi-Fi networks found.")

    # ----------------------------------WIFI PASSWORDS END-------------------------------------------------
    # ----------------------------------DISK SPEEDTEST-------------------------------------------------

    def run_winsat_disk(self):
        print("Running Disk speed test.")

        def get_available_drives():
            drives = []
            for partition in psutil.disk_partitions(all=False):
                if partition.device and partition.device[0].isalpha():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        drives.append(f"{partition.device[0]}: ({usage.total / (1024 ** 3):.2f} GB)")
                    except PermissionError:
                        # Skip drives that we don't have permission to access
                        print(f"Permission denied for {partition.device}")
                    except OSError as e:
                        # Handle other OS-related errors
                        print(f"Error accessing {partition.device}: {e}")
            return drives

        def on_run():
            selected_drive = drive_var.get()

            if selected_drive == "Select a drive":
                messagebox.showwarning("No Drive Selected", "Please select a drive from the dropdown menu.")
                return

            drive_letter = selected_drive[0]

            def run_winsat():
                try:
                    powershell_command = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/c winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
                    subprocess.Popen(powershell_command, shell=True)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while trying to run the WinSAT disk Speedtest test: {str(e)}")
                finally:
                    top.destroy()

            threading.Thread(target=run_winsat, daemon=True).start()

        # Create a top-level window for drive selection
        top = tk.Toplevel(self)
        top.title("WinSAT Disk Performance Test")
        top.geometry("380x130")
        top.configure(bg=UI_COLOR)

        # Center the window on the screen
        top.update_idletasks()
        width = top.winfo_width()
        height = top.winfo_height()
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        top.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Create and pack a label
        label = tk.Label(top, text="Select a drive to test:",
                         bg=UI_COLOR, fg=BUTTON_TEXT_COLOR, pady=10)
        label.pack()

        # Create and pack the dropdown for drive selection
        drive_var = tk.StringVar(top)
        drive_var.set("Select a drive")
        drive_options = get_available_drives()
        drive_menu = tk.OptionMenu(top, drive_var, *drive_options)
        drive_menu.config(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                          activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                          highlightthickness=0)
        drive_menu["menu"].config(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        drive_menu.pack(pady=10)

        # Create and pack the run button
        run_button = tk.Button(top, text="Run Disk Speedtest", command=on_run,
                               bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                               activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                               borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        run_button.pack(pady=10)

    # ----------------------------------DISK SPEEDTEST END-------------------------------------------------
    # ----------------------------------WEBSITE/PC ONLINE STATUS CHECKER-------------------------------------------------

    def run_website_checker(self):
        def on_run():
            website_url = self.website_entry.get().strip()

            # Input validation (keep as is)
            if not website_url:
                messagebox.showwarning("No URL Provided", "Please enter a website URL.")
                return

            url_pattern = re.compile(
                r'^(?:https?:\/\/)?(?:www\.)?'
                r'[a-zA-Z0-9]+(?:[\-\.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}'
                r'(?::[0-9]{1,5})?(?:\/.*)?$'
            )
            if not url_pattern.match(website_url):
                messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
                return

            website_url = 'https://' + website_url if not website_url.startswith(('http://', 'https://')) else website_url

            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bat', encoding='utf-8') as temp_file:
                    check_website_script = temp_file.name
                    formatted_script = batch_script.replace("{{website_url}}", website_url)
                    temp_file.write(formatted_script)

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
        self.top.configure(bg=UI_COLOR)  # Set background color

        # Center the window on the screen
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Create and pack a label
        label = tk.Label(self.top, text="Enter the website URL to check (e.g., example.com):",
                         bg=UI_COLOR, fg=BUTTON_TEXT_COLOR, pady=10)
        label.pack()

        # Create and pack the entry field for the website URL
        self.website_entry = tk.Entry(self.top, width=50, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                      insertbackground=BUTTON_TEXT_COLOR)
        self.website_entry.pack(pady=10)
        self.website_entry.focus_set()

        # Create and pack the run button
        run_button = tk.Button(self.top, text="Check Website", command=on_run,
                               bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                               activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                               borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        run_button.pack(pady=10)

    def check_internet(self):
        print("Running various online checks.")

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

            self.show_result_window(online, status_message)

        # Run the internet checks in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_checks)
        thread.start()

    def show_result_window(self, online, status_message):
        # Create a new window to display internet check results
        result_window = tk.Toplevel(self)
        result_window.title("Internet Status")
        result_window.configure(bg=BUTTON_BG_COLOR)

        # Set window size and position
        window_width, window_height = 470, 250
        screen_width = result_window.winfo_screenwidth()
        screen_height = result_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        result_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Create a text widget to display results
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=40, height=10,
                                                bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                                insertbackground=BUTTON_TEXT_COLOR)
        result_text.pack(expand=True, fill='both', padx=10, pady=10)

        # Replace this part in the show_result_window function
        if online:
            result_text.insert(tk.END, "==============================\n", "center")
            result_text.insert(tk.END, "***       ONLINE :)       ***\n", "center")
            result_text.insert(tk.END, "==============================\n\n", "center")
            result_text.insert(tk.END, status_message)
        else:
            result_text.insert(tk.END, "==============================\n", "center")
            result_text.insert(tk.END, "***      OFFLINE :(      ***\n", "center")
            result_text.insert(tk.END, "==============================\n\n", "center")
            result_text.insert(tk.END, status_message)

        # Add this line after creating the result_text widget
        result_text.tag_configure("center", justify='center')

        result_text.config(state='disabled')  # Make the text widget read-only

    # ----------------------------------WEBSITE/PC ONLINE STATUS CHECKER END-------------------------------------------------
    # ----------------------------------(INTERACTIVE) SHELL COMMANDS-------------------------------------------------

    def get_powershell_command(self):
        # Define potential paths for PowerShell executables
        powershell_paths = [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
            r"C:\Windows\System32\powershell.exe",  # In case of newer versions
        ]

        # Check each path and return the first one that exists
        for path in powershell_paths:
            if os.path.exists(path):
                return path

        # Fallback to PowerShell Core if available
        return "pwsh.exe"

    def activate_win(self):
        print("Activating Microsoft Products")

        def run_command():
            powershell = self.get_powershell_command()
            command = [powershell, '-Command', 'irm https://get.activated.win | iex']
            subprocess.run(command, shell=True)

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def activate_wui(self):
        print("Opening Windows Utility Improved")

        def run_command():
            powershell = self.get_powershell_command()
            command = [powershell, '-Command', 'irm christitus.com/win | iex']
            subprocess.run(command, shell=True)

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    # ----------------------------------(INTERACTIVE) SHELL COMMANDS END-------------------------------------------------
    # ------------------------------------------FFMPEG INSTALLER SCRIPT-----------------------------------------------

    def install_ffmpeg(self):
        # Check if Chocolatey is installed
        chocolatey_installed = os.path.exists(r'C:\ProgramData\chocolatey\bin\choco.exe')

        if chocolatey_installed:
            print('Chocolatey is installed. Attempting to update Chocolatey...')
            try:
                subprocess.run(['powershell.exe', '-Command', 'choco upgrade chocolatey -y'], check=True)
                print('Chocolatey updated successfully.')
            except subprocess.CalledProcessError:
                print('Failed to update Chocolatey. Proceeding with the FFMPEG installation/update anyway.')
        else:
            print('Chocolatey is not installed.')

        print('Proceeding with the FFMPEG installation/update script...')

        def run_ffmpeg_script():
            command = ['powershell.exe', '-Command', 'iex (irm ffmpeg.tc.ht)']
            subprocess.run(command, shell=True)

        # Run the FFMPEG script command in a separate thread
        thread = threading.Thread(target=run_ffmpeg_script)
        thread.start()

    # ------------------------------------------FFMPEG INSTALLER SCRIPT END-----------------------------------------------

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

    def icon_cache(self):
        # Ask for user confirmation before proceeding
        if messagebox.askyesno(
                "Clear Icon Cache",
                "This will kill the explorer.exe task, delete the icon cache in %localappdata%\\Microsoft\\Windows\\Explorer and restart explorer.exe. Proceed?"
        ):
            # Batch script content to clear icon cache and delete itself
            script_content = """
    @echo off
    cls
    echo Clearing the icon cache...
    
    rem Stop explorer.exe
    taskkill /f /im explorer.exe
    
    rem Delete icon cache
    del /a /q /f "%localappdata%\\IconCache.db"
    del /a /q /f "%localappdata%\\Microsoft\\Windows\\Explorer\\iconcache*.*"
    
    rem Restart explorer.exe
    start explorer.exe
    echo Icon cache cleared.
    echo explorer.exe restarted.
    
    rem Use START to launch a new process to delete this script
    start /b cmd /c del "%~f0"
    """

            # Create the .bat file with the script content
            with open('clear_icon_cache.bat', 'w') as script_file:
                script_file.write(script_content)

            # Execute the .bat file
            subprocess.run(['clear_icon_cache.bat'], shell=True)

    # ----------------------------------(INTERACTIVE) SHELL COMMANDS END-------------------------------------------------
    # ----------------------------------FLUSH DNS-------------------------------------------------

    def renew_ip_config(self):
        if messagebox.askyesno("Renew IP Configuration",
                               "Are you sure you want to release/renew the IP config and flush DNS?\n\nIMPORTANT:\n- Active downloads may pause or fail, but they won't be explicitly cancelled.\n- Internet connection will be temporarily lost and then reestablished.\n- Any ongoing network activities will be disrupted."):
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

    # ----------------------------------FLUSH DNS END-------------------------------------------------
    # ----------------------------------ADGUARD HOME INSTALL HELPER-------------------------------------------------

    def agh_curl(self):
        print("Executing 'AdGuard Home' install helper.")

        def create_agh_window():
            agh_window = tk.Toplevel(self)
            agh_window.title("Copy to Clipboard?")
            agh_window.configure(bg=UI_COLOR)
            agh_window.grid_columnconfigure(0, weight=1)

            # Set window size and position
            window_width, window_height = 380, 300
            screen_width = agh_window.winfo_screenwidth()
            screen_height = agh_window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            agh_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

            message = tk.Label(agh_window,
                               text="This will copy the curl-command:\n\ncurl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v\n\nto your clipboard to assist in setting up AdGuard Home on a device like a Raspberry. Proceed?",
                               wraplength=280, bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
            message.grid(row=0, column=0, pady=10, padx=10)

            link = tk.Label(agh_window,
                            text="AdGuard Home GitHub Repository",
                            cursor="hand2",
                            fg=VERSION_LABEL_TEXT,
                            bg=UI_COLOR)
            link.grid(row=1, column=0, pady=5)

            def open_link(event):
                webbrowser.open(ADGUARD_LINK)

            def on_enter(event):
                link.config(fg="white")

            def on_leave(event):
                link.config(fg=VERSION_LABEL_TEXT)

            link.bind("<Button-1>", open_link)
            link.bind("<Enter>", on_enter)
            link.bind("<Leave>", on_leave)

            button_frame = tk.Frame(agh_window, bg=UI_COLOR)
            button_frame.grid(row=2, column=0, pady=10)
            button_frame.grid_columnconfigure((0, 1), weight=1)

            def on_yes():
                AdGuardClipBoard = "curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v"
                agh_window.clipboard_clear()
                agh_window.clipboard_append(AdGuardClipBoard)
                agh_window.update()
                print("Command copied to clipboard")
                agh_window.destroy()

            def on_no():
                print("Command execution canceled.")
                agh_window.destroy()

            def copy_dns_resolvers():
                dns_resolvers = """https://dns.quad9.net/dns-query
https://dns.google/dns-query
https://dns.cloudflare.com/dns-query"""
                agh_window.clipboard_clear()
                agh_window.clipboard_append(dns_resolvers)
                agh_window.update()
                print("DNS resolvers copied to clipboard")

            yes_button = tk.Button(button_frame, text="Yes", command=on_yes, width=20,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                   activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
            yes_button.grid(row=0, column=0, padx=5, pady=5)

            no_button = tk.Button(button_frame, text="No", command=on_no, width=20,
                                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                  activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
            no_button.grid(row=0, column=1, padx=5, pady=5)

            dns_button = tk.Button(agh_window, text="Copy DNS Resolvers", command=copy_dns_resolvers,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                   activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                                   width=20)
            dns_button.grid(row=3, column=0, pady=10)

        # Create the AGH window in a separate thread
        threading.Thread(target=create_agh_window, daemon=True).start()

    # ----------------------------------ADGUARD HOME INSTALL HELPER END-------------------------------------------------
    # ----------------------------------CHECKSUM HELPER-------------------------------------------------

    def get_file_checksum(self):
        print("Running file checksum helper.")
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showinfo("Info", "No file selected.")
            return

        # Create a new window for algorithm selection
        algo_window = tk.Toplevel(self)
        algo_window.title("Compute File Checksum")
        algo_window.geometry("400x210")
        algo_window.configure(bg=UI_COLOR)

        # Center the window
        algo_window.update_idletasks()
        width = algo_window.winfo_width()
        height = algo_window.winfo_height()
        x = (algo_window.winfo_screenwidth() // 2) - (width // 2)
        y = (algo_window.winfo_screenheight() // 2) - (height // 2)
        algo_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Create and pack a label
        label = tk.Label(algo_window, text="Choose a checksum algorithm:",
                         bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
        label.pack(pady=5)

        # Create a variable to hold the selected algorithm
        selected_algo = tk.StringVar()

        # Create a dropdown for algorithm selection
        algorithms = ["MD5", "SHA1", "SHA256", "SHA384", "SHA512"]
        algo_menu = tk.OptionMenu(algo_window, selected_algo, *algorithms)
        algo_menu.config(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                         activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                         highlightthickness=0, width=18)
        algo_menu["menu"].config(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        selected_algo.set("SHA256")  # Default value
        algo_menu.pack(pady=5)

        # Create a label to display the selected algorithm
        algo_label = tk.Label(algo_window, text="", bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
        algo_label.pack(pady=5)

        # Create a Text widget with Scrollbar to display the result
        result_frame = tk.Frame(algo_window, bg=UI_COLOR)
        result_frame.pack(pady=5, padx=10, expand=True, fill=tk.BOTH)

        result_text = tk.Text(result_frame, height=3, width=50, wrap=tk.WORD,
                              bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                              insertbackground=BUTTON_TEXT_COLOR)
        result_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        result_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)  # Make it read-only initially

        def run_checksum():
            algo = selected_algo.get()
            cmd = f'certutil -hashfile "{file_path}" {algo}'

            try:
                # Run the command and capture the output
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

                # Extract the checksum from the output
                checksum = result.stdout.split('\n')[1].strip()

                # Update the UI in the main thread
                algo_window.after(0, lambda: update_ui(algo, checksum))
            except subprocess.CalledProcessError as e:
                algo_window.after(0, lambda: messagebox.showerror("Error", f"An error occurred while computing the checksum:\n{e.stderr}"))
            except Exception as e:
                algo_window.after(0, lambda: messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}"))

        def update_ui(algo, checksum):
            # Update the algorithm label
            algo_label.config(text=f"Selected algorithm: {algo}")

            # Display only the checksum in the text widget
            result_text.config(state=tk.NORMAL)
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, checksum)
            result_text.config(state=tk.DISABLED)

        def on_compute():
            # Disable the button while computing
            button.config(state=tk.DISABLED)
            # Start the checksum computation in a separate thread
            threading.Thread(target=run_checksum, daemon=True).start()
            # Re-enable the button after a short delay
            algo_window.after(100, lambda: button.config(state=tk.NORMAL))

        # Create and pack a button
        button = tk.Button(algo_window, text="Compute Checksum", command=on_compute,
                           bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, width=20,
                           activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                           borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        button.pack(pady=10)

        # Don't make the window modal
        # algo_window.transient(self)
        # algo_window.grab_set()
        # self.wait_window(algo_window)

    # ----------------------------------CHECKSUM HELPER END-------------------------------------------------
    # ----------------------------------SYSTEM INFO COMPARE-------------------------------------------------

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
        print("Saving system info to .csv file.")
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Field', 'Value'])
            for key, value in info.items():
                if isinstance(value, list):
                    if key == 'Installed Software':
                        writer.writerow([key, ''])
                        for software in value:
                            writer.writerow(['', software])
                    else:
                        writer.writerow([key, ', '.join(value)])
                else:
                    writer.writerow([key, value])

    def gather_and_save_info(self):
        print("Extracting system info.")
        info = self.get_system_info()  # Gathers system info

        # Ask user if they want single system view or multi-system comparison
        choice = tk.messagebox.askquestion("Choose Option", "Do you want to view a single system?\nSelect: [Yes]\n\nOr prepare for multi-system comparison\nSelect: [No]")

        # Get default filename (hostname)
        default_filename = socket.gethostname()

        if choice == 'yes':  # Single system view
            save_path = filedialog.asksaveasfilename(
                defaultextension='.html',
                filetypes=[("HTML Files", "*.html")],
                initialfile=f"{default_filename}.html",
                title="Save HTML Report"
            )
            if save_path:
                self.save_to_html(info, save_path)
                os.startfile(save_path)  # Open the HTML file
        else:  # Multi-system comparison
            save_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[("CSV Files", "*.csv")],
                initialfile=f"{default_filename}.csv",
                title="Save CSV for Comparison"
            )
            if save_path:
                self.save_to_file(info, save_path)  # We still need this method for CSV creation

    def save_to_html(self, info, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('''
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; }
                    tr:nth-child(even) { background-color: #f2f2f2; }
                    th { padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #4CAF50; color: white; }
                </style>
            </head>
            <body>
                <h1>System Information</h1>
                <table>
                    <tr><th>Field</th><th>Value</th></tr>
            ''')

            for key, value in info.items():
                if isinstance(value, list):
                    if key == 'Installed Software':
                        file.write(f'<tr><td>{key}</td><td><ul>')
                        for software in value:
                            file.write(f'<li>{software}</li>')
                        file.write('</ul></td></tr>')
                    else:
                        file.write(f'<tr><td>{key}</td><td>{", ".join(value)}</td></tr>')
                else:
                    file.write(f'<tr><td>{key}</td><td>{value}</td></tr>')

            file.write('''
                </table>
            </body>
            </html>
            ''')

    def compare_system_info(self):
        file_paths = filedialog.askopenfilenames(
            title="Select CSV files for comparison",
            filetypes=[("CSV Files", "*.csv")])

        if not file_paths:
            return

        all_systems_info = [self.read_csv_file(path) for path in file_paths]
        differences = self.find_differences(all_systems_info)

        if differences:
            save_path = filedialog.asksaveasfilename(
                title="Save System Comparison Report",
                defaultextension=".html",
                filetypes=[("HTML Files", "*.html")],
                initialfile="SystemCompare.html")

            if save_path:
                self.write_differences_to_html(differences, save_path)
                os.startfile(save_path)  # Open the HTML file
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

    def write_differences_to_html(self, differences, file_path):
        print("Creating system comparison report.")
        with open(file_path, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write('''
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                    th, td { border: 1px solid #ddd; padding: 8px; }
                    tr:nth-child(even) { background-color: #f2f2f2; }
                    th { padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #4CAF50; color: white; }
                </style>
            </head>
            <body>
                <h1>System Comparison Report</h1>
            ''')

            for field, values in differences.items():
                htmlfile.write(f'<h2>{field}</h2>')
                htmlfile.write('<table><tr><th>Value</th><th>Files</th></tr>')
                for value, files in values.items():
                    file_names = [os.path.basename(f) for f in files]
                    file_names_with_count = f"{', '.join(file_names)} ({len(files)})"
                    htmlfile.write(f'<tr><td>{value}</td><td>{file_names_with_count}</td></tr>')
                htmlfile.write('</table>')

            htmlfile.write('</body></html>')

    def show_system_info(self):
        file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            return

        system_info = self.read_single_csv(file_path)

        save_path = filedialog.asksaveasfilename(
            title="Save System Info File",
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html")],
            initialfile="SystemInfo.html")

        if save_path:
            try:
                self.write_system_info_to_file(system_info, save_path)
            except PermissionError as e:
                messagebox.showerror("Permission Error", f"Permission denied: {str(e)}")

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

    # ----------------------------------SYSTEM INFO COMPARE END-------------------------------------------------

    def netstat_output(self):
        print("Executing Network Shell command to extract apps with active internet connection.")

        def get_netstat_data():
            try:
                result = subprocess.check_output('netstat -b -n -o', shell=True).decode('utf-8', errors='ignore')
                lines = result.split('\n')
                connections = []
                current_app = ""
                for line in lines:
                    if line.strip().startswith('TCP') or line.strip().startswith('UDP'):
                        parts = line.split()
                        if len(parts) >= 5:
                            state = parts[3] if len(parts) > 3 else "N/A"
                            if state == 'TIME_WAIT':
                                continue
                            protocol, local_address, foreign_address, pid = parts[0], parts[1], parts[2], parts[-1]
                            connections.append((protocol, local_address, foreign_address, state, pid, current_app))
                    elif '[' in line and ']' in line:
                        current_app = re.findall(r'\[(.*?)]', line)[0]
                return connections
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"An error occurred while executing the netstat command: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return []

        def check_online():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("Selection Required", "Please select at least one entry.")
                return
            for item in selected_items:
                appname = tree.item(item)['values'][-1]  # Get the app name (last column)
                google_query = f"https://www.google.com/search?q=Is+{appname}+safe"
                webbrowser.open(google_query)

        def update_ui(connections):
            netstat_window = tk.Toplevel(self)
            netstat_window.title("Apps with Active Internet Connection")
            netstat_window.configure(bg=BUTTON_BG_COLOR)

            window_width, window_height = 1550, 720
            screen_width = netstat_window.winfo_screenwidth()
            screen_height = netstat_window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            netstat_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

            # Create a frame to hold the Treeview and scrollbar
            frame = tk.Frame(netstat_window, bg=BUTTON_BG_COLOR)
            frame.pack(expand=True, fill='both', padx=10, pady=10)

            # Create Treeview
            global tree
            tree = ttk.Treeview(frame,
                                columns=("Protocol", "Local Address", "Foreign Address", "State", "PID", "App Name"),
                                show="headings", selectmode="extended")
            tree.heading("Protocol", text="Protocol")
            tree.heading("Local Address", text="Local Address")
            tree.heading("Foreign Address", text="Foreign Address")
            tree.heading("State", text="State")
            tree.heading("PID", text="PID")
            tree.heading("App Name", text="App Name")

            for col in tree["columns"]:
                tree.column(col, width=100, anchor="center")

            tree.column("Local Address", width=150)
            tree.column("Foreign Address", width=150)
            tree.column("App Name", width=200)

            # Configure Treeview colors
            style = ttk.Style(netstat_window)
            style.theme_use('default')
            style.configure("Treeview",
                            background=UI_COLOR,
                            foreground=BUTTON_TEXT_COLOR,
                            fieldbackground=UI_COLOR)
            style.map('Treeview',
                      background=[('selected', BUTTON_BG_COLOR)],
                      foreground=[('selected', BUTTON_TEXT_COLOR)])

            for conn in connections:
                tree.insert("", "end", values=conn)

            tree.pack(side="left", expand=True, fill="both")

            # Add vertical scrollbar
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

            # Add Check Online button at the bottom
            check_button = tk.Button(netstat_window, text="Check Online", command=check_online,
                                     bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
            check_button.pack(side='bottom', pady=10)

        # Run the netstat command in a separate thread
        def run_netstat():
            connections = get_netstat_data()
            self.after(0, update_ui, connections)

        threading.Thread(target=run_netstat, daemon=True).start()

    # -----------------------------------------------GODMODE--------------------------------------------------

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

    def get_root_dir(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return os.path.dirname(sys.executable)
        else:
            # Running as script
            return os.path.dirname(os.path.abspath(__file__))

    def open_super_godmode(self):
        print("Executing 'Windows-Super-God-Mode' Script")
        repo_url = "https://github.com/ThioJoe/Windows-Super-God-Mode"
        repo_name = "Windows-Super-God-Mode"
        bat_file = "SuperGodMode-EasyLauncher.bat"

        # Get the root directory of your application
        root_dir = self.get_root_dir()
        repo_path = os.path.join(root_dir, repo_name)

        # Check if the repository exists
        if not os.path.exists(repo_path):
            # Repository doesn't exist, ask user if they want to clone it
            user_response = messagebox.askyesno(
                "Clone Repository",
                f"The {repo_name} repository is not found. Do you want to clone it?"
            )

            if user_response:
                try:
                    subprocess.run(["git", "clone", repo_url, repo_path], check=True)
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Failed to clone repository: {str(e)}")
                    return
                except FileNotFoundError:
                    messagebox.showerror("Error", "Git is not installed or not in the system PATH.")
                    return
            else:
                return

        # Repository exists or has been cloned, proceed with git pull and running the bat file
        try:
            # Change to the repository directory
            os.chdir(repo_path)

            # Run git pull (ignoring errors)
            subprocess.run(["git", "pull"], check=False, capture_output=True)

            # Run the bat file
            subprocess.Popen(f"cmd /c {bat_file}", shell=True)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Change back to the original directory
            os.chdir(root_dir)

    # -----------------------------------------------GODMODE END--------------------------------------------------
    # -----------------------------------------------LOGOFF USER(S)--------------------------------------------------

    def logoff_user(self, username, session_id):
        print(f"Attempting to log off user: {username}")
        try:
            if session_id != 'N/A':
                subprocess.run(['logoff', session_id], check=True)
            else:
                # More robust username handling
                cmd = f'query session "{username}" | findstr "{username}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    session_line = result.stdout.strip()
                    if match := re.search(r'\s(\d+)\s', session_line):
                        session_id = match.group(1)
                        subprocess.run(['logoff', session_id], check=True)
                else:
                    raise subprocess.CalledProcessError(1, f'No session found for {username}')
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error logging off {username}: {e}")
            return False

    def logoff_users(self):
        print("Getting list of logged-in users.")
        self.users = []  # Make users a class instance variable

        def get_users_quser():
            try:
                result = subprocess.run(['quser'], capture_output=True, text=True,
                                        encoding='utf-8', errors='replace')
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, 'quser')
                output = result.stdout
                lines = output.strip().split('\n')
                for line in lines[1:]:  # Skip header line
                    match = re.match(r'>\s*(\S.*?)\s+(\d+)\s+', line) or \
                            re.match(r'\s*(\S.*?)\s+(\d+)\s+', line)
                    if match:
                        username = match.group(1).strip()
                        session_id = match.group(2)
                        self.users.append((username, session_id))  # Use self.users
            except subprocess.CalledProcessError:
                return False
            except Exception as e:
                print(f"Error in get_users_quser: {e}")
                return False
            return True

        def get_users_powershell():
            try:
                cmd = """
                Get-CimInstance -ClassName Win32_LoggedOnUser | 
                Select-Object -Property Antecedent | 
                ForEach-Object { 
                    $user = $_.Antecedent.ToString()
                    if ($user -match 'Domain="(.*?)",Name="(.*?)"') {
                        $matches[2]
                    }
                } | Sort-Object -Unique
                """
                result = subprocess.run(['powershell', '-NoProfile', '-Command', cmd],
                                        capture_output=True, text=True,
                                        encoding='utf-8', errors='replace')
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, 'powershell')
                output = result.stdout
                usernames = [u for u in output.strip().split('\n') if u.strip()]
                for username in usernames:
                    self.users.append((username.strip(), 'N/A'))  # Use self.users
            except Exception as e:
                print(f"Error in get_users_powershell: {e}")
                return False
            return True

        if not get_users_quser():
            if not get_users_powershell():
                messagebox.showerror("Error", "Failed to retrieve logged-in users.")
                return

        if not self.users:  # Use self.users
            messagebox.showinfo("Info", "No users found.")
            return

        window = tk.Toplevel(self)  # Changed from Tk() to Toplevel(self)
        window.title("Select Users to Log Off")
        window.configure(bg=UI_COLOR)

        window_width = 400
        window_height = 300
        window.geometry(f"{window_width}x{window_height}")
        window.resizable(False, False)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        window.geometry(f"+{x_cordinate}+{y_cordinate}")

        frame = tk.Frame(window, bg=UI_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50, bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for username, session_id in self.users:  # Use self.users
            listbox.insert(tk.END, f"{username} (Session ID: {session_id})")

        def on_submit():
            selected_indices = listbox.curselection()
            selected_users = [self.users[i] for i in selected_indices]  # Use self.users

            if not selected_users:
                messagebox.showinfo("Info", "No users selected.")
                return

            confirmation = messagebox.askyesno("Confirm",
                                               f"Are you sure you want to log off {len(selected_users)} user(s)?")
            if not confirmation:
                return

            success_count = 0
            for username, session_id in selected_users:
                if self.logoff_user(username, session_id):  # Added self.
                    success_count += 1
                    print(f"Logged off: {username} (Session ID: {session_id})")
                else:
                    messagebox.showerror("Error", f"Failed to log off {username}")

            messagebox.showinfo("Success",
                                f"Successfully logged off {success_count} out of {len(selected_users)} user(s).")
            window.destroy()

        button_frame = tk.Frame(window, bg=UI_COLOR)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        submit_button = tk.Button(button_frame, text="Log Off Selected Users", command=on_submit,
                                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        submit_button.pack(side=tk.LEFT, padx=(0, 5))

        cancel_button = tk.Button(button_frame, text="Cancel", command=window.destroy,
                                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        cancel_button.pack(side=tk.RIGHT)

        window.mainloop()

    # -----------------------------------------------LOGOFF USER(S) END--------------------------------------------------
    # -----------------------------------------------LINK SUMMARY--------------------------------------------------

    def open_links_window(self):
        print("Open Link summary.")
        window = tk.Toplevel(self)
        window.title("Download Links")
        window.resizable(True, True)
        window.configure(bg=UI_COLOR)

        main_frame = tk.Frame(window, bg=BUTTON_BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg=UI_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BUTTON_BG_COLOR)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.checkbox_vars = {}

        for category, items in links.items():
            category_frame = tk.LabelFrame(scrollable_frame, text=category, bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                           highlightbackground=UI_COLOR, highlightcolor=UI_COLOR,
                                           highlightthickness=5)
            category_frame.pack(fill="x", expand=True, padx=10, pady=5)

            num_columns = 3
            num_items = len(items)
            num_rows = (num_items + num_columns - 1) // num_columns

            for i, (text, link) in enumerate(items.items()):
                var = tk.IntVar()
                checkbox = tk.Checkbutton(category_frame, text=text, variable=var,
                                          bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                          selectcolor=BUTTON_BG_COLOR, activebackground=UI_COLOR,
                                          activeforeground=BUTTON_TEXT_COLOR)
                row = i % num_rows
                col = i // num_rows
                checkbox.grid(row=row, column=col, sticky="w", padx=10, pady=3)
                self.checkbox_vars[link] = var

            # Configure column weights to distribute space evenly
            for col in range(num_columns):
                category_frame.columnconfigure(col, weight=1)

        button_frame = tk.Frame(window, bg=UI_COLOR)
        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(button_frame, text="Open Links", command=lambda: self.on_ok(window), width=20,
                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                  activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                  borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE).pack(side="right", padx=5)

        tk.Button(button_frame, text="Cancel", command=window.destroy, width=20,
                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                  activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                  borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE).pack(side="right", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        window.update_idletasks()
        width = min(496, window.winfo_screenwidth() - 100)
        height = min(770, window.winfo_screenheight() - 100)
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_ok(self, window):
        for link, var in self.checkbox_vars.items():
            if var.get():
                webbrowser.open_new_tab(link)
        window.destroy()  # Close the window

    # -----------------------------------------------LINK SUMMARY END--------------------------------------------------

    # --------------VVVVVVVVVVVVVVVVVV--------------MAIN GUI SECTION BELOW HERE-----------------VVVVVVVVVVVVVVVVVVVV---------------

    # ------------------------------MAIN WINDOW/TABS/STYLES-------------------------------

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('default')

        # Configure tab padding and general styles
        style.configure('TNotebook.Tab', padding=[10, 7], background=BUTTON_BG_COLOR, foreground=BUTTON_TEXT_COLOR)
        style.configure('TNotebook', background=UI_COLOR)
        style.map('TNotebook.Tab', background=[('selected', UI_COLOR)])

        # Background color for the main frames
        style.configure('Functions.TFrame', background=f'{UI_COLOR}')
        style.configure('Options.TFrame', background=f'{UI_COLOR}')
        style.configure('Fun.TFrame', background=f'{UI_COLOR}')
        style.configure('Advanced.TFrame', background=f'{UI_COLOR}')
        style.configure('SystemTools.TFrame', background=f'{UI_COLOR}')
        style.configure('Utilities.TFrame', background=f'{UI_COLOR}')
        style.configure('Tools.TFrame', background=f'{UI_COLOR}')
        style.configure('Trouble.TFrame', background=f'{UI_COLOR}')
        style.configure('Netsh.TFrame', background=f'{UI_COLOR}')
        style.configure('Bottom.TFrame', background=f'{UI_COLOR}')

        # Define and configure a custom style for the buttons
        style.configure(
            'Custom.TButton',
            background=BUTTON_BG_COLOR,
            foreground=BUTTON_TEXT_COLOR,
            borderwidth=BORDER_WIDTH,
            relief=BUTTON_STYLE
        )

        # Map the style to handle button state changes
        style.map(
            'Custom.TButton',
            background=[('active', BUTTON_BG_COLOR)],  # This will handle button hover state
            foreground=[('active', BUTTON_TEXT_COLOR)]
        )

        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.pack(fill="both", expand=True)

        # Create frames with background colors
        self.functions_frame = tk.Frame(self.tabs, bg=UI_COLOR)
        self.options_frame = tk.Frame(self.tabs, bg=UI_COLOR)
        self.fun_frame = tk.Frame(self.tabs, bg=UI_COLOR)

        self.tabs.add(self.functions_frame, text="Scripts")
        self.tabs.add(self.options_frame, text="Options")
        self.tabs.add(self.fun_frame, text="Misc")

        # Options Notebook within the options tab
        options_notebook = ttk.Notebook(self.options_frame)
        options_notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # New Category Frames inside the Options tab
        advanced_windows_settings_frame = tk.Frame(options_notebook, bg=UI_COLOR)
        system_tools_frame = tk.Frame(options_notebook, bg=UI_COLOR)
        utilities_frame = tk.Frame(options_notebook, bg=UI_COLOR)
        tools_frame = tk.Frame(options_notebook, bg=UI_COLOR)
        trouble_frame = tk.Frame(options_notebook, bg=UI_COLOR)
        netsh_frame = tk.Frame(options_notebook, bg=UI_COLOR)

        # Adding new frames to the options notebook
        options_notebook.add(advanced_windows_settings_frame, text='Management')
        options_notebook.add(system_tools_frame, text='Security & Network')
        options_notebook.add(utilities_frame, text='System Tools')
        options_notebook.add(tools_frame, text='RDP & Environment')
        options_notebook.add(trouble_frame, text='Trouble & Optimize')
        options_notebook.add(netsh_frame, text='Shell Commands')

        # Packing the notebook into the options_frame
        options_notebook.pack(fill='both', expand=True, padx=25, pady=10)

        # Function to create buttons within a frame from a list of option tuples
        def create_option_buttons(frame, options_list):
            for i, option in enumerate(options_list):
                btn = tk.Button(frame, text=option[0], command=lambda cmd=option[1]: execute_command(cmd), width=20,
                                bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, activebackground=UI_COLOR,
                                activeforeground=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
                btn.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="we")

        # Create buttons in their distinct categories
        create_option_buttons(advanced_windows_settings_frame, windows_management_options)
        create_option_buttons(system_tools_frame, security_and_networking_options)
        create_option_buttons(utilities_frame, system_tools_options)
        create_option_buttons(tools_frame, remote_and_virtualization_options)
        create_option_buttons(trouble_frame, troubleshooting_and_optimization_options)
        create_option_buttons(netsh_frame, netsh_commands)

        # ------------------------------MAIN WINDOW/TABS/STYLES END-------------------------------
        # ------------------------------VERSION LABEL-------------------------------

        # Create a bottom frame for the version label
        bottom_frame = tk.Frame(self.main_frame, bg=UI_COLOR)
        bottom_frame.pack(side="bottom", fill="x")

        self.version_label = tk.Label(
            bottom_frame,  # Place the label in the bottom frame
            text=VERSION,
            anchor="se",
            cursor="hand2",
            fg=VERSION_LABEL_TEXT,
            bg=UI_COLOR,
        )
        self.version_label.pack(side="right", padx=5, pady=2)

        # Callback function for clicking the version label
        def open_link(event):
            webbrowser.open(WINFUNCT_LINK)

        # Bind the callback function to the version label
        self.version_label.bind("<Button-1>", open_link)

        # Optional: Change color on hover to provide visual feedback
        def on_enter(event):
            self.version_label.config(fg="white")  # Change text color on hover

        def on_leave(event):
            self.version_label.config(fg=VERSION_LABEL_TEXT)  # Restore original text color

        self.version_label.bind("<Enter>", on_enter)
        self.version_label.bind("<Leave>", on_leave)

        # ----------------------------VERSION LABEL END----------------------------
        # ----------------------------MAIN BUTTONS----------------------------

        # Script tab Buttons and Positions
        agh_curl_btn = tk.Button(self.functions_frame, text="AdGuard Install Helper", command=self.agh_curl, width=20,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        agh_curl_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        autostart_btn = tk.Button(self.functions_frame, text="Autostart Locations", command=self.open_autostart_locations, width=20,
                                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        autostart_btn.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        renew_ip_config_btn = tk.Button(self.functions_frame, text="Flush/Renew DNS", command=self.renew_ip_config,
                                        bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        renew_ip_config_btn.grid(row=0, column=2, padx=10, pady=5, sticky="we")

        logoff_usr_btn = tk.Button(self.functions_frame, text="Logoff Local User(s)", command=self.logoff_users, width=20,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        logoff_usr_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        open_links_btn = tk.Button(self.functions_frame, text="Open Link Summary", command=self.open_links_window, width=20,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        open_links_btn.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        checksum_btn = tk.Button(self.functions_frame, text="Verify File Checksum", command=self.get_file_checksum, width=20,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        checksum_btn.grid(row=1, column=2, padx=10, pady=5, sticky="we")

        wifi_btn = tk.Button(self.functions_frame, text="Wi-Fi Profile Info", command=self.show_wifi_networks, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        wifi_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        clear_icon_btn = tk.Button(self.functions_frame, text="Clear Icon Cache", command=self.icon_cache, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        clear_icon_btn.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        quick_access_btn = tk.Button(self.functions_frame, text="Quick Access Manager", command=self.quick_access_manager, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        quick_access_btn.grid(row=2, column=2, padx=10, pady=5, sticky="we")

        create_ctt_btn = tk.Button(self.functions_frame, text="Create CTT Shortcut",
                                     command=self.create_ctt_shortcut, width=20,
                                     bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                     relief=BUTTON_STYLE)
        create_ctt_btn.grid(row=3, column=0, padx=10, pady=5, sticky="we")

        restore_health_btn = tk.Button(self.functions_frame, text="Restore System Health",
                                   command=self.restore_health, width=20,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                   relief=BUTTON_STYLE)
        restore_health_btn.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        create_backup_window_btn = tk.Button(self.functions_frame, text="Backup and Restore",
                                       command=self.create_backup_window, width=20,
                                       bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                       relief=BUTTON_STYLE)
        create_backup_window_btn.grid(row=3, column=2, padx=10, pady=5, sticky="we")

        # ----------------------------MAIN BUTTONS END----------------------------
        # ----------------------------------DROPDOWN SECTION-------------------------------------------------

        # System Info Compare
        self.selected_function1 = tk.StringVar()
        self.selected_function1.set("*System Info*")

        self.function_dropdown1 = tk.OptionMenu(
            self.functions_frame,
            self.selected_function1,
            "*System Info*",
            "[1] Extract Sys Info",
            "[2] Compare Sys Info"
        )
        self.function_dropdown1.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown1["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown1.grid(row=1, column=4, padx=10, pady=5, sticky="we")
        self.selected_function1.trace('w', self.on_function_select1)

        # DROPDOWM WITH NUMBER [2] IS IN BOTTOM BORDER SECTION

        # God-mode
        self.selected_function3 = tk.StringVar()
        self.selected_function3.set("*God Mode*")

        self.function_dropdown3 = tk.OptionMenu(
            self.functions_frame,
            self.selected_function3,
            "*God Mode*",
            "[1] Simple God mode",
            "[2] Super God mode"
        )
        self.function_dropdown3.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown3["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown3.grid(row=2, column=4, padx=10, pady=5, sticky="we")
        self.selected_function3.trace('w', self.on_function_select3)

        # Admin Shells
        self.selected_function4 = tk.StringVar()
        self.selected_function4.set("*Admin Shells*")

        self.function_dropdown4 = tk.OptionMenu(
            self.functions_frame,
            self.selected_function4,
            "*Admin Shells*",
            "[1] cmd",
            "[2] PowerShell"
        )
        self.function_dropdown4.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown4["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown4.grid(row=0, column=4, padx=10, pady=5, sticky="we")
        self.selected_function4.trace('w', self.on_function_select4)

        # Check Online Status
        self.selected_function5 = tk.StringVar()
        self.selected_function5.set("*IP & Online Status*")

        self.function_dropdown5 = tk.OptionMenu(
            self.functions_frame,
            self.selected_function5,
            "*IP & Online Status*",
            "[1] PC online status",
            "[2] Website online status",
            "[3] Current IP info",
            "[4] Apps with internet connection",
            "[5] Execute <ping> command"
        )
        self.function_dropdown5.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown5["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown5.grid(row=1, column=3, padx=10, pady=5, sticky="we")
        self.selected_function5.trace('w', self.on_function_select5)

        # Interactive Shells
        self.selected_function6 = tk.StringVar()
        self.selected_function6.set("*Interactive Shells*")

        self.function_dropdown6 = tk.OptionMenu(
            self.functions_frame,
            self.selected_function6,
            "*Interactive Shells*",
            "[1] CTT Winutils",
            "[2] Activate Win/Office",
            "[3] Install/Upd. FFMPEG"
        )
        self.function_dropdown6.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown6["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown6.grid(row=0, column=3, padx=10, pady=5, sticky="we")
        self.selected_function6.trace('w', self.on_function_select6)

        # Disk utility
        self.selected_function7 = tk.StringVar()
        self.selected_function7.set("*Disk Operations*")

        self.function_dropdown7 = tk.OptionMenu(
            self.functions_frame,
            self.selected_function7,
            "*Disk Operations*",
            "[1] Disk Speedtest",
            "[2] Show Disk Info"
        )
        self.function_dropdown7.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown7["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown7.grid(row=2, column=3, padx=10, pady=5, sticky="we")
        self.selected_function7.trace('w', self.on_function_select7)

        # DROPDOWM WITH NUMBER [8] IS IN BOTTOM BORDER SECTION

        # ----------------------------------DROPDOWN SECTION END---------------------------------------------
        # ---------------------------------- TABS/FRAME FOR OPTION BUTTONS --------------------------------------------

        # Fun Notebook within the fun tab
        fun_notebook = ttk.Notebook(self.fun_frame)
        fun_notebook.pack(fill='both', expand=True, padx=25, pady=10)

        # New Category Frames inside the Fun tab
        apps_frame = tk.Frame(fun_notebook, bg=UI_COLOR)
        fun_stuff_frame = tk.Frame(fun_notebook, bg=UI_COLOR)

        # Adding new frames to the fun notebook
        fun_notebook.add(apps_frame, text='Tools')
        fun_notebook.add(fun_stuff_frame, text='Fun Stuff')

        # Packing the notebook into the fun_frame
        fun_notebook.pack(fill='both', expand=True, padx=25, pady=10)

        # Function to create buttons within a frame from a list of option tuples
        def create_fun_buttons(frame, buttons_list):
            for i, button in enumerate(buttons_list):
                btn = tk.Button(frame, text=button[0], command=button[1], width=20,
                                bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
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

        # Bottom frame
        self.bottom_frame = tk.Frame(self.main_frame, bg=UI_COLOR)
        self.bottom_frame.pack(fill="x", padx=5, pady=5)

        # ---------------------------------- TABS/FRAME FOR OPTION BUTTONS END --------------------------------------------
        # ---------------------------------- STATIC BOTTOM FRAME --------------------------------------------

        # Left-aligned buttons
        shutdown_btn = tk.Button(self.bottom_frame, text="Instant Shutdown", command=self.confirm_shutdown, width=20,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        shutdown_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        reboot_btn = tk.Button(self.bottom_frame, text="Forced Reboot", command=self.confirm_reboot, width=20,
                               bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        reboot_btn.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        uefi_btn = tk.Button(self.bottom_frame, text="Reboot to BIOS/UEFI", command=self.confirm_uefi, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        uefi_btn.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        sleep_btn = tk.Button(self.bottom_frame, text="Enter Hibernation", command=self.confirm_sleep, width=20,
                              bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        sleep_btn.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Spacer label to fill the space between left and right groups
        spacer = tk.Label(self.bottom_frame, background=f'{UI_COLOR}')
        spacer.grid(row=0, column=2, rowspan=2, sticky="we")
        self.bottom_frame.columnconfigure(2, weight=1)

        root_btn = tk.Button(self.bottom_frame, text="Open Root Folder", command=self.open_app_root_folder, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        root_btn.grid(row=1, column=4, padx=5, pady=5, sticky="we")

        exit_btn = tk.Button(self.bottom_frame, text="Exit Application", command=self.quit, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        exit_btn.grid(row=1, column=5, padx=5, pady=5, sticky="we")

        # UI utility
        self.selected_function8 = tk.StringVar()
        self.selected_function8.set("*GUI Options*")

        self.function_dropdown8 = tk.OptionMenu(
            self.bottom_frame,
            self.selected_function8,
            "*GUI Options*",
            "[1] Theme Selector",
            "[2] Reset UI"
        )
        self.function_dropdown8.config(
            width=18,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=UI_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            highlightthickness=0
        )
        self.function_dropdown8["menu"].config(
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR
        )
        self.function_dropdown8.grid(row=0, column=5, padx=10, pady=5, sticky="we")
        self.selected_function8.trace('w', self.on_function_select8)

        # FREE FOR NEW BUTTON / FUNCTION
        # self.selected_function2 = tk.StringVar()
        # self.selected_function2.set("*WHATEV*")
        #
        # self.function_dropdown2 = tk.OptionMenu(
        #     self.bottom_frame,
        #     self.selected_function2,
        #     "*WHATEV*",
        #     "[1] NEW OPTION",
        # )
        # self.function_dropdown2.config(
        #     width=18,
        #     bg=BUTTON_BG_COLOR,
        #     fg=BUTTON_TEXT_COLOR,
        #     activebackground=UI_COLOR,
        #     activeforeground=BUTTON_TEXT_COLOR,
        #     highlightthickness=0
        # )
        # self.function_dropdown2["menu"].config(
        #     bg=BUTTON_BG_COLOR,
        #     fg=BUTTON_TEXT_COLOR
        # )
        # self.function_dropdown2.grid(row=0, column=4, padx=10, pady=5, sticky="we")
        # self.selected_function2.trace('w', self.on_function_select2)

# ---------------------------------- STATIC BOTTOM FRAME END --------------------------------------------


app = Application()
app.mainloop()
