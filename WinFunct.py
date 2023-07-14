import ctypes
import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import requests
import webbrowser
# import shutil


VERSION = "v1.0.0.1"
LINK = "https://github.com/df8819/WinFunct"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # The script is already running with admin rights.
    # Replace the line below with your actual script
    print("I have admin rights")
else:
    # Re-run the program with admin rights.
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

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

class UserCreationWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("User Creation")
        self.geometry("250x200")  # Set the window size
        self.resizable(False, False)

        # Add the necessary widgets and functionality for user creation
        self.username_label_above = tk.Label(self, text="This will create a new\nWindows user as admin:\n")
        self.username_label_above.pack()


        # Example: Add a label and an entry field for username
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Example: Add a label and an entry field for password
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")  # Mask the password
        self.password_entry.pack()

        # Example: Add a button to create the user
        create_button = tk.Button(self, text="Create User", command=self.create_user)
        create_button.pack()

        # Example: Add a button to cancel user creation
        cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.pack()

    def create_user(self):
        # Retrieve the username and password entered by the user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if both username and password are provided
        if username and password:
            # Check if the username already exists
            cmd_check_user = f"net user {username}"
            result_check_user = subprocess.run(cmd_check_user, shell=True, capture_output=True, text=True)
            if result_check_user.returncode == 0:
                # User already exists, display an error message
                messagebox.showerror("User Creation Error", f"User '{username}' already exists.")
            else:
                # Add the logic to create the user
                cmd_create = f"net user {username} {password} /add"
                cmd_admin = f"net localgroup administrators {username} /add"

                # Create the user
                result_create = subprocess.run(cmd_create, shell=True, capture_output=True, text=True)
                if result_create.returncode == 0:
                    # Set the user as an administrator
                    result_admin = subprocess.run(cmd_admin, shell=True, capture_output=True, text=True)
                    if result_admin.returncode == 0:
                        messagebox.showinfo("User Created",
                                            f"User '{username}' created successfully and set as an administrator.")
                    else:
                        messagebox.showerror("User Creation Error", "Failed to set the user as an administrator.")
                else:
                    messagebox.showerror("User Creation Error", "Failed to create the user.")
        else:
            messagebox.showerror("Missing Information", "Please enter both username and password.")

        # Close the window after user creation attempt
        self.destroy()


# App Window
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("520x500")
        self.center_window()
        self.title("Scripts & Options - (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")

        self.main_frame = ttk.Frame(self)
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
        networks = re.findall("All User Profile\s+:\s(.+)\r", cmd_output)
        if networks:
            network_window = tk.Toplevel(self)
            network_window.title("Wi-Fi Networks")
            network_window.geometry("300x200")  # Customize the window size (width x height)
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
            ok_button = tk.Button(network_window, text="Ok", command=ok_button_click)
            ok_button.pack(pady=5)

            # Function to handle the "Cancel" button click
            def cancel_button_click():
                network_window.destroy()

            # Create the "Cancel" button
            cancel_button = tk.Button(network_window, text="Cancel", command=cancel_button_click)
            cancel_button.pack(pady=5)
        else:
            tk.messagebox.showinfo("Wi-Fi Networks", "No Wi-Fi networks found.")

    def show_wifi_password(self, network):
        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", network, "key=clear"]).decode("utf-8",
                                                                                                                "ignore")
        password = re.search("Key Content\s+:\s(.+)\r", cmd_output)
        if password:
            # Create a new window to display the password
            password_window = tk.Toplevel(self)
            password_window.title(f"Password for {network}")
            password_frame = tk.Frame(password_window)
            password_frame.pack(padx=10, pady=10)

            # Add a label for the password
            password_label = tk.Label(password_frame, text="Password:")
            password_label.grid(row=0, column=0, padx=5, pady=5)

            # Add a text field to display the password
            password_text = tk.Text(password_frame, height=1, width=30)
            password_text.insert(tk.END, password.group(1))
            password_text.grid(row=0, column=1, padx=5, pady=5)
            password_text.config(state="disabled")

            # Add a button to copy the password to the clipboard
            def copy_password():
                self.clipboard_clear()
                self.clipboard_append(password_text.get("1.0", "end-1c"))
                self.update()

            copy_button = tk.Button(password_frame, text="Copy Password", command=copy_password)
            copy_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        else:
            # No password found
            tk.messagebox.showinfo(f"Wi-Fi Password for {network}", "No password found.")

    def run_winsat_disk(self):
        # Ask user to input the drive letter
        drive_letter = askstring("Drive selection", "Enter the drive letter (without colon) to test:")
        if drive_letter is not None:
            powershell_command = f'powershell.exe -Command "Start-Process cmd -ArgumentList \'/k winsat disk -drive {drive_letter} && pause\' -Verb RunAs"'
            subprocess.Popen(powershell_command, shell=True)

    def create_user(self):
        window = UserCreationWindow(self)
        window.grab_set()

    def activate_win(self):
        user_response = messagebox.askyesno("Activate MS Products",
                                            "Are you sure you want to activate Win/Office products?")
        if user_response:
            command = ['powershell.exe', '-Command', 'irm https://massgrave.dev/get | iex']
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
        if tk.messagebox.askyesno("Shutdown", "Are you sure you want to force-shutdown your PC?"):
            os.system("shutdown /s /t 1")

    def confirm_reboot(self):
        if tk.messagebox.askyesno("Reboot", "Are you sure you want to force-reboot your PC?"):
            os.system("shutdown /r /t 1")

    def confirm_sleep(self):
        if tk.messagebox.askyesno("Sleep", "Are you sure you want to force-sleep your PC?"):
            os.system("shutdown /h /t 1")

    def confirm_uefi(self):
        if tk.messagebox.askyesno("UEFI Boot", "Are you sure you want to reboot directly into BIOS/UEFI?"):
            os.system("shutdown /r /fw /t 1")

    def bloatware_killer(self):
        if not tk.messagebox.askyesno("Bloatware Killer",
                                      "Are you sure you want to uninstall non-essential apps and PWA shortcuts?\n\nWARNING: This will force-delete without any further conformation!"):
            return  # User did not confirm, so we exit the function early.

        # Prepare the PowerShell script
        powershell_script = "powershell -Command "

        # Generate the script command for uninstalling apps
        uninstall_commands = [
            f"Get-AppxPackage {app} | Remove-AppxPackage" for app in apps_to_uninstall
        ]
        uninstall_script = "; ".join(uninstall_commands)

        # Generate the script command for unregistering PWA shortcuts
        unregister_commands = [
            f"Get-AppxPackage {pwa} | Remove-AppxPackage; Remove-AppxProvisionedPackage -Online -PackageName {pwa}" for
            pwa in pwas_to_unregister
        ]
        unregister_script = "; ".join(unregister_commands)

        # Combine the uninstall and unregister scripts
        full_script = f"{uninstall_script}; {unregister_script}"

        # Run the combined script in a single PowerShell window
        subprocess.run(["powershell", "-Command", full_script], shell=True)

        messagebox.showinfo("Bloatware Killer", "Non-essential apps and PWA shortcuts have been uninstalled.")

    def renew_ip_config(self):
        if messagebox.askyesno("Renew IP Configuration", "Are you sure you want to release/renew the IP config and flush DNS?"):
            cmd = "cmd.exe /c ipconfig /release && ipconfig /flushdns && ipconfig /renew"
            print(f"Executing command: {cmd}")
            subprocess.run(cmd, shell=True)


    def create_widgets(self):
        self.tabs = ttk.Notebook(self.main_frame)

        self.functions_frame = ttk.Frame(self.tabs)
        self.options_frame = ttk.Frame(self.tabs)

        self.tabs.add(self.functions_frame, text="Scripts")
        self.tabs.add(self.options_frame, text="Options")

        self.tabs.pack(fill="both", expand=True)

        version_label = tk.Label(self, text=VERSION, anchor="se", cursor="hand2", fg="blue")
        version_label.pack(side="bottom", anchor="se", padx=0, pady=0)

        # Callback function for clicking the version label
        def open_link(event):
            webbrowser.open(LINK)

        # Bind the callback function to the version label
        version_label.bind("<Button-1>", open_link)

        # Functions tab
        wifi_btn = ttk.Button(self.functions_frame, text="Wifi Password", command=self.show_wifi_networks)
        my_ip_btn = ttk.Button(self.functions_frame, text="My IP", command=self.show_ip_address)
        winsat_disk_btn = ttk.Button(self.functions_frame, text="Disk Speedtest", command=self.run_winsat_disk)
        kill_bloatware_btn = ttk.Button(self.functions_frame, text="Kill Bloatware", command=self.bloatware_killer)
        renew_ip_config_btn = ttk.Button(self.functions_frame, text="Flush DNS", command=self.renew_ip_config)
        create_user_btn = ttk.Button(self.functions_frame, text="Create Account", command=self.create_user)
        activate_win_btn = ttk.Button(self.functions_frame, text="Activate MS", command=self.activate_win)

        my_ip_btn.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.ip_text = tk.Entry(self.functions_frame)  # Define ip_text as an instance variable using 'self'
        self.ip_text.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        wifi_btn.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        winsat_disk_btn.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        kill_bloatware_btn.grid(row=1, column=2, padx=10, pady=10, sticky="we")
        renew_ip_config_btn.grid(row=1, column=3, padx=10, pady=10, sticky="we")
        create_user_btn.grid(row=2, column=0, padx=10, pady=10, sticky="we")
        activate_win_btn.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        # Options tab
        options = [
            ("GoTo hosts file location", "explorer.exe /select,C:\\Windows\\System32\\drivers\\etc\\hosts"),
            ("Run PowerShell as admin", "powershell.exe -Command Start-Process powershell.exe -Verb RunAs"),
            ("Browser", "start https://www.google.com"),
            ("Windows Defender", "start ms-settings:windowsdefender"),
            ("Registry Editor", "regedit"),
            ("File Explorer", "explorer.exe"),
            ("Control Panel", "control"),
            ("Device Manager", "devmgmt.msc"),
            ("Network Connections", "ncpa.cpl"),
            ("Windows Firewall", "firewall.cpl"),
            ("System Config (msc)", "msconfig"),
            ("Advanced System Settings", "SystemPropertiesAdvanced"),
            ("Task Manager", "taskmgr"),
            ("Disk Management", "diskmgmt.msc"),
            ("Device Installers", "hdwwiz"),
            ("Computer Management", "compmgmt.msc"),
            ("Event Viewer", "eventvwr.msc"),
            ("User Account Control", "useraccountcontrolsettings"),
            ("Windows Update", "start ms-settings:windowsupdate"),
            ("Performance Monitor", "perfmon"),
            ("Services", "services.msc"),
            ("Windows Features", "optionalfeatures"),
            ("Group Policy Editor", "gpedit.msc"),
            ("Power Options", "powercfg.cpl"),
            ("Programs and Features", "appwiz.cpl"),
            ("Windows Version", "winver"),
        ]

        for i, option in enumerate(options):
            btn = ttk.Button(self.options_frame, text=option[0], command=lambda cmd=option[1]: execute_command(cmd))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="we")

        # Bottom buttons
        shutdown_btn = ttk.Button(self.main_frame, text="Shutdown", command=self.confirm_shutdown)
        reboot_btn = ttk.Button(self.main_frame, text="Reboot", command=self.confirm_reboot)
        uefi_btn = ttk.Button(self.main_frame, text="UEFI Boot", command=self.confirm_uefi)
        sleep_btn = ttk.Button(self.main_frame, text="Sleep", command=self.confirm_sleep)
        exit_btn = ttk.Button(self.main_frame, text="Exit", command=self.quit)

        shutdown_btn.pack(side="left", padx=10, pady=10)
        sleep_btn.pack(side="left", padx=10, pady=10)
        reboot_btn.pack(side="left", padx=10, pady=10)
        uefi_btn.pack(side="left", padx=10, pady=10)
        exit_btn.pack(side="right", padx=10, pady=10)


# Create and run the app
app = Application()
app.mainloop()
