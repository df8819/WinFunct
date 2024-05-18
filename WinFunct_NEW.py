# all imports

VERSION = "Use at your own risk and responsibility - v1.342"

LINK = "https://github.com/df8819/WinFunct"

command = 'curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s ' \
          '-- -v'

# apps to uninstall
apps_to_uninstall = [
    "Microsoft.SkypeApp",
]

# PWA links
pwas_to_unregister = [
    "Microsoft.TikTok",
]


def is_admin():
    pass


def run_as_admin():
    pass


def is_running_in_ide():
    pass


if __name__ == "__main__":
    # Bypass admin check if running in an IDE
    pass


# Command functions
def execute_command(cmd):
    pass


# App Window
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("650x520")
        self.center_window()
        self.title("Windows Functionalities --- (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
        self.font_family = "Segoe UI Emoji"

        # background color
        self.main_frame = ttk.Frame(self, style='LightBlue.TFrame')

        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()
        self.resizable(True, True)

    def center_window(self):
        pass

# Many more functions

    def show_ip_address(self):
        pass

    def show_wifi_networks(self):
        pass

            def ok_button_click():
                pass

    def show_wifi_password(self, network):
        pass

            def copy_password():
                pass

            def cancel_button_click():
                pass

    def run_winsat_disk(self):
        pass

# Many more functions

    def notify_user_of_restart(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Update",
                            "Updates.")
        root.destroy()

# Many more functions

    def open_godmode(self):
        pass

    def open_links_window(self):
        # Define your links here
        links = {
            "Dev Tools": {
                "Rufus": "https://rufus.ie/en/",
            },

            "Utilities": {
                "PicPick": "https://picpick.app/en/download/",
            },

            "Tutorials": {
                "NSE Lab": "https://nse.digital",
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
        initial_width = 400
        initial_height = 550  # Adjust the height as needed
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

        # Original tabs
        self.functions_frame = ttk.Frame(self.tabs)  # Renamed from functions_frame for clarity
        self.options_frame = ttk.Frame(self.tabs)
        self.fun_frame = ttk.Frame(self.tabs)

        self.tabs.add(self.functions_frame, text="Scripts")
        self.tabs.add(self.options_frame, text="Options")
        self.tabs.add(self.fun_frame, text="Apps")

        self.tabs.pack(fill="both", expand=True)

        # Options Notebook within the options tab
        options_notebook = ttk.Notebook(self.options_frame)

        # Frames inside the Options tab Example
        advanced_windows_settings_frame = ttk.Frame(options_notebook)

        # options notebook example
        options_notebook.add(advanced_windows_settings_frame, text='Win Manag.')

        # options_frame Example
        options_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Multiple sets for different notebooks/options Example
        windows_management_options = [
            ("RegEdit", "regedit"),
        ]

        security_and_networking_options = [
            ("FW Advanced", "wf.msc"),
        ]

        system_tools_options = [
            ("Ctrl Panel", "control"),
        ]

        remote_and_virtualization_options = [
            ("RDP", "mstsc"),
        ]

        troubleshooting_and_optimization_options = [
            ("RelMon", "perfmon /rel"),
        ]

        netsh_commands = [
            ("IP Config", "netsh interface ip show config"),
        ]

        # Function to create buttons within a frame from a list of option tuples
        def create_option_buttons(frame, options_list):
            # grid for buttons

        # Create buttons in categories Example
        create_option_buttons(advanced_windows_settings_frame, windows_management_options)

        # Functions tab Buttons Example
        wifi_btn = ttk.Button(self.functions_frame, text="Wifi Password", command=self.show_wifi_networks)

        # Functions tab Positions Example
        wifi_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        # Fun tab Buttons Example
        chat_btn = ttk.Button(self.fun_frame, text="JChat", command=self.open_chat)

        # Fun tab Positions Example
        chat_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        # Frame for bottom buttons
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)

        # Left-aligned buttons Example
        shutdown_btn = ttk.Button(self.bottom_frame, text="Shutdown", command=self.confirm_shutdown)
        shutdown_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        # Right-aligned buttons Example
        clone_btn = ttk.Button(self.bottom_frame, text="Clone Repo", command=self.clone_repo_with_prompt)
        clone_btn.grid(row=0, column=4, padx=5, pady=5, sticky="we")


app = Application()
app.mainloop()
