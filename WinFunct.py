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
import threading
import time

# Tkinter Imports
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
# import ttkbootstrap as ttk
# from ttkbootstrap import Style
import webbrowser
import winreg

# Third-Party Imports
import requests
import wmi

# Local Imports
from HashStuffInt import HashStuff
from JChatInt import JChat
from SimplePWGenInt import SimplePWGen

# Version of the app
VERSION = "Use at your own risk and responsibility - v1.624"

# GitHub repo link
LINK = "https://github.com/df8819/WinFunct"

# The curl-command to copy to the clipboard
command = 'curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s ' \
          '-- -v'


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

    # Your normal script execution for both admin and non-admin mode continues here
    print(f"\n...Now running with admin rights. Nice (⌐■_■)\n")


# Command functions
def execute_command(cmd):
    subprocess.Popen(cmd, shell=True)


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


# App Window
# noinspection PyMethodMayBeStatic,PyShadowingNames
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resolution_main = "660x520"
        self.tabs = None
        self.checkbox_vars = None
        self.fun_frame = None
        self.options_frame = None
        self.create_user = None
        self.ip_text = None
        self.functions_frame = None
        self.bottom_frame = None
        self.geometry(self.resolution_main)
        self.center_window()
        self.title("Windows Functionalities --- (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
        self.font_family = "Segoe UI Emoji"

        # Setting the background color of the main frame to light blue
        self.main_frame = ttk.Frame(self, style='LightBlue.TFrame')

        # Creating a style (Delete this to delete style)
        style = ttk.Style()
        style.configure('LightBlue.TFrame', background='#4791cc')

        # Initial code for non-style:
        # self.main_frame = ttk.Frame(self)


        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()
        self.resizable(True, True)

    def center_window(self):
        self.update_idletasks()  # Ensures the geometry is calculated
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_top = int(self.winfo_screenheight() / 2 - window_height / 2)

        self.geometry(f"+{position_right}+{position_top}")

    def reset_ui(self):
        self.geometry(self.resolution_main)
        self.center_window()

    def open_chat(self):
        if tk.messagebox.askyesno("Open JChat", "This will open a chat-app GUI that requires an OpenAI API Key.\n\nSelect 'No' if you don't have your personal Key yet."):
            chat_window = tk.Toplevel(self)
            chat_window.title("JChat")
            JChat(chat_window)  # Initialize JChat within the new window

    def open_pw_gen(self):
        pw_window = tk.Toplevel(self)
        pw_window.title("Password Generator")
        SimplePWGen(pw_window)

    def open_hash_stuff(self):
        hash_window = tk.Toplevel(self)
        hash_window.title("Hash Generator")
        HashStuff(hash_window)

    def open_app_root_folder(self):
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
        def run_command():
            try:
                subprocess.run('powershell Start-Process powershell -Verb runAs', shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PowerShell as admin: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def open_cmd_as_admin(self):
        def run_command():
            try:
                subprocess.run('start cmd.exe /k cd C:\\ & title Command Prompt as Admin', shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Command Prompt as admin: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def open_autostart_locations(self):
        # Folder locations
        user_startup_path = os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        all_users_startup_path = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp'

        # Open folder locations
        if os.path.exists(user_startup_path):
            os.startfile(user_startup_path)
        if os.path.exists(all_users_startup_path):
            os.startfile(all_users_startup_path)

    def show_ip_address(self):
        response = requests.get("https://ifconfig.me/ip")
        ip_address = response.text
        self.ip_text.delete(0, tk.END)
        self.ip_text.insert(tk.END, ip_address)

        # Schedule the removal of the IP address
        self.ip_text.after(3000, self.clear_ip_text)

    def clear_ip_text(self):
        self.ip_text.delete(0, tk.END)

    def show_wifi_networks(self):
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
                powershell_command = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/k winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
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
            print("Command was cancelled.")

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
            print("Command was cancelled.")


    def shutdown_i(self):
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

    def enhanced_bloatware_killer(self):
        def run_uninstall(items, is_app):
            for item in items:
                if is_app:
                    command = f'powershell.exe Get-AppxPackage *{item}* | Remove-AppxPackage'
                else:
                    command = f'powershell.exe Get-AppxProvisionedPackage -Online | Where-Object DisplayName -like *{item}* | Remove-AppxProvisionedPackage -Online'

                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                result = "Success" if process.returncode == 0 else "Failed"
                log_text.insert(tk.END, f"{'App' if is_app else 'PWA'}: {item} - {result}\n")
                log_text.see(tk.END)
                progress['value'] += 1

            if is_app:
                selected_pwas = [pwa for pwa in pwas_to_unregister if pwa_vars[pwa].get()]
                run_uninstall(selected_pwas, False)
            else:
                messagebox.showinfo("Bloatware Killer", "Uninstallation process completed.")
                start_button['state'] = 'normal'

        def start_uninstall():
            if not any(app_vars[app].get() for app in apps_to_uninstall) and not any(
                    pwa_vars[pwa].get() for pwa in pwas_to_unregister):
                messagebox.showwarning("No Selection", "Please select at least one item to uninstall.")
                return

            if not messagebox.askokcancel("Confirm Uninstallation",
                                       "Are you sure you want to uninstall the selected items?\n\nWARNING: This process cannot be undone!\n\nThis is still a bit messed up. I recommend using the \n>>>CTT Winutil<<< \nbutton/function in this app for de-bloat your system."):
                return

            start_button['state'] = 'disabled'
            log_text.delete(1.0, tk.END)
            progress['maximum'] = sum(app_vars[app].get() for app in apps_to_uninstall) + sum(
                pwa_vars[pwa].get() for pwa in pwas_to_unregister)
            progress['value'] = 0

            selected_apps = [app for app in apps_to_uninstall if app_vars[app].get()]
            threading.Thread(target=run_uninstall, args=(selected_apps, True), daemon=True).start()

        def select_all():
            for var in list(app_vars.values()) + list(pwa_vars.values()):
                var.set(True)

        def unselect_all():
            for var in list(app_vars.values()) + list(pwa_vars.values()):
                var.set(False)

        # Create main window
        top = tk.Toplevel(self.master)
        top.title("Enhanced Bloatware Killer")
        top.geometry("560x780")

        top.update_idletasks()

        width = top.winfo_width()
        height = top.winfo_height()
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        top.geometry(f'{width}x{height}+{x}+{y}')

        # Create notebook for tabs
        notebook = ttk.Notebook(top)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create frames for each tab
        apps_frame = ttk.Frame(notebook)
        pwas_frame = ttk.Frame(notebook)
        notebook.add(apps_frame, text="Apps")
        notebook.add(pwas_frame, text="PWAs")

        # Create checkbuttons for apps and PWAs
        app_vars = {app: tk.BooleanVar(value=True) for app in apps_to_uninstall}
        pwa_vars = {pwa: tk.BooleanVar(value=True) for pwa in pwas_to_unregister}

        for i, app in enumerate(apps_to_uninstall):
            ttk.Checkbutton(apps_frame, text=app, variable=app_vars[app]).grid(row=i // 2, column=i % 2, sticky="w",
                                                                               padx=5, pady=2)

        for i, pwa in enumerate(pwas_to_unregister):
            ttk.Checkbutton(pwas_frame, text=pwa, variable=pwa_vars[pwa]).grid(row=i // 2, column=i % 2, sticky="w",
                                                                               padx=5, pady=2)

        # Create log text area
        log_frame = ttk.Frame(top)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        log_text = tk.Text(log_frame, height=10)
        log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        log_text.configure(yscrollcommand=scrollbar.set)

        # Create progress bar
        progress = ttk.Progressbar(top, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=10)

        # Create a frame for buttons
        button_frame = ttk.Frame(top)
        button_frame.pack(pady=10)

        # Create Select All button
        select_all_button = ttk.Button(button_frame, text="Select All", command=select_all)
        select_all_button.pack(side=tk.LEFT, padx=5)

        # Create Unselect All button
        unselect_all_button = ttk.Button(button_frame, text="Unselect All", command=unselect_all)
        unselect_all_button.pack(side=tk.LEFT, padx=5)

        # Create start button
        start_button = ttk.Button(button_frame, text="Start Uninstallation", command=start_uninstall)
        start_button.pack(side=tk.LEFT, padx=5)

        top.mainloop()

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
            print("Command was cancelled.")

    def agh_curl(self):
        # Copy the command to the clipboard using the 'clip' command on Windows
        subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(input=command.encode())
        print('Command copied to clipboard!')

    def arp(self):
        def run_command():
            # Command to open a new PowerShell window and run 'arp -a'
            command = 'powershell.exe arp -a'
            subprocess.run(command, shell=True)

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def get_file_checksum(self):
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
            messagebox.showinfo("Cancelled", "No files were selected.")
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
            messagebox.showinfo("Cancelled", "No file was selected.")
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
                        param = '-n' if subprocess.sys.platform.lower() == 'win32' else '-c'
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
                        success, message = True, f"{method_name} (8.8.8.8 -Port 53) connection successful"
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

    def git_pull(self):
        # Determine if we're running as a script or frozen executable
        if getattr(sys, 'frozen', False):
            # We're running in a PyInstaller bundle
            base_path = sys._MEIPASS
            repo_path = os.path.dirname(sys.executable)
            print(">>>>> You are running WinFunct from an .exe. Please clone the repository from github via 'Get from GitHub' button to make use of the 'Update' function. <<<<<")
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
                print("Update detected. Notifying user...")
                self.notify_user_of_update(full_output)

                # Check if requirements.txt has changed by comparing hashes
                after_pull_hash = self.file_hash(requirements_path) if os.path.exists(requirements_path) else None
                if before_pull_hash != after_pull_hash:
                    print("requirements.txt has changed. Installing new requirements...")
                    self.install_requirements(requirements_path)
            else:
                print("No updates available.")

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

            print("Requirements installed successfully.")
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
        """Show a message box with options to download missing dependencies."""
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
        """Clone the repository into the selected path."""
        repo_name = repo_url.split('/')[-1][:-4]  # Extract repo name
        final_clone_path = os.path.join(clone_path, repo_name)

        try:
            subprocess.run(["git", "clone", repo_url, final_clone_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            messagebox.showinfo("Repository Cloned", f"Repository cloned successfully into {final_clone_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to clone repository: {e.stderr.strip()}")  # Improved: Strip extra whitespace

    def clone_repo_with_prompt(self):
        """Check dependencies, prompt user for directory, and clone the repository."""
        if not self.check_dependencies():
            messagebox.showerror("Missing Dependencies", "Git and/or Python are not installed.")
            return

        clone_path = self.select_clone_directory()
        if clone_path is None:
            messagebox.showwarning("Clone Cancelled", "Repository clone cancelled. No directory selected.")
            return

        self.clone_repository("https://github.com/df8819/WinFunct.git", clone_path)

    def open_godmode(self):
        def run_command():
            try:
                subprocess.run("explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}", shell=True)
            except Exception as e:
                print(f"Error: {e}")

        # Run the command in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=run_command)
        thread.start()

    def open_links_window(self):
        links = {
            "Dev Tools": {
                "Python": "https://www.python.org/downloads/",
                "Git": "https://git-scm.com/downloads",
                "GitHub Desktop": "https://desktop.github.com",
                "Visual Studio Code": "https://code.visualstudio.com/download",
                "PyCharm": "https://www.jetbrains.com/pycharm/download/?section=windows",
                "UPX Packer": "https://github.com/upx/upx/releases",
                "Rust/Cargo": "https://rustup.rs",
                "Qt Designer": "https://build-system.fman.io/qt-designer-download",
            },
            "Network Tools": {
                "AirCrack": "https://www.aircrack-ng.org",
                "Wifi-Cracker": "https://github.com/trevatk/Wifi-Cracker",
                "WireShark": "https://www.wireshark.org/download.html",
                "Advanced IP Scanner": "https://www.advanced-ip-scanner.com/de/",
                "PuTTY (SSH)": "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html",
                "TCPView": "https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview",
            },
            "System Utilities": {
                "Process Explorer": "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer",
                "HxD Hex Editor": "https://mh-nexus.de/en/programs.php",
                "HWInfo64": "https://www.hwinfo.com/download/",
                "MSI Afterburner": "https://www.msi.com/Landing/afterburner/graphics-cards",
                "WinDirStat": "https://sourceforge.net/projects/windirstat/",
                "O&O ShutUp10++": "https://www.oo-software.com/de/shutup10",
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
            },
            "Productivity": {
                "PicPick": "https://picpick.app/en/download/",
                "Notepad++": "https://notepad-plus-plus.org/downloads/v8.5.8/",
                "Total Commander": "https://www.ghisler.com/ddownload.htm",
                "NetManSet": "https://www.netsetman.com/en/freeware",
                "Posy Cursors": "http://www.michieldb.nl/other/cursors",
                "Bitwarden": "https://bitwarden.com/download/",
            },
            "Tutorials & Resources": {
                "MAS Script": "https://massgrave.dev/index.html",
                "AdGuard Home": "https://youtu.be/B2V_8M9cjYw?si=Z_AeA4hCFGiElOHB",
                "NSE Lab": "https://nse.digital",
                "Wifi-Hack": "https://hackernoon.com/how-to-hack-wifi-like-a-pro-hacker",
            },
        }

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
                checkbox.grid(row=i // 2, column=i % 2, sticky="w", padx=5, pady=2)
                self.checkbox_vars[link] = var

        button_frame = ttk.Frame(window)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Open Links", command=lambda: self.on_ok(window)).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=window.destroy).pack(side="right", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        window.update_idletasks()
        width = min(340, window.winfo_screenwidth() - 100)
        height = min(750, window.winfo_screenheight() - 100)
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_ok(self, window):
        for link, var in self.checkbox_vars.items():
            if var.get():
                webbrowser.open_new_tab(link)
        window.destroy()  # Close the window

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.main_frame)

        # These are your original tabs
        self.functions_frame = ttk.Frame(self.tabs)  # Renamed from functions_frame for clarity
        self.options_frame = ttk.Frame(self.tabs)
        self.fun_frame = ttk.Frame(self.tabs)

        self.tabs.add(self.functions_frame, text="Scripts")
        self.tabs.add(self.options_frame, text="Options")
        self.tabs.add(self.fun_frame, text="Apps")

        self.tabs.pack(fill="both", expand=True)

        # Options Notebook within the options tab
        options_notebook = ttk.Notebook(self.options_frame)

        # New Category Frames inside the Options tab
        advanced_windows_settings_frame = ttk.Frame(options_notebook)
        system_tools_frame = ttk.Frame(options_notebook)
        utilities_frame = ttk.Frame(options_notebook)
        tools_frame = ttk.Frame(options_notebook)
        trouble_frame = ttk.Frame(options_notebook)
        netsh_frame = ttk.Frame(options_notebook)

        # Adding new frames to the options notebook
        options_notebook.add(advanced_windows_settings_frame, text='Management')
        options_notebook.add(system_tools_frame, text='Security & Network')
        options_notebook.add(utilities_frame, text='System Tools')
        options_notebook.add(tools_frame, text='RDP & Environment')
        options_notebook.add(trouble_frame, text='Trouble & Optimize')
        options_notebook.add(netsh_frame, text='Network Shell')

        # Packing the notebook into the options_frame
        options_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Categorized options lists
        # Note: You might need to adjust these lists based on your application's requirements
        # Windows Management and Configuration Tools
        windows_management_options = [
            ("RegEdit", "regedit"),
            ("PC Mgr", "compmgmt.msc"),
            ("Event Viewer", "eventvwr.msc"),
            ("Services", "services.msc"),
            ("GPO", "gpedit.msc"),
            ("Programs", "appwiz.cpl"),
            ("Win Version", "winver"),
            ("Adv Sys Set", "SystemPropertiesAdvanced"),
            ("UAC", "useraccountcontrolsettings"),
            ("Disk Mgr", "diskmgmt.msc"),
            ("Local Users", "lusrmgr.msc"),
            ("Sys Name", "SystemPropertiesComputerName"),
            ("ODBC", "odbcad32"),
            ("Shared Folders", "fsmgmt.msc"),
            ("Mobility", "mblctr"),
        ]

        # Security and Networking Tools
        security_and_networking_options = [
            ("Sec Center", "start ms-settings:windowsdefender"),
            ("Sec Policy", "secpol.msc"),
            ("FW Adv", "wf.msc"),
            ("Net Sharing", "control /name Microsoft.NetworkAndSharingCenter"),
            ("Internet Opt", "inetcpl.cpl"),
            ("Cred Mgr", "control /name Microsoft.CredentialManager"),
            ("Firewall", "firewall.cpl"),
            ("Net Adapts", "ncpa.cpl"),
            ("DNS Cache", "ipconfig /displaydns"),
            ("Remote Conn", "control /name Microsoft.RemoteAppAndDesktopConnections"),
            ("VPN", "start ms-settings:network-vpn"),
            ("Wi-Fi", "start ms-settings:network-wifi"),
            ("Ethernet", "start ms-settings:network-ethernet"),
            ("Proxy", "start ms-settings:network-proxy"),
        ]

        # System Tools and Utilities
        system_tools_options = [
            ("Hosts File", "notepad C:\\Windows\\System32\\drivers\\etc\\hosts"),
            ("Task Manager", "taskmgr"),
            ("Control Panel", "control"),
            ("Device Manager", "devmgmt.msc"),
            ("Performance Mon", "perfmon"),
            ("Resource Mon", "resmon"),
            ("Device Pair", "devicepairingwizard"),
            ("Win Features", "optionalfeatures"),
            ("System Info", "msinfo32"),
        ]

        # Remote Management and Virtualization Tools
        remote_and_virtualization_options = [
            ("RDP", "mstsc"),
            ("RDP Settings", "start ms-settings:remotedesktop"),
            ("Hyper-V", "C:\\Windows\\System32\\virtmgmt.msc"),
            ("Environ Vari", "rundll32.exe sysdm.cpl,EditEnvironmentVariables"),
        ]

        # Troubleshooting and Optimization Tools
        troubleshooting_and_optimization_options = [
            ("Rel Mon", "perfmon /rel"),
            ("Disk Clean", "cleanmgr"),
            ("Sys Restore", "rstrui"),
            ("Opt Drives", "dfrgui"),
            ("Memory Diag", "MdSched"),
            ("DirectX Diag", "dxdiag"),
            ("Sys Config", "msconfig"),
            ("Win Update", "start ms-settings:windowsupdate"),
        ]

        netsh_commands = [
            ("IP Config", "netsh interface ip show config"),
            ("Interface", "netsh interface show interface"),
            ("IPv4 Interface", "netsh interface ipv4 show interface"),
            ("IPv6 Interface", "netsh interface ipv6 show interface"),
            ("IP Address", "netsh interface ip show addresses"),
            ("DNS Configs", "netsh interface ip show dns"),
            ("FW State", "netsh advfirewall show currentprofile state"),
            ("Routing Table", "netsh interface ipv4 show route"),
            ("WiFi Profiles", "netsh wlan show profiles"),
            ("WiFi Settings", "netsh wlan show settings"),
            ("WiFi Netwroks", "netsh wlan show networks"),
            ("Net Stats", "netstat -s"),
        ]

        # Function to create buttons within a frame from a list of option tuples
        def create_option_buttons(frame, options_list):
            for i, option in enumerate(options_list):
                btn = ttk.Button(frame, text=option[0], command=lambda cmd=option[1]: execute_command(cmd))
                btn.grid(row=i // 6, column=i % 6, padx=5, pady=5, sticky="we")

        # Create buttons in their distinct categories
        create_option_buttons(advanced_windows_settings_frame, windows_management_options)
        create_option_buttons(system_tools_frame, security_and_networking_options)
        create_option_buttons(utilities_frame, system_tools_options)
        create_option_buttons(tools_frame, remote_and_virtualization_options)
        create_option_buttons(trouble_frame, troubleshooting_and_optimization_options)
        create_option_buttons(netsh_frame, netsh_commands)

        version_label = tk.Label(self, text=VERSION, anchor="se", cursor="hand2", fg="#7a7a7a")
        version_label.pack(side="bottom", anchor="se", padx=5, pady=2)

        # Callback function for clicking the version label
        def open_link(event):
            webbrowser.open(LINK)

        # Bind the callback function to the version label
        version_label.bind("<Button-1>", open_link)

        # Script tab Buttons and Positions
        my_ip_btn = ttk.Button(self.functions_frame, text="My IP", command=self.show_ip_address)
        my_ip_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        self.ip_text = tk.Entry(self.functions_frame)
        self.ip_text.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        internet_btn = ttk.Button(self.functions_frame, text="Are we online?", command=self.check_internet)
        internet_btn.grid(row=0, column=2, padx=10, pady=5, sticky="we")

        cmd_btn = ttk.Button(self.functions_frame, text="admin cmd", command=self.open_cmd_as_admin)
        cmd_btn.grid(row=0, column=3, padx=10, pady=5, sticky="we")

        ps_btn = ttk.Button(self.functions_frame, text="admin PowerShell", command=self.open_ps_as_admin)
        ps_btn.grid(row=0, column=4, padx=10, pady=5, sticky="we")

        wifi_btn = ttk.Button(self.functions_frame, text="Wifi Password", command=self.show_wifi_networks)
        wifi_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        winsat_disk_btn = ttk.Button(self.functions_frame, text="Disk Speedtest", command=self.run_winsat_disk)
        winsat_disk_btn.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        kill_bloatware_btn = ttk.Button(self.functions_frame, text="Kill Bloatware", command=self.enhanced_bloatware_killer)
        kill_bloatware_btn.grid(row=1, column=2, padx=10, pady=5, sticky="we")

        renew_ip_config_btn = ttk.Button(self.functions_frame, text="Flush DNS", command=self.renew_ip_config)
        renew_ip_config_btn.grid(row=1, column=3, padx=10, pady=5, sticky="we")

        # Dropdown menu for similar functions - System Info Compare
        self.selected_function1 = tk.StringVar()
        self.function_dropdown1 = ttk.Combobox(
            self.functions_frame,
            textvariable=self.selected_function1,
            values=["Extract Sys Info", "Compare Sys Info", "Show single Sys"],
            state="readonly"
        )
        self.function_dropdown1.grid(row=1, column=4, padx=10, pady=5, sticky="we")
        self.function_dropdown1.set("System Info")  # Set default text
        self.function_dropdown1.bind("<<ComboboxSelected>>", self.on_function_select1)

        self.selected_function2 = tk.StringVar()
        self.function_dropdown2 = ttk.Combobox(
            self.functions_frame,
            textvariable=self.selected_function2,
            values=["Active Connections", "Threat Search"],
            state="readonly"
        )
        self.function_dropdown2.grid(row=2, column=4, padx=10, pady=5, sticky="we")
        self.function_dropdown2.set("App Connections")  # Set default text
        self.function_dropdown2.bind("<<ComboboxSelected>>", self.on_function_select2)

        activate_wui_btn = ttk.Button(self.functions_frame, text="CTT Winutil", command=self.activate_wui)
        activate_wui_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        activate_win_btn = ttk.Button(self.functions_frame, text="Activate Win/Office", command=self.activate_win)
        activate_win_btn.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        agh_curl_btn = ttk.Button(self.functions_frame, text="AdGuard curl-copy", command=self.agh_curl)
        agh_curl_btn.grid(row=2, column=2, padx=10, pady=5, sticky="we")

        arp_btn = ttk.Button(self.functions_frame, text="ARP scan", command=self.arp)
        arp_btn.grid(row=2, column=3, padx=10, pady=5, sticky="we")

        open_links_btn = ttk.Button(self.functions_frame, text="Link Opener", command=self.open_links_window)
        open_links_btn.grid(row=3, column=0, padx=10, pady=5, sticky="we")

        autostart_btn = ttk.Button(self.functions_frame, text="Autostart locations", command=self.open_autostart_locations)
        autostart_btn.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        shutdown_i_btn = ttk.Button(self.functions_frame, text="shutdown -i", command=self.shutdown_i)
        shutdown_i_btn.grid(row=3, column=2, padx=10, pady=5, sticky="we")

        godmode_btn = ttk.Button(self.functions_frame, text="Godmode", command=self.open_godmode)
        godmode_btn.grid(row=4, column=0, padx=10, pady=5, sticky="we")

        checksum_btn = ttk.Button(self.functions_frame, text="Verify file checksum", command=self.get_file_checksum)
        checksum_btn.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        clone_btn = ttk.Button(self.functions_frame, text="Get from GitHub", command=self.clone_repo_with_prompt)
        clone_btn.grid(row=4, column=2, padx=10, pady=5, sticky="we")

        # Fun tab Buttons and Positions
        chat_btn = ttk.Button(self.fun_frame, text="JChat", command=self.open_chat)
        chat_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        pw_btn = ttk.Button(self.fun_frame, text="Password Generator", command=self.open_pw_gen)
        pw_btn.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        hash_btn = ttk.Button(self.fun_frame, text="Hash Generator", command=self.open_hash_stuff)
        hash_btn.grid(row=0, column=2, padx=10, pady=5, sticky="we")

        # Frame for bottom buttons
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)

        # Left-aligned buttons
        shutdown_btn = ttk.Button(self.bottom_frame, text="Shutdown", command=self.confirm_shutdown)
        shutdown_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        reboot_btn = ttk.Button(self.bottom_frame, text="Reboot", command=self.confirm_reboot)
        reboot_btn.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        uefi_btn = ttk.Button(self.bottom_frame, text="UEFI Boot", command=self.confirm_uefi)
        uefi_btn.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        sleep_btn = ttk.Button(self.bottom_frame, text="Hibernate", command=self.confirm_sleep)
        sleep_btn.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        # Spacer label to fill the space between left and right groups
        spacer = ttk.Label(self.bottom_frame)
        spacer.grid(row=0, column=2, rowspan=2, sticky="we")
        self.bottom_frame.columnconfigure(2, weight=1)

        # Right-aligned buttons
        reset_ui_btn = ttk.Button(self.bottom_frame, text="Reset UI", command=self.reset_ui)
        reset_ui_btn.grid(row=0, column=5, padx=5, pady=5, sticky="we")

        root_btn = ttk.Button(self.bottom_frame, text="Root Folder", command=self.open_app_root_folder)
        root_btn.grid(row=0, column=4, padx=5, pady=5, sticky="we")

        exit_btn = ttk.Button(self.bottom_frame, text="Exit", command=self.quit)
        exit_btn.grid(row=1, column=5, padx=5, pady=5, sticky="we")

        update_btn = ttk.Button(self.bottom_frame, text="Update", command=self.git_pull)
        update_btn.grid(row=1, column=4, padx=5, pady=5, sticky="we")


app = Application()
app.mainloop()
