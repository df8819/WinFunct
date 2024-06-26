# Standard Library Imports
import os
import sys
import re
import csv
import subprocess
import hashlib
import threading
import urllib.request
import ctypes
import webbrowser

# Third-Party Imports
import requests
import wmi

# Tkinter Imports
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

# Local Imports
from JChatInt import JChat
from SimplePWGenInt import SimplePWGen
from HashStuffInt import HashStuff

# Version of the app
VERSION = "Use at your own risk and responsibility - v1.423"

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
    print("\n...Now running with admin rights. Nice (⌐■_■)")


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


# App Window
# noinspection PyMethodMayBeStatic,PyShadowingNames
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resolution_main = "630x520"
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
        # Initial code for non-style: self.main_frame = ttk.Frame(self)

        # Creating a style (Delete this to delete style)
        style = ttk.Style()
        style.configure('LightBlue.TFrame', background='#4791cc')

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
        if tk.messagebox.askyesno("Open JChat", "This will open a chat-app that requires an OpenAI API Key.\n\nSelect 'No' if you don't have your personal Key yet."):
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
        """Open the root folder of the Python app."""
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
        try:
            subprocess.run('powershell Start-Process powershell -Verb runAs', shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PowerShell as admin: {e}")

    def open_cmd_as_admin(self):
        try:
            # Open a new Command Prompt window, navigate to C:\ and set the title
            subprocess.run('start cmd.exe /k cd C:\\ & title Command Prompt as Admin', shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Command Prompt as admin: {e}")

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
            cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network, "key=clear"], stderr=subprocess.STDOUT).decode("utf-8", "ignore")
            password = re.search(r"Key Content\s*:\s*(.+)", cmd_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute netsh command for network '{network}': {e.output.decode('utf-8', 'ignore')}")
            return

        if password:
            password_window = tk.Toplevel(self)
            password_window.title(f"Password for {network}")

            window_width = 350
            window_height = 100
            screen_width = password_window.winfo_screenwidth()
            screen_height = password_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            password_window.resizable(False, False)

            password_frame = tk.Frame(password_window)
            password_frame.pack(padx=10, pady=10)

            password_label = tk.Label(password_frame, text="Password:")
            password_label.grid(row=0, column=0, padx=5, pady=5)

            password_text = tk.Text(password_frame, height=1, width=20)
            password_text.insert(tk.END, password.group(1))
            password_text.grid(row=0, column=1, padx=5, pady=5)
            password_text.config(state="disabled")

            def copy_password():
                self.clipboard_clear()
                self.clipboard_append(password_text.get("1.0", "end-1c"))
                self.update()

            copy_button = ttk.Button(password_frame, text="Copy Password", command=copy_password)
            copy_button.grid(row=1, column=0, padx=(5, 5), pady=5, sticky="sw")

            def cancel_button_click():
                password_window.destroy()

            cancel_button = ttk.Button(password_frame, text="Cancel", command=cancel_button_click)
            cancel_button.grid(row=1, column=1, padx=(5, 50), pady=5, sticky="se")
        else:
            tk.messagebox.showinfo(f"Wi-Fi Password for {network}", "No password found.")

    def run_winsat_disk(self):
        def is_valid_drive_letter(letter):
            return len(letter) == 1 and letter.isalpha()

        # Ask user to input the drive letter
        drive_letter = simpledialog.askstring("Drive selection", "Enter the drive letter (without colon) to test:")

        if drive_letter is None:  # User cancelled the input
            messagebox.showinfo("Operation Cancelled", "Drive selection was cancelled.")
            return

        if is_valid_drive_letter(drive_letter):
            drive_letter = drive_letter.upper()
            powershell_command = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/k winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
            subprocess.Popen(powershell_command, shell=True)
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid drive letter (A-Z).")

    def activate_win(self):
        user_response = messagebox.askyesno("Activate Microsoft Products", "This will open a PowerShell instance and guide the user with instructions. Proceed?")
        if user_response:
            command = ['powershell.exe', '-Command', 'irm https://get.activated.win | iex']
            subprocess.run(command, shell=True)
        else:
            print("Command was cancelled.")

    def activate_wui(self):
        user_response = messagebox.askyesno("Open Windows Utility Improved", "This will open a PowerShell instance and GUI for Windows Utility Improved. Proceed?")
        if user_response:
            command = ['powershell.exe', '-Command', 'irm christitus.com/win | iex']
            subprocess.run(command, shell=True)
        else:
            print("Command was cancelled.")

    def install_rust_transformers(self):
        response = messagebox.askokcancel("Warning", "This script will install Rust, the transformers library, and generate an SSH key. Continue?")
        if response:
            try:
                # Download the Rust installer for Windows
                rust_installer_url = "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
                rust_installer_path = os.path.expanduser("~/rustup-init.exe")
                self.download_file(rust_installer_url, rust_installer_path)

                # Run the Rust installer silently with the '-y' flag (yes to all)
                subprocess.run([rust_installer_path, '-y'], check=True)

                # Install the transformers library via pip
                subprocess.run(['pip', 'install', 'transformers'], check=True)

                # Check if an SSH key already exists, otherwise generate one
                ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')
                if not os.path.exists(ssh_key_path):
                    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', 'user@example.com', '-N', '', '-f', ssh_key_path], check=True)

                messagebox.showinfo("Success", "Installation completed successfully.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"An error occurred during the installation process: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}")

    def download_file(self, url, dest):
        """Download a file from a given URL to the destination path."""
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            messagebox.showerror("Download Error", f"Could not download the file: {e}")
            raise

    def ssh_key(self):
        response = messagebox.askokcancel("SSH-Key", "Generating SSH-Key for this device. Continue?")
        if response:
            # Open a new Command Prompt window and run ssh-keygen
            subprocess.Popen('start cmd.exe /k ssh-keygen', shell=True)

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

    def bloatware_killer(self):
        if not messagebox.askyesno("Bloatware Killer", "Are you sure you want to uninstall non-essential apps and PWA shortcuts?\n\nWARNING: This script will aggressively force-delete without any further confirmation!\n\nINFO: This script creates a .txt log file in the folder it was executed."):
            return

        messagebox.showinfo("Bloatware Killer", "The uninstallation process has started. This may take a while...")
        self.run_script_async(apps_to_uninstall, pwas_to_unregister)

    def renew_ip_config(self):
        if messagebox.askyesno("Renew IP Configuration", "Are you sure you want to release/renew the IP config and flush DNS?"):
            cmd = "cmd.exe /c ipconfig /release && ipconfig /flushdns && ipconfig /renew"
            print(f"Executing command: {cmd}")
            subprocess.run(cmd, shell=True)

    def agh_curl(self):
        # Copy the command to the clipboard using the 'clip' command on Windows
        subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(input=command.encode())
        print('Command copied to clipboard!')

    def arp(self):
        # Command to open a new PowerShell window and run 'arp -a'
        command = 'powershell.exe arp -a'
        subprocess.run(command, shell=True)

    def get_file_checksum(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            # Open cmd with certutil to compute hash for the selected file
            cmd = f'certutil -hashfile "{file_path}" SHA256'
            # Run the command without waiting for it to complete
            subprocess.Popen(cmd, shell=True)
        else:
            print("No file selected.")  # Replace with user notification as needed

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
        installed_software = [software.Caption.strip() for software in c.Win32_Product() if
                              software.Caption and software.Caption != 'HOTKEY']

        system_info['Installed Software'] = installed_software

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

    def check_internet(self):
        # Try to run the 'ping' command to check connectivity.
        try:
            # For Windows, use '-n' for count; for UNIX/Linux, use '-c'.
            # The argument 'stdout=subprocess.PIPE' hides the command output.
            # 'shell=True' is used to execute the command through the shell (use with caution).
            output = subprocess.run(['ping', '-n', '1', '8.8.8.8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)

            # Decode the output using the correct encoding
            # output_decoded = output.stdout.decode('cp437')  # 'cp437' is a common code page for the Windows command prompt

            # If the ping command succeeds, the return code should be 0.
            if output.returncode == 0:
                messagebox.showinfo("Online?!", "Yes, we're online.")
            else:
                messagebox.showinfo("Online?!", "No, we're offline.")

        except Exception as e:
            # If an error occurs during the ping process, consider it as offline.
            messagebox.showinfo("Online?!", f"An error occurred: {e}")

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

            messagebox.showinfo("Success", "'netstat_exe_output.txt' successfully created in the app's root folder.\n\n'netstat_exe_output.txt' lists all apps that have established an internet connection. 'Scan Apps' will lookup each one in a separate Google search tab.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while executing the netstat command: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def search_app_info(self, file_path):
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
            messagebox.showinfo("File Not Found", f"netstat_exe_output.txt not found\n\nPlease click 'App Connections' first and try again.")
            return

        response = messagebox.askyesno("Confirm Search", "Do you want to check scanned App information online?\n\nWARNING: This will open a new google search tab for every entry in netstat_exe_output.txt")
        if response:
            self.search_app_info(file_path)

    def git_pull(self):
        """
        Executes 'git pull' command in the current directory, which is assumed to be a git repository.
        Additionally, checks if requirements.txt has changed and installs new requirements if necessary.
        """
        # Save the current working directory
        repo_path = os.getcwd()
        requirements_path = os.path.join(repo_path, 'requirements.txt')

        # Get the hash of requirements.txt before the pull
        before_pull_hash = self.file_hash(requirements_path) if os.path.exists(requirements_path) else None

        try:
            # Execute 'git pull'
            result = subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)

            # If the result indicates that updates were applied, notify the user
            if "Already up to date." not in result.stdout:
                print("Update detected. Notifying user...")
                self.notify_user_of_restart()

                # Check if requirements.txt has changed by comparing hashes
                after_pull_hash = self.file_hash(requirements_path) if os.path.exists(requirements_path) else None
                if before_pull_hash != after_pull_hash:
                    print("requirements.txt has changed. Installing new requirements...")
                    self.install_requirements(requirements_path)

            return True, result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error during git pull: {e.stderr}")
            return False, e.stderr
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False, str(e)

    def file_hash(self, filepath):
        """
        Calculates the MD5 hash of a file.
        """
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def install_requirements(self, requirements_path):
        """
        Installs the packages from requirements.txt using pip.
        """
        try:
            subprocess.run(["pip", "install", "-r", requirements_path], check=True)
            print("Requirements installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing requirements: {e.stderr}")

    def notify_user_of_restart(self):
        """
        Notifies the user to manually restart the application after an update has been applied.
        """
        # Initialize Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("Update Applied", "Updates have been applied. Please restart the application to use the latest version.")
        root.destroy()

    def check_dependencies(self):
        """Check if Git and Python are installed and show a message box if not."""
        dependencies = {
            "Git": ["git", "--version", "https://git-scm.com/downloads"],
            "Python": [sys.executable, "--version", "https://www.python.org/downloads/"]
        }
        missing_deps = []

        for dep, commands in dependencies.items():
            try:
                result = subprocess.run(commands[:2], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"{dep} version: {result.stdout}")  # Debug print to check successful output
            except subprocess.CalledProcessError as e:
                print(f"Failed to run {commands[0]}: {e.stderr}")  # Debug print to check error output
                missing_deps.append((dep, commands[2]))

        if missing_deps:
            self.notify_missing_dependencies(missing_deps)
        else:
            return True  # Indicate that all dependencies are present

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
        self.check_dependencies()

    def select_clone_directory(self):
        """Prompt user to select directory where the repo should be cloned."""
        root = tk.Tk()
        root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
        directory = filedialog.askdirectory()  # show an "Open" dialog box and return the path to the selected directory
        root.destroy()
        # Check if the user selected a directory or cancelled the dialog
        if directory:  # This will be False if the user clicked "Cancel" or closed the dialog
            return directory
        else:
            return None  # Indicate no selection was made

    def clone_repository(self, repo_url, clone_path):
        """
        Clone the repository directly into a subdirectory within the selected path,
        named after the repository itself.
        """
        # Extract the repo name from the URL (assuming the URL ends with '.git')
        repo_name = repo_url.split('/')[-1][:-4]  # Removes '.git' from the end of the URL to get the repo name
        final_clone_path = os.path.join(clone_path, repo_name)

        try:
            subprocess.run(["git", "clone", repo_url, final_clone_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            messagebox.showinfo("Repository Cloned", f"Repository cloned successfully into {final_clone_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to clone repository: {e.stderr}")

    def clone_repo_with_prompt(self):
        # Check for Git and Python
        if not self.check_dependencies():
            messagebox.showerror("Missing Dependencies", "Git and/or Python are not installed.")
            return

        # Prompt the user to select a directory
        clone_path = self.select_clone_directory()
        if clone_path is None:
            messagebox.showwarning("Clone Cancelled", "Repository clone cancelled. No directory selected.")
            return  # Exit the function as the user cancelled the directory selection

        # Clone the repository directly into the selected path without appending the repo name
        self.clone_repository("https://github.com/df8819/WinFunct.git", clone_path)

    def open_godmode(self):
        try:
            subprocess.run("explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}", shell=True)
        except Exception as e:
            print(f"Error: {e}")

    def open_links_window(self):
        # Define your links here
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
                "Rufus USB Creator": "https://rufus.ie/en/",
                "Etcher USB Creator": "https://etcher.balena.io",
                "SoapUI": "https://www.soapui.org/downloads/soapui/",
                "Win X Server": "https://sourceforge.net/projects/vcxsrv/",
                "HxD": "https://mh-nexus.de/de/downloads.php?product=HxD20",
                "Process Explorer": "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer",
                "TCPView": "https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview",
                "Qt Designer": "https://build-system.fman.io/qt-designer-download",
                "fbs Installer": "https://github.com/mherrmann/fbs-tutorial",
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
                "LinuxLive USB Creator": "https://www.linuxliveusb.com/downloads/?stable",
                "O&O ShutUp10++": "https://www.oo-software.com/de/shutup10",
            },

            "Tutorials": {
                "MAS Script": "https://massgrave.dev/index.html",
                "AdGuard Home": "https://youtu.be/B2V_8M9cjYw?si=Z_AeA4hCFGiElOHB",
                "NSE Lab": "https://nse.digital",
                "Wifi-Hack": "https://hackernoon.com/how-to-hack-wifi-like-a-pro-hacker",
            },
            # Add more categories and items as needed
        }

        # Create a new window
        window = tk.Toplevel(self)
        window.title("Download Links")
        window.resizable(True, True)  # Allow the window to be resizable

        # Create a scrollbar
        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side='right', fill='y')

        # Create a canvas for scrolling
        canvas = tk.Canvas(window, yscrollcommand=scrollbar.set)
        canvas.pack(side='top', fill='both', expand=True)
        scrollbar.config(command=canvas.yview)

        # Create a frame for checkboxes within the canvas
        checkbox_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=checkbox_frame, anchor='nw')

        # Dictionary to hold the IntVar linked to each checkbox
        self.checkbox_vars = {}

        # Create checkboxes within each category
        row = 0
        for category, links_dict in links.items():
            col = 0  # Ensure a category label starts in the first column
            # Create a label for the category
            category_label = tk.Label(checkbox_frame, text=category, font="bold")
            category_label.grid(row=row, column=col, columnspan=2, sticky='w', pady=(10, 5))
            row += 1  # Increment the row for the first item in the category

            # Create checkboxes for each link in the category
            for text, link in links_dict.items():
                var = tk.IntVar()
                checkbox = ttk.Checkbutton(checkbox_frame, text=f"{text}", variable=var)
                checkbox.grid(row=row, column=col, sticky='w', padx=10)

                self.checkbox_vars[link] = var

                # Update row and column positions
                if col == 0:
                    col = 1
                else:
                    col = 0
                    row += 1

            # If the number of items in the category is odd, increment the row to start a new line
            if col != 0:
                row += 1

        # Update the canvas's scrollregion
        checkbox_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create a frame for buttons
        button_frame = tk.Frame(window)
        button_frame.pack(side='bottom', fill='x', pady=10)

        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=lambda: self.on_ok(window))
        ok_button.pack(side='right', padx=5)

        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
        cancel_button.pack(side='right', padx=5)

        # Set the initial geometry of the window
        initial_width = 360
        initial_height = 640  # Adjust the height as needed
        window.geometry(f"{initial_width}x{initial_height}")

        # Center the window on the screen
        window.update_idletasks()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
        options_notebook.add(advanced_windows_settings_frame, text='Win Manag.')
        options_notebook.add(system_tools_frame, text='Sec. & Netw.')
        options_notebook.add(utilities_frame, text='Tools & Options')
        options_notebook.add(tools_frame, text='Remote & Venv')
        options_notebook.add(trouble_frame, text='Trouble & Optim.')
        options_notebook.add(netsh_frame, text='netsh')

        # Packing the notebook into the options_frame
        options_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Categorized options lists
        # Note: You might need to adjust these lists based on your application's requirements
        # Windows Management and Configuration Tools
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

        internet_btn = ttk.Button(self.functions_frame, text="Online?", command=self.check_internet)
        internet_btn.grid(row=0, column=2, padx=10, pady=5, sticky="we")

        cmd_btn = ttk.Button(self.functions_frame, text="cmd", command=self.open_cmd_as_admin)
        cmd_btn.grid(row=0, column=3, padx=10, pady=5, sticky="we")

        ps_btn = ttk.Button(self.functions_frame, text="PowerShell", command=self.open_ps_as_admin)
        ps_btn.grid(row=0, column=4, padx=10, pady=5, sticky="we")

        wifi_btn = ttk.Button(self.functions_frame, text="Wifi Password", command=self.show_wifi_networks)
        wifi_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        winsat_disk_btn = ttk.Button(self.functions_frame, text="Disk Speedtest", command=self.run_winsat_disk)
        winsat_disk_btn.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        kill_bloatware_btn = ttk.Button(self.functions_frame, text="Kill Bloatware", command=self.bloatware_killer)
        kill_bloatware_btn.grid(row=1, column=2, padx=10, pady=5, sticky="we")

        renew_ip_config_btn = ttk.Button(self.functions_frame, text="Flush DNS", command=self.renew_ip_config)
        renew_ip_config_btn.grid(row=1, column=3, padx=10, pady=5, sticky="we")

        save_info_btn = ttk.Button(self.functions_frame, text="Extract Sys Info", command=self.gather_and_save_info)
        save_info_btn.grid(row=1, column=4, padx=10, pady=5, sticky="we")

        activate_wui_btn = ttk.Button(self.functions_frame, text="CTT Winutil", command=self.activate_wui)
        activate_wui_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        activate_win_btn = ttk.Button(self.functions_frame, text="Activate Win/Office", command=self.activate_win)
        activate_win_btn.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        agh_curl_btn = ttk.Button(self.functions_frame, text="AdGuard curl-copy", command=self.agh_curl)
        agh_curl_btn.grid(row=2, column=2, padx=10, pady=5, sticky="we")

        arp_btn = ttk.Button(self.functions_frame, text="ARP scan", command=self.arp)
        arp_btn.grid(row=2, column=3, padx=10, pady=5, sticky="we")

        compare_systems_btn = ttk.Button(self.functions_frame, text="Compare Sys Info", command=self.compare_system_info)
        compare_systems_btn.grid(row=2, column=4, padx=10, pady=5, sticky="we")

        open_links_btn = ttk.Button(self.functions_frame, text="Link Opener", command=self.open_links_window)
        open_links_btn.grid(row=3, column=0, padx=10, pady=5, sticky="we")

        autostart_btn = ttk.Button(self.functions_frame, text="Autostart locations", command=self.open_autostart_locations)
        autostart_btn.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        rust_btn = ttk.Button(self.functions_frame, text="Rust/Transformers", command=self.install_rust_transformers)
        rust_btn.grid(row=3, column=2, padx=10, pady=5, sticky="we")

        ssh_key_btn = ttk.Button(self.functions_frame, text="New SSH Key", command=self.ssh_key)
        ssh_key_btn.grid(row=3, column=3, padx=10, pady=5, sticky="we")

        shutdown_i_btn = ttk.Button(self.functions_frame, text="shutdown -i", command=self.shutdown_i)
        shutdown_i_btn.grid(row=3, column=4, padx=10, pady=5, sticky="we")

        godmode_btn = ttk.Button(self.functions_frame, text="Godmode", command=self.open_godmode)
        godmode_btn.grid(row=4, column=0, padx=10, pady=5, sticky="we")

        checksum_btn = ttk.Button(self.functions_frame, text="SHA256 file checksum", command=self.get_file_checksum)
        checksum_btn.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        netstat_output_btn = ttk.Button(self.functions_frame, text="App Connections", command=self.netstat_output)
        netstat_output_btn.grid(row=4, column=2, padx=10, pady=5, sticky="we")

        search_app_btn = ttk.Button(self.functions_frame, text="Scan Apps", command=self.confirm_and_search)
        search_app_btn.grid(row=4, column=3, padx=10, pady=5, sticky="we")

        clone_btn = ttk.Button(self.functions_frame, text="Clone this Repo", command=self.clone_repo_with_prompt)
        clone_btn.grid(row=4, column=4, padx=10, pady=5, sticky="we")

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
