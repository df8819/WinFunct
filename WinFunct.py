# Standard Library Imports
import base64
import csv
import ctypes
import hashlib
import json
import logging
import os
import re
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

# noinspection PyUnresolvedReferences
# Local Imports
from config import (
    LOGO, VERSION_NUMBER, VERSION, VERSION_SHORT,
    UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR, BOTTOM_BORDER_COLOR, VERSION_LABEL_TEXT,
    BUTTON_STYLE, BORDER_WIDTH,
    LINK, AdGuardClipBoard,
    links, batch_script,
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


# noinspection PyUnresolvedReferences,PyProtectedMember
class GitUpdater:
    @staticmethod
    def is_frozen():
        return getattr(sys, 'frozen', False)

    @staticmethod
    def is_git_repository():
        try:
            subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def check_update_status():
        if GitUpdater.is_frozen() or not GitUpdater.is_git_repository():
            return False  # Ignore update check for frozen executable or non-Git repository
        try:
            # Run git fetch to get updates from the remote
            subprocess.run(['git', 'fetch'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Run git diff to check if there are updates
            result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True, check=True)
            return "Your branch is behind" in result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error checking update status: {e}")
            return False

    @staticmethod
    def prompt_update():
        if GitUpdater.check_update_status():
            user_choice = input(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   WinFunct update available. Do you want to update?   ║
    ║   Type [y/n] and press Enter to proceed...            ║
    ║         ‾ ‾                                           ║
    ║   Please restart after updating WinFunct.             ║
    ║          ‾‾‾‾‾‾‾                                      ║
    ╚═══════════════════════════════════════════════════════╝

    """).strip().lower()
            if user_choice == 'y':
                return True  # User wants to update
        return False

    @staticmethod
    def execute_update():
        try:
            if GitUpdater.is_frozen():
                print(f'Running as ".exe". Skipping update check. *{VERSION_SHORT}*')
            elif not GitUpdater.is_git_repository():
                print(f'Not running in a Git repository. Skipping update check. *{VERSION_SHORT}*')
            else:
                if GitUpdater.prompt_update():
                    print('Executing git pull...')
                    try:
                        subprocess.run(['git', 'pull'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        print('Repository updated. Restarting application...')

                        # Create a new window for the timer
                        root = tk.Tk()
                        root.title("Update Complete")
                        root.configure(bg=UI_COLOR)

                        # Set window size and position
                        window_width, window_height = 400, 120
                        screen_width = root.winfo_screenwidth()
                        screen_height = root.winfo_screenheight()
                        x = (screen_width // 2) - (window_width // 2)
                        y = (screen_height // 2) - (window_height // 2)
                        root.geometry(f'{window_width}x{window_height}+{x}+{y}')

                        label = tk.Label(root, text="Repository updated. The application will restart in 30 seconds.",
                                         bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
                        label.pack(pady=10)

                        def update_timer(seconds):
                            if seconds > 0:
                                label.config(text=f"Repository updated. The application will restart in {seconds} seconds.")
                                root.after(1000, update_timer, seconds - 1)
                            else:
                                root.destroy()
                                os._exit(0)  # This will immediately terminate the script

                        def manual_close():
                            root.destroy()
                            os._exit(0)  # This will immediately terminate the script

                        close_button = tk.Button(root, text="Close Now", command=manual_close,
                                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                                 activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
                        close_button.pack(pady=10)

                        # Start the timer
                        update_timer(30)

                        root.mainloop()

                    except subprocess.CalledProcessError as e:
                        print(f"Error during git pull: {e}")
                else:
                    print(f'No update needed. *{VERSION_SHORT}*')
        except Exception as e:
            print(f"An error occurred during the update process: {e}")
            print("Continuing with the current version.")


# Execute the update check before any class instantiation
GitUpdater.execute_update()


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
        cmd_line = ' '.join('"' + item.replace('"', '\\"') + '"' for item in cmd)
        try:
            log_message("Initial checks completed. Running as intended...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd_line, None, 1)
        except Exception as e:
            log_message(f"Error re-running the script with admin rights: {e}")


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
        if is_admin() or check_admin_cmd():
            print("Running with admin rights...")
            # Print log messages in the elevated terminal
            print_log()
        else:
            print("Not running with administrative privileges...")
            run_as_admin()
            # The script will exit here if not running as admin
            sys.exit()
    else:
        # Print log messages if running in an IDE
        print_log()


def show_logo():
    print(LOGO)


show_logo()
print(f"Awaiting user input (⌐■_■)")


# Command functions
def execute_command(cmd):
    print(f"Executing: {cmd}")
    subprocess.Popen(cmd, shell=True)


def load_theme_from_file():
    try:
        with open('last_selected_theme.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


# App Window
# noinspection PyTypeChecker,RegExpRedundantEscape,PyMethodMayBeStatic,PyUnusedLocal,PyShadowingNames,PyAttributeOutsideInit,SpellCheckingInspection,PyGlobalUndefined
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
            "[4] Apps with internet connection": lambda: self.netstat_output()
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
                if getattr(sys, 'frozen', False):
                    # Running as a PyInstaller executable
                    exe_dir = os.path.dirname(sys.executable)
                    ps_command = f'Set-Location "{exe_dir}"'
                else:
                    # Running as a script
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    ps_command = f'Set-Location "{script_dir}"'

                encoded_command = base64.b64encode(ps_command.encode('utf-16le')).decode('ascii')
                subprocess.run(f'powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \'-NoExit -EncodedCommand {encoded_command}\'"', shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PowerShell as admin: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

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

        for attempt in range(max_retries):
            try:
                ip_info = "========== Local ==========\n"

                # Fetch adapter names and IP addresses
                adapters = psutil.net_if_addrs()
                for adapter, addresses in adapters.items():
                    for addr in addresses:
                        if addr.family == 2:  # IPv4
                            ip_address = addr.address
                            ip_info += f"{adapter}:\n{ip_address}\n\n"

                ip_info += "\n========== Internet ==========\n"

                response = requests.get("https://ipapi.co/json/")
                data = response.json()

                ip_info += f"Public IP:     {data['ip']}\n"
                ip_info += f"ISP:           {data.get('org', 'N/A')}\n"
                ip_info += f"Country:       {data['country_name']}\n"
                ip_info += f"Region:        {data['region']}\n"
                ip_info += f"City:          {data['city']}\n"
                ip_info += f"Postal Code:   {data.get('postal', 'N/A')}\n\n"

                ip_info += "\n========== Topology ==========\n"

                ip_info += f"Latitude:      {data['latitude']}\n"
                ip_info += f"Longitude:     {data['longitude']}\n"
                ip_info += f"Timezone:      {data['timezone']}\n\n"

                ip_info += "\n========== Additional Info ==========\n"

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
                    ip_info = f"Error fetching IP information: {str(e)}"
                    break
            except Exception as e:
                ip_info = f"Error fetching IP information: {str(e)}"
                break

        ip_info_text.insert(tk.END, ip_info)
        ip_info_text.config(state='disabled')

    # ----------------------------------DISK INFO-------------------------------------------------

    def show_disk_info(self):
        print("Showing Disk Information")

        # Create a new window
        disk_window = tk.Toplevel(self)
        disk_window.title("Disk Information")
        disk_window.configure(bg=BUTTON_BG_COLOR)

        # Set window size and position
        window_width, window_height = 520, 600
        screen_width = disk_window.winfo_screenwidth()
        screen_height = disk_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        disk_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Create a text widget to display disk information
        disk_info_text = scrolledtext.ScrolledText(disk_window, wrap=tk.WORD, width=60, height=20,
                                                   bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                                   insertbackground=BUTTON_TEXT_COLOR)
        disk_info_text.pack(expand=True, fill='both', padx=10, pady=10)

        def fetch_disk_info():
            try:
                # Get list of disks
                disks_cmd = 'echo list disk | diskpart'
                disks_output = subprocess.check_output(disks_cmd, shell=True, text=True)

                # Filter out the DISKPART> prompts and empty lines
                cleaned_lines = [line.strip() for line in disks_output.split('\n') if line.strip() and not line.strip().startswith('DISKPART>')]

                # Process the cleaned lines
                processed_lines = []
                for line in cleaned_lines:
                    processed_lines.append(line)

                cleaned_output = '\n'.join(processed_lines)

                disk_info = """
    ========================
    *** Disk Information ***
    ========================

"""
                disk_info += cleaned_output + "\n\n"

                # Additional helpful information
                disk_info += """
    ==============================
    *** Additional Information ***
    ==============================

"""
                disk_info += "1. Disk Status:       Online/Offline\n"
                disk_info += "2. Partition Types:   Primary, Extended, Logical\n"
                disk_info += "3. File Systems:      NTFS, FAT32, exFAT\n"
                disk_info += "4. Disk Signature:    GPT or MBR\n"
                disk_info += "5. Free Space:        Check for unallocated space\n\n"
                disk_info += "Use 'chkdsk' for NTFS volumes to check disk health\n"

                disk_window.after(0, lambda: update_disk_info(disk_info))
            except Exception as e:
                error_message = f"Error fetching disk information: {str(e)}"
                disk_window.after(0, lambda: update_disk_info(error_message))

        def update_disk_info(info):
            disk_info_text.config(state='normal')
            disk_info_text.delete('1.0', tk.END)
            disk_info_text.insert(tk.END, info)
            disk_info_text.config(state='disabled')

        # Start fetching disk info in a separate thread
        threading.Thread(target=fetch_disk_info, daemon=True).start()

    # ----------------------------------DISK INFO END-------------------------------------------------
    # ----------------------------------WIFI PASSWORD EXTRACTION-------------------------------------------------

    def show_wifi_networks(self):
        print("""Extracting Wifi profiles.""")
        try:
            cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profiles"],
                                                 stderr=subprocess.STDOUT).decode("utf-8", "ignore")
            networks = re.findall(r"All User Profile\s*:\s*(.+)", cmd_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute netsh command: {e.output.decode('utf-8', 'ignore')}")
            return

        if networks:
            network_window = tk.Toplevel(self)
            network_window.title("Wi-Fi Networks")
            network_window.configure(bg=BUTTON_BG_COLOR)

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

            def ok_button_click():
                selected_index = network_listbox.curselection()
                if selected_index:
                    selected_network = network_listbox.get(selected_index[0])
                    self.show_wifi_password(selected_network)
                network_window.destroy()

            ok_button = tk.Button(network_window, text="Select", command=ok_button_click, width=10,
                                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                  relief=BUTTON_STYLE)
            ok_button.pack(side="left", padx=(5, 5), pady=10)

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
                        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network_profile, "key=clear"],
                                                             stderr=subprocess.STDOUT).decode("utf-8", "ignore")
                        password = re.search(r"Key Content\s*:\s*(.+)", cmd_output)
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

            extract_all_button = tk.Button(network_window, text="<ALL>", command=extract_all_passwords,
                                           width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                           relief=BUTTON_STYLE)
            extract_all_button.pack(side="left", padx=(5, 5), pady=10)

            def fast_extract_passwords():
                ssid_passwords = {}
                for network in networks:
                    network_profile = network.strip()
                    try:
                        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network_profile, "key=clear"],
                                                             stderr=subprocess.STDOUT).decode("utf-8", "ignore")
                        password = re.search(r"Key Content\s*:\s*(.+)", cmd_output)
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

            fast_extract_button = tk.Button(network_window, text="<AUTO>", command=fast_extract_passwords,
                                            width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                            relief=BUTTON_STYLE)
            fast_extract_button.pack(side="left", padx=(5, 5), pady=10)

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
            password_window.title(f"Information for {network}")
            password_window.configure(bg=UI_COLOR)

            window_width = 320
            window_height = 120
            screen_width = password_window.winfo_screenwidth()
            screen_height = password_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            password_window.resizable(False, False)

            password_frame = tk.Frame(password_window, bg=UI_COLOR)
            password_frame.pack(padx=20, pady=20)

            password_label = tk.Label(password_frame, text="Password:", bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
            password_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

            password_text = tk.Entry(password_frame, width=30, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
            password_text.insert(0, password.group(1))
            password_text.grid(row=0, column=1, padx=5, pady=5)

            def copy_password():
                self.clipboard_clear()
                self.clipboard_append(password_text.get())
                self.update()

            button_frame = tk.Frame(password_frame, bg=UI_COLOR)
            button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

            copy_button = tk.Button(button_frame, text="Copy", command=copy_password, width=10,
                                    bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                    relief=BUTTON_STYLE)
            copy_button.pack(side="left", padx=10)

            def cancel_button_click():
                password_window.destroy()

            cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_button_click, width=10,
                                      bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH,
                                      relief=BUTTON_STYLE)
            cancel_button.pack(side="left", padx=10)
        else:
            messagebox.showinfo(f"Wi-Fi Password for {network}", "No password found.")

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

    def activate_win(self):
        print("Activating Microsoft Products")

        def run_command():
            command = ['powershell.exe', '-Command', 'irm https://get.activated.win | iex']
            subprocess.run(command, shell=True)

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def activate_wui(self):
        print("Opening Windows Utility Improved")

        def run_command():
            command = ['powershell.exe', '-Command', 'irm christitus.com/win | iex']
            subprocess.run(command, shell=True)

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

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
        algo_window.geometry("400x250")
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
        label.pack(pady=10)

        # Create a variable to hold the selected algorithm
        selected_algo = tk.StringVar()

        # Create a dropdown for algorithm selection
        algorithms = ["MD5", "SHA1", "SHA256", "SHA384", "SHA512"]
        algo_menu = tk.OptionMenu(algo_window, selected_algo, *algorithms)
        algo_menu.config(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                         activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                         highlightthickness=0)
        algo_menu["menu"].config(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)
        selected_algo.set("SHA256")  # Default value
        algo_menu.pack(pady=10)

        # Create a label to display the selected algorithm
        algo_label = tk.Label(algo_window, text="", bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
        algo_label.pack(pady=5)

        # Create a Text widget with Scrollbar to display the result
        result_frame = tk.Frame(algo_window, bg=UI_COLOR)
        result_frame.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

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
        button = tk.Button(algo_window, text="Compute Checksum", command=run_checksum,
                           bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                           activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR,
                           borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        button.pack(pady=10)

        # Make the window modal
        algo_window.transient(self)
        algo_window.grab_set()
        self.wait_window(algo_window)

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

    # Detect Apps with an active internet connection
    def netstat_output(self):
        print("Executing Network Shell command to extract apps with active internet connection.")
        try:
            # Execute the netstat command and capture the output
            result = subprocess.check_output('netstat -b -n', shell=True).decode()

            # Process the command output
            lines = result.split('\n')
            processed_lines = [re.findall(r'\[(.*?)]', line) for line in lines]
            processed_lines = [item for sublist in processed_lines for item in sublist]
            unique_lines = list(set(processed_lines))

            # Create a new window to display the apps with active internet connection
            netstat_window = tk.Toplevel(self)
            netstat_window.title("Apps with Active Internet Connection")
            netstat_window.configure(bg=BUTTON_BG_COLOR)

            # Set window size and position
            window_width, window_height = 420, 580
            screen_width = netstat_window.winfo_screenwidth()
            screen_height = netstat_window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            netstat_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

            # Create a text widget to display the apps
            app_text = scrolledtext.ScrolledText(netstat_window, wrap=tk.WORD, width=40, height=10,
                                                 bg=UI_COLOR, fg=BUTTON_TEXT_COLOR,
                                                 insertbackground=BUTTON_TEXT_COLOR)
            app_text.pack(expand=True, fill='both', padx=10, pady=10)

            # Insert the apps into the text widget
            for line in unique_lines:
                app_text.insert(tk.END, line + '\n')

            app_text.config(state='disabled')  # Make the text widget read-only

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while executing the netstat command: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # -----------------------------------------------CLONE REPO--------------------------------------------------

    def git_pull(self):
        # Determine if we're running as a script or frozen executable
        if getattr(sys, 'frozen', False):
            # We're running in a PyInstaller bundle
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))  # Use default if _MEIPASS not present
            repo_path = os.path.dirname(sys.executable)

            print(f"""
    ╔═════════════════════════════════ERROR═════════════════════════════════════╗
    ║ You are NOT running WinFunct from a python file!                          ║
    ║ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                          ║
    ║ Please download the latest Release from GitHub                            ║
    ║                                                                           ║
    ║                               ---OR---                                    ║
    ║                                                                           ║
    ║ Clone this repository from GitHub via 'Get from GitHub' button            ║
    ║ and execute 'Run' to start the app to make use of the 'Update' function.  ║
    ║                                                                           ║
    ║ Make sure "Git for Windows" and "Python 3.x" is installed or this         ║
    ║ function will produce an Error!                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
""")

            if messagebox.askyesno("Open GitHub Releases",
                                   "Open the WinFunct GitHub 'Releases' section in the default browser?\n\n(Read the terminal message for more information)"):
                webbrowser.open("https://github.com/df8819/WinFunct/releases")
            else:
                print("Command aborted.")

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
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("300x100")
        window.configure(bg=UI_COLOR)

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

        progress_label = tk.Label(window, text="Starting...",
                                  bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
        progress_label.pack(pady=10)

        # Create a style for the progress bar
        style = ttk.Style(window)
        style.theme_use('default')
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor=UI_COLOR,
                        background=BUTTON_BG_COLOR,
                        darkcolor=BUTTON_BG_COLOR,
                        lightcolor=BUTTON_BG_COLOR)

        progress_bar = ttk.Progressbar(window, mode="indeterminate", length=200,
                                       style="Custom.Horizontal.TProgressbar")
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
            print(f"Missing dependencies: {missing_deps}")
            self.notify_missing_dependencies(missing_deps)
            return False
        else:
            print("All dependencies are installed.")
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
            return

        self.clone_repository("https://github.com/df8819/WinFunct.git", clone_path)

    # -----------------------------------------------CLONE REPO END--------------------------------------------------
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

    def logoff_users(self):
        print("""Running 'quser' command to get list of logged-in users.""")
        try:
            result = subprocess.run(['quser'], capture_output=True, text=True, encoding='cp850', errors='replace', shell=True)
            output = result.stdout
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run 'quser': {e}")
            return

        if output is None:
            messagebox.showerror("Error", "No output from 'quser'.")
            return

        lines = output.strip().split('\n')
        users = []

        for line in lines[1:]:
            match = re.match(r'^\s*(.*?)\s+(\d+)\s+\w+', line)
            if match:
                username = match.group(1).strip()
                session_id = match.group(2)
                users.append((username, session_id))

        if not users:
            messagebox.showinfo("Info", "No users found.")
            return

        window = tk.Tk()
        window.title("Select Users to Log Off")
        window.configure(bg=UI_COLOR)

        window_width = 400
        window_height = 300
        window.geometry(f"{window_width}x{window_height}")

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
            webbrowser.open(LINK)

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
        agh_curl_btn = tk.Button(self.functions_frame, text="AdGuard curl-copy", command=self.agh_curl, width=20,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        agh_curl_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        autostart_btn = tk.Button(self.functions_frame, text="Autostart locations", command=self.open_autostart_locations, width=20,
                                  bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        autostart_btn.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        renew_ip_config_btn = tk.Button(self.functions_frame, text="Flush/Renew DNS", command=self.renew_ip_config,
                                        bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        renew_ip_config_btn.grid(row=0, column=2, padx=10, pady=5, sticky="we")

        clone_btn = tk.Button(self.functions_frame, text="Get from GitHub", command=self.clone_repo_with_prompt, width=20,
                              bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        clone_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        logoff_usr_btn = tk.Button(self.functions_frame, text="Logoff local user(s)", command=self.logoff_users, width=20,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        logoff_usr_btn.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        open_links_btn = tk.Button(self.functions_frame, text="Open Link Summary", command=self.open_links_window, width=20,
                                   bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        open_links_btn.grid(row=1, column=2, padx=10, pady=5, sticky="we")

        checksum_btn = tk.Button(self.functions_frame, text="Verify file checksum", command=self.get_file_checksum, width=20,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        checksum_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        wifi_btn = tk.Button(self.functions_frame, text="Wi-Fi Profile Info", command=self.show_wifi_networks, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        wifi_btn.grid(row=2, column=1, padx=10, pady=5, sticky="we")

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
            width=17,
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

        # NEW DROPDOWM WITH NUMBER [2] ######################

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
            width=17,
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
            width=17,
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
            "[4] Apps with internet connection"
        )
        self.function_dropdown5.config(
            width=17,
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
            width=17,
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
            width=17,
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
        shutdown_btn = tk.Button(self.bottom_frame, text="Shutdown", command=self.confirm_shutdown, width=20,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        shutdown_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        reboot_btn = tk.Button(self.bottom_frame, text="Reboot", command=self.confirm_reboot, width=20,
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

        exit_btn = tk.Button(self.bottom_frame, text="Exit", command=self.quit, width=20,
                             bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        exit_btn.grid(row=1, column=5, padx=5, pady=5, sticky="we")

        update_btn = tk.Button(self.bottom_frame, text="Update WinFunct", command=self.git_pull, width=20,
                               bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE)
        update_btn.grid(row=0, column=4, padx=5, pady=5, sticky="we")

        # UI utility
        self.selected_function8 = tk.StringVar()
        self.selected_function8.set("GUI Options")

        self.function_dropdown8 = tk.OptionMenu(
            self.bottom_frame,
            self.selected_function8,
            "GUI Options",
            "[1] Theme Selector",
            "[2] Reset UI"
        )
        self.function_dropdown8.config(
            width=17,
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


# ---------------------------------- STATIC BOTTOM FRAME END --------------------------------------------


app = Application()
app.mainloop()
