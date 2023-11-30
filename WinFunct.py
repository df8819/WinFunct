import csv
import ctypes
import os
import re
import subprocess
import sys
import tkinter as tk
import webbrowser
import threading
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askstring
import requests
import wmi

# Version of the app
VERSION = "df8819 - v1.1.0.0"

# GitHub repo link
LINK = "https://github.com/df8819/WinFunct"

# The curl-command to copy to the clipboard
command = 'curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s ' \
          '-- -v'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False


def run_as_admin():
    if sys.platform == "win32":
        cmd = [sys.executable] + sys.argv
        cmd_line = ' '.join('"' + item.replace('"', '\\"') + '"' for item in cmd)
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd_line, None, 1)
            sys.exit()  # Exit after trying to elevate privileges
        except Exception as e:
            print(f"Error re-running the script with admin rights: {e}")
    else:
        print("Current platform is not Windows, skipping admin check.")


def is_running_in_ide():
    # This function checks for common IDE-specific variables
    return any(ide_env in os.environ for ide_env in ["PYCHARM_HOSTED", "VSCode"])


if __name__ == "__main__":
    # Bypass admin check if running in an IDE
    if not is_running_in_ide():
        if not is_admin():
            print("Script is not running with admin rights. Trying to obtain them...")
            run_as_admin()
            # The script will exit here if not running as admin

    # Your normal script execution for both admin and non-admin mode continues here
    print("Running with admin rights. Nice (⌐■_■)")


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
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.create_user = None
        self.ip_text = None
        self.functions_frame = None
        self.bottom_frame = None
        self.geometry("650x520")
        self.center_window()
        self.title("Scripts & Options --- (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")

        # Setting the background color of the main frame to light blue
        self.main_frame = ttk.Frame(self, style='LightBlue.TFrame')
        #### Initial code for non-style: self.main_frame = ttk.Frame(self)

        # Creating a style (Delete this to delete style)
        style = ttk.Style()
        style.configure('LightBlue.TFrame', background='dark grey')

        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()
        self.resizable(False, False)

    def center_window(self):
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        position_top = int(self.winfo_screenheight() / 3 - window_height / 2)
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)

        self.geometry(f"+{position_right}+{position_top}")

    def show_ip_address(self):
        response = requests.get("https://ifconfig.me/ip")
        ip_address = response.text
        self.ip_text.delete(0, tk.END)
        self.ip_text.insert(tk.END, ip_address)

    def show_wifi_networks(self):
        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8", "ignore")
        networks = re.findall(r"All User Profile\s+:\s(.+)\r", cmd_output)
        if networks:
            network_window = tk.Toplevel(self)
            network_window.title("Wi-Fi Networks")

            window_width = 300
            window_height = 200
            screen_width = network_window.winfo_screenwidth()
            screen_height = network_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            network_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set window size and position
            network_window.resizable(False, False)  # Lock the window size

            label_text = "Select a Wi-Fi Network in the\ndrop-down menu to copy its password:"  # Text for the label
            label = tk.Label(network_window, text=label_text)
            label.pack(pady=10)

            selected_network = tk.StringVar()  # Variable to store the selected network

            # Create the network dropdown menu
            network_menu = tk.OptionMenu(network_window, selected_network, *networks)
            network_menu.pack(padx=10, pady=10)

            # Function to handle the "Ok" button click
            def ok_button_click():
                if selected_network.get():
                    self.show_wifi_password(selected_network.get())
                network_window.destroy()

            # Create the "Ok" button
            ok_button = tk.Button(network_window, text="Ok", command=ok_button_click, width=10)
            ok_button.pack(side="left", padx=(50, 5))  # Increase the padding on the left side

            # Function to handle the "Cancel" button click
            def cancel_button_click():
                network_window.destroy()

            # Create the "Cancel" button
            cancel_button = tk.Button(network_window, text="Cancel", command=cancel_button_click, width=10)
            cancel_button.pack(side="right", padx=(5, 50))  # Increase the padding on the right side

        else:
            tk.messagebox.showinfo("Wi-Fi Networks", "No Wi-Fi networks found.")

    def show_wifi_password(self, network):
        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network, "key=clear"]).decode("utf-8",
                                                                                                                "ignore")
        password = re.search(r"Key Content\s+:\s(.+)\r", cmd_output)
        if password:
            # Create a new window to display the password
            password_window = tk.Toplevel(self)
            password_window.title(f"Password for {network}")

            window_width = 350
            window_height = 100
            screen_width = password_window.winfo_screenwidth()
            screen_height = password_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set window size and position
            password_window.resizable(False, False)

            password_frame = tk.Frame(password_window)
            password_frame.pack(padx=10, pady=10)

            # Add a label for the password
            password_label = tk.Label(password_frame, text="Password:")
            password_label.grid(row=0, column=0, padx=5, pady=5)

            # Add a text field to display the password
            password_text = tk.Text(password_frame, height=1, width=20)
            password_text.insert(tk.END, password.group(1))
            password_text.grid(row=0, column=1, padx=5, pady=5)
            password_text.config(state="disabled")

            # Add a button to copy the password to the clipboard
            def copy_password():
                self.clipboard_clear()
                self.clipboard_append(password_text.get("1.0", "end-1c"))
                self.update()

            copy_button = tk.Button(password_frame, text="Copy Password", command=copy_password)
            copy_button.grid(row=1, column=0, padx=(5, 5), pady=5, sticky="sw")

            # Add a "Cancel" button to close the window
            def cancel_button_click():
                password_window.destroy()

            cancel_button = tk.Button(password_frame, text="Cancel", command=cancel_button_click)
            cancel_button.grid(row=1, column=1, padx=(5, 50), pady=5, sticky="se")

        else:
            # No password found
            tk.messagebox.showinfo(f"Wi-Fi Password for {network}", "No password found.")

    def run_winsat_disk(self):
        # Ask user to input the drive letter
        drive_letter = askstring("Drive selection", "Enter the drive letter (without colon) to test:")
        if drive_letter is not None:
            powershell_command = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/k winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
            subprocess.Popen(powershell_command, shell=True)

    def activate_win(self):
        user_response = messagebox.askyesno("Activate Microsoft Products",
                                            "This will open a PowerShell instance and guide the user with "
                                            "instructions. Proceed?")
        if user_response:
            command = ['powershell.exe', '-Command', 'irm https://massgrave.dev/get | iex']
            subprocess.run(command, shell=True)
        else:
            print("Command was cancelled.")

    def activate_idm(self):
        user_response = messagebox.askyesno("Activate Internet Download Manager",
                                            "This will open a PowerShell instance and guide the user with "
                                            "instructions. Proceed?")
        if user_response:
            command = ['powershell.exe', '-Command', 'irm https://massgrave.dev/ias | iex']
            subprocess.run(command, shell=True)
        else:
            print("Command was cancelled.")

    def check_user_and_reset_password(self):  # For further customization
        pass
        username = "xxxx"
        password = "xxxx"

        # Check if user exists
        cmd = f"net user {username}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout

        if username in output:
            # Reset password if user exists
            cmd = f"net user {username} {password}"
            subprocess.call(cmd, shell=True)
            messagebox.showinfo("Password Reset", f"Password for user '{username}' reset.")
        else:
            messagebox.showinfo("User Not Found", f"User '{username}' not found.")

    def confirm_shutdown(self):
        # if tk.messagebox.askyesno("Shutdown", "Are you sure you want to shutdown your PC?"):
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

            process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True, shell=True)
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
            stdout, stderr = self.run_powershell_command(f"Get-AppxPackage {app} | Remove-AppxPackage",
                                                         return_output=True)
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
        if not messagebox.askyesno("Bloatware Killer",
                                   "Are you sure you want to uninstall non-essential apps and PWA shortcuts?\n\nWARNING: This will force-delete without any further confirmation!"):
            return

        messagebox.showinfo("Bloatware Killer", "The uninstallation process has started. This may take a while...")
        self.run_script_async(apps_to_uninstall, pwas_to_unregister)

    def renew_ip_config(self):
        if messagebox.askyesno("Renew IP Configuration",
                               "Are you sure you want to release/renew the IP config and flush DNS?"):
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
                    # If the field exists in both systems and they are not equal, record the difference
                    if field in system and field in other_system and system[field] != other_system[field]:
                        if system[field] not in differences[field]:
                            differences[field][system[field]] = []
                        if other_system[field] not in differences[field]:
                            differences[field][other_system[field]] = []

                        differences[field][system[field]].append(file_path)
                        differences[field][other_system[field]].append(other_file_path)

        # Remove fields where no differences were found
        return {field: vals for field, vals in differences.items() if vals}

    import os

    def write_differences_to_file(self, differences, file_path):
        with open(file_path, mode='w', encoding='utf-8') as htmlfile:
            # Write the beginning of the HTML file
            htmlfile.write('<html><head><style>')
            htmlfile.write('table {border-collapse: collapse; width: 100%;}')
            htmlfile.write('th, td {border: 1px solid #ddd; padding: 8px;}')
            htmlfile.write('th {padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #f2f2f2;}')
            htmlfile.write('</style></head><body>')
            htmlfile.write('<table>')
            htmlfile.write('<tr><th>Field</th><th>Value</th><th>Files</th></tr>')

            for field, values in differences.items():
                for value, files in values.items():
                    # Extract just the file names from the paths
                    file_names = set(os.path.basename(file) for file in files)  # Use a set to get unique filenames
                    file_names_with_count = ', '.join(sorted(file_names))  # Sort the filenames
                    htmlfile.write(f'<tr><td>{field}</td><td>{value}</td><td>{file_names_with_count}</td></tr>')

            # End the HTML file
            htmlfile.write('</table></body></html>')

    def check_internet(self):
        # Try to run the 'ping' command to check connectivity.
        try:
            # For Windows, use '-n' for count; for UNIX/Linux, use '-c'.
            # The argument 'stdout=subprocess.PIPE' hides the command output.
            output = subprocess.run(['ping', '-n', '1', '8.8.8.8'], stdout=subprocess.PIPE, text=True)

            # If the ping command succeeds, the return code should be 0.
            if output.returncode == 0:
                messagebox.showinfo("Online?!", "Yes, we're online 👍")
            else:
                messagebox.showinfo("Online?!", "No, we're offline 👎")

        except Exception as e:
            # If an error occurs during the ping process, consider it as offline.
            messagebox.showinfo("Online?!", f"An error occurred: {e}")

    def open_links_window(self):
        # Define your links here
        links = {
            "Python - download": "https://www.python.org/downloads/",
            "Git - download": "https://git-scm.com/downloads",
            "GitHub Desktop - download": "https://desktop.github.com",
            "Visual Studio - download": "https://code.visualstudio.com/download",
            "MS/IDM Script - website": "https://massgrave.dev/index.html",
            "TeamViewer - download": "https://www.teamviewer.com/de/download/windows/",
            "RustDesk - download": "https://github.com/rustdesk/rustdesk/releases/tag/1.2.3",
            "PyCharm - download": "https://www.jetbrains.com/pycharm/download/?section=windows",
            "MS PowerToys - download": "https://github.com/microsoft/PowerToys/releases/tag/v0.75.1",
            "PicPick - download": "https://picpick.app/en/download/",
            "HWInfo64 - download": "https://www.hwinfo.com/download/",
            "MSI Afterburner - download": "https://www.msi.com/Landing/afterburner/graphics-cards",
            "SpaceSniffer - download": "http://www.uderzo.it/main_products/space_sniffer/download.html",
            "Advanced IP Scanner - download": "https://www.advanced-ip-scanner.com/de/",
            "Raspberry Pi Imager - download": "https://www.raspberrypi.com/software/",
            "PuTTY (SSH) - download": "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html",
            "Notepad++ - download": "https://notepad-plus-plus.org/downloads/v8.5.8/",
            "Partition Manager - download": "https://www.paragon-software.com/free/pm-express/#features",
            "Win10 Creation Tool - download": "https://www.microsoft.com/de-de/software-download/windows10",
            "AdGuard Home - YT Tutorial": "https://youtu.be/B2V_8M9cjYw?si=Z_AeA4hCFGiElOHB",

            # Add more items as needed
        }

        # Create a new window
        window = tk.Toplevel(self)
        window_width = 380
        window_height = 520

        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate position x, y
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.resizable(False, False)

        # Create a frame for checkboxes
        checkbox_frame = tk.Frame(window)
        checkbox_frame.pack(padx=10, pady=10, expand=True)

        # Dictionary to hold the IntVar linked to each checkbox
        self.checkbox_vars = {}

        # Create checkboxes
        for text, link in links.items():
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(checkbox_frame, text=text, variable=var)
            checkbox.pack(anchor='w')
            self.checkbox_vars[link] = var

        # Create a frame for buttons
        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)

        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=lambda: self.on_ok(window))
        ok_button.pack(side='right', padx=5)

        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
        cancel_button.pack(side='right')

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

        self.tabs.add(self.functions_frame, text="Scripts")
        self.tabs.add(self.options_frame, text="Options")

        self.tabs.pack(fill="both", expand=True)

        # Options Notebook within the options tab
        options_notebook = ttk.Notebook(self.options_frame)

        # New Category Frames inside the Options tab
        advanced_windows_settings_frame = ttk.Frame(options_notebook)
        system_tools_frame = ttk.Frame(options_notebook)
        utilities_frame = ttk.Frame(options_notebook)
        tools_frame = ttk.Frame(options_notebook)
        trouble_frame = ttk.Frame(options_notebook)

        # Adding new frames to the options notebook
        options_notebook.add(advanced_windows_settings_frame, text='Windows Management')
        options_notebook.add(system_tools_frame, text='Security & Network')
        options_notebook.add(utilities_frame, text='Tools & Options')
        options_notebook.add(tools_frame, text='Remote & Venv')
        options_notebook.add(trouble_frame, text='Trouble & Optimize')

        # Packing the notebook into the options_frame
        options_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Categorized options lists
        # Note: You might need to adjust these lists based on your application's requirements
        # Windows Management and Configuration Tools
        windows_management_options = [
            ("Registry Editor", "regedit"),
            ("Computer Manag.", "compmgmt.msc"),
            ("Event Viewer", "eventvwr.msc"),
            ("Services", "services.msc"),
            ("Group Policy", "gpedit.msc"),
            ("Programs", "appwiz.cpl"),
            ("Windows Ver", "winver"),
            ("Advanced Sys Set.", "SystemPropertiesAdvanced"),
            ("User Acc Control", "useraccountcontrolsettings"),
            ("Windows Update", "start ms-settings:windowsupdate"),
            ("Sys Config", "msconfig"),
            ("Disk Manag.", "diskmgmt.msc"),
        ]

        # Security and Networking Tools
        security_and_networking_options = [
            ("Win Security", "start ms-settings:windowsdefender"),
            ("Security Policy", "secpol.msc"),
            ("Firewall Rules", "wf.msc"),
            ("Network/Sharing", "control /name Microsoft.NetworkAndSharingCenter"),
            ("Internet Options", "inetcpl.cpl"),
            ("Cred. Manager", "control /name Microsoft.CredentialManager"),
            ("Firewall Defender", "firewall.cpl"),
        ]

        # System Tools and Utilities
        system_tools_options = [
            ("hosts file location", "explorer.exe /select,C:\\Windows\\System32\\drivers\\etc\\hosts"),
            ("Admin PS", "powershell.exe -Command Start-Process powershell -Verb RunAs"),
            ("Task Manager", "taskmgr"),
            ("Control Panel", "control"),
            ("Device Manager", "devmgmt.msc"),
            ("Network Conn.", "ncpa.cpl"),
            ("Perform. Monitor", "perfmon"),
            ("Resource Monitor", "resmon"),
            ("Device Install", "hdwwiz"),
            ("Windows Features", "optionalfeatures"),
            ("DirectX Diag.", "dxdiag"),
            ("Environm. Var.", "rundll32.exe sysdm.cpl,EditEnvironmentVariables"),
            ("Sys. Information", "msinfo32"),
        ]

        # Remote Management and Virtualization Tools
        remote_and_virtualization_options = [
            ("Remote Desktop", "mstsc"),
            ("Hyper-V", "virtmgmt.msc"),
            ("Windows Sandbox", "Sandbox"),
        ]

        # Troubleshooting and Optimization Tools
        troubleshooting_and_optimization_options = [
            ("Reliability", "perfmon /rel"),
            ("Disk Cleanup", "cleanmgr"),
            ("Sys Restore", "rstrui"),
            ("Troubleshooting", "msdt"),
            ("Optim. Drives", "dfrgui"),
            ("Memory Diagnostic", "MdSched"),
            ("Security Center", "wscui.cpl"),
            ("Mobility Center", "mblctr"),
        ]

        # Function to create buttons within a frame from a list of option tuples
        def create_option_buttons(frame, options_list):
            for i, option in enumerate(options_list):
                btn = ttk.Button(frame, text=option[0], command=lambda cmd=option[1]: execute_command(cmd))
                btn.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="we")

        # Create buttons in their respective new categories
        create_option_buttons(advanced_windows_settings_frame, windows_management_options)
        create_option_buttons(system_tools_frame, security_and_networking_options)
        create_option_buttons(utilities_frame, system_tools_options)
        create_option_buttons(tools_frame, remote_and_virtualization_options)
        create_option_buttons(trouble_frame, troubleshooting_and_optimization_options)

        version_label = tk.Label(self, text=VERSION, anchor="se", cursor="hand2", fg="blue")
        version_label.pack(side="bottom", anchor="se", padx=5, pady=2)

        # Callback function for clicking the version label
        def open_link(event):
            webbrowser.open(LINK)

        # Bind the callback function to the version label
        version_label.bind("<Button-1>", open_link)

        # Functions tab ("create_user" is excluded due to a bug
        wifi_btn = ttk.Button(self.functions_frame, text="Wifi Password", command=self.show_wifi_networks)
        my_ip_btn = ttk.Button(self.functions_frame, text="My IP", command=self.show_ip_address)
        winsat_disk_btn = ttk.Button(self.functions_frame, text="Disk Speedtest", command=self.run_winsat_disk)
        kill_bloatware_btn = ttk.Button(self.functions_frame, text="Kill Bloatware", command=self.bloatware_killer)
        renew_ip_config_btn = ttk.Button(self.functions_frame, text="Flush DNS", command=self.renew_ip_config)
        activate_idm_btn = ttk.Button(self.functions_frame, text="Activate IDM", command=self.activate_idm)
        activate_win_btn = ttk.Button(self.functions_frame, text="Activate Win/Office", command=self.activate_win)
        agh_curl_btn = ttk.Button(self.functions_frame, text="AdGuard curl-copy", command=self.agh_curl)
        arp_btn = ttk.Button(self.functions_frame, text="ARP scan", command=self.arp)
        open_links_btn = ttk.Button(self.functions_frame, text="Link Opener", command=self.open_links_window)
        save_info_btn = ttk.Button(self.functions_frame, text="Extract Sys Info", command=self.gather_and_save_info)
        compare_systems_btn = ttk.Button(self.functions_frame, text="Compare Sys Info",
                                         command=self.compare_system_info)
        internet_btn = ttk.Button(self.functions_frame, text="Online?", command=self.check_internet)

        my_ip_btn.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.ip_text = tk.Entry(self.functions_frame)
        self.ip_text.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        wifi_btn.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        winsat_disk_btn.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        kill_bloatware_btn.grid(row=1, column=2, padx=10, pady=10, sticky="we")
        renew_ip_config_btn.grid(row=1, column=3, padx=10, pady=10, sticky="we")
        activate_idm_btn.grid(row=2, column=0, padx=10, pady=10, sticky="we")
        activate_win_btn.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        agh_curl_btn.grid(row=2, column=2, padx=10, pady=10, sticky="we")
        arp_btn.grid(row=2, column=3, padx=10, pady=10, sticky="we")
        open_links_btn.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        save_info_btn.grid(row=1, column=4, padx=10, pady=10, sticky="we")
        compare_systems_btn.grid(row=2, column=4, padx=10, pady=10, sticky="we")
        internet_btn.grid(row=0, column=2, padx=10, pady=10, sticky="we")

        # New frame for bottom buttons
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)

        # Adjusting the button parent frame to bottom_frame and using grid
        shutdown_btn = ttk.Button(self.bottom_frame, text="Shutdown", command=self.confirm_shutdown)
        shutdown_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        reboot_btn = ttk.Button(self.bottom_frame, text="Reboot", command=self.confirm_reboot)
        reboot_btn.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        text1_label = ttk.Label(self.bottom_frame, text="⬅ [Foreced command; No confirmation]")
        text1_label.grid(row=0, column=2, padx=5, pady=5, sticky="we")

        uefi_btn = ttk.Button(self.bottom_frame, text="UEFI Boot", command=self.confirm_uefi)
        uefi_btn.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        sleep_btn = ttk.Button(self.bottom_frame, text="Hibernate", command=self.confirm_sleep)
        sleep_btn.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        text2_label = ttk.Label(self.bottom_frame, text="⬅ [Foreced command; No confirmation]")
        text2_label.grid(row=1, column=2, padx=5, pady=5, sticky="we")

        exit_btn = ttk.Button(self.bottom_frame, text="Exit", command=self.quit)
        exit_btn.grid(row=1, column=3, padx=95, pady=5, sticky="we")


# Create and run the app
app = Application()
app.mainloop()
