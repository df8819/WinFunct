# Standard Library Imports
import base64
import csv
import ctypes
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
    system_management_options, network_security_options,
    troubleshooting_options, advanced_tools_options
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
def execute_system_command(cmd):
    print(f"Executing: {cmd}")
    subprocess.Popen(cmd, shell=True)

def load_theme_from_file():
    try:
        with open('last_selected_theme.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
# ---------------------------------- START WITH ADMIN RIGHTS / SHOW LOGO / LOAD THEME END ----------------------------------
# ---------------------------------- GUI CLASSES ----------------------------------
class StyleManager:
    def __init__(self):
        self.style = ttk.Style()

    def configure_base_styles(self):
        self.style.theme_use('default')
        self.configure_tab_styles()
        self.configure_frame_styles()
        self.configure_button_styles()
        self.configure_combobox_styles()

    def configure_tab_styles(self):
        self.style.configure('Custom.TNotebook',
                           background=UI_COLOR)
        self.style.configure('Custom.TNotebook.Tab',
                           padding=[10, 7],
                           background=BUTTON_BG_COLOR,
                           foreground=BUTTON_TEXT_COLOR)
        self.style.map('Custom.TNotebook.Tab',
                      background=[('selected', UI_COLOR)],
                      foreground=[('selected', BUTTON_TEXT_COLOR)])

    def configure_frame_styles(self):
        self.style.configure('Custom.TFrame',
                           background=UI_COLOR)

    def configure_button_styles(self):
        self.style.configure('Custom.TButton',
                           padding=(10, 5),
                           background=BUTTON_BG_COLOR,
                           foreground=BUTTON_TEXT_COLOR,
                           borderwidth=BORDER_WIDTH,
                           relief=BUTTON_STYLE)
        self.style.map('Custom.TButton',
                      background=[('active', UI_COLOR)],
                      foreground=[('active', BUTTON_TEXT_COLOR)])

    def configure_combobox_styles(self):
        """Configure the styling for dropdown menus (Combobox)"""
        self.style.configure('Custom.TCombobox',
                             background=BUTTON_BG_COLOR,
                             foreground=BUTTON_TEXT_COLOR,
                             fieldbackground=BUTTON_BG_COLOR,
                             selectbackground=UI_COLOR,
                             selectforeground=BUTTON_TEXT_COLOR,
                             arrowcolor=BUTTON_TEXT_COLOR)

        self.style.map('Custom.TCombobox',
                       fieldbackground=[('readonly', BUTTON_BG_COLOR)],
                       selectbackground=[('readonly', UI_COLOR)],
                       selectforeground=[('readonly', BUTTON_TEXT_COLOR)],
                       background=[('readonly', BUTTON_BG_COLOR)],
                       foreground=[('readonly', BUTTON_TEXT_COLOR)])

# noinspection PyMethodMayBeStatic
class WidgetFactory:
    def create_notebook(self, parent):
        notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        notebook.pack(fill="both", expand=True)
        return notebook

    def create_frame(self, parent):
        frame = ttk.Frame(parent, style='Custom.TFrame')
        return frame

    def create_button(self, parent, text, command, row=None, column=None, **kwargs):
        """
        Create a button with proper frame wrapping and grid/pack layout

        Args:
            parent: Parent widget
            text: Button text
            command: Button command callback
            row: Grid row position (optional)
            column: Grid column position (optional)
            **kwargs: Additional button configuration options
        """
        # Remove sticky from kwargs if present since it's not valid for Button
        if 'sticky' in kwargs:
            del kwargs['sticky']

        btn_frame = ttk.Frame(parent, style='Custom.TFrame')
        if row is not None and column is not None:
            btn_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        # Ensure command is properly wrapped
        if callable(command):
            wrapped_command = command
        else:
            wrapped_command = lambda: None
            print(f"Warning: Invalid command for button '{text}'")

        btn = ttk.Button(btn_frame,
                         text=text,
                         command=wrapped_command,
                         style='Custom.TButton',
                         **kwargs)
        btn.pack(fill="both", expand=True)
        return btn

    def create_fixed_height_frame(self, parent, height):
        frame = ttk.Frame(parent, style='Custom.TFrame', height=height)
        frame.pack(fill="x", padx=3, pady=3)
        frame.pack_propagate(False)
        return frame

# noinspection PyMethodMayBeStatic
class LayoutManager:
    def create_grid_container(self, parent, columns=5):
        container = tk.Frame(parent, bg=UI_COLOR, padx=15, pady=15)
        container.pack(expand=True, fill="both")

        # Configure grid weights
        for i in range(columns):
            container.grid_columnconfigure(i, weight=1, uniform="column")

        return container

    def setup_main_tabs(self, notebook, frames):
        for frame, text in frames.items():
            notebook.add(frames[frame], text=text)

# noinspection PyUnresolvedReferences,PyMethodMayBeStatic,PyUnusedLocal
class GUI:
    def __init__(self):
        self.main_frame = None
        self.style_manager = StyleManager()
        self.widget_factory = WidgetFactory()
        self.layout_manager = LayoutManager()

        # Initialize dropdown widget references
        self.function_dropdown1 = None
        self.function_dropdown2 = None
        self.function_dropdown3 = None
        self.function_dropdown4 = None
        self.function_dropdown5 = None
        self.function_dropdown6 = None
        self.function_dropdown7 = None
        self.function_dropdown8 = None

        # Initialize StringVar references
        self.selected_function1 = None
        self.selected_function2 = None
        self.selected_function3 = None
        self.selected_function4 = None
        self.selected_function5 = None
        self.selected_function6 = None
        self.selected_function7 = None
        self.selected_function8 = None

        # Initialize other UI elements
        self.tabs = None
        self.checkbox_vars = None
        self.fun_frame = None
        self.options_frame = None
        self.create_user = None
        self.ip_text = None
        self.functions_frame = None
        self.bottom_frame = None
        self.frames = {}

    # Create Widgets and Dropdowns
    def create_widgets(self):
        # Initialize styles
        self.style_manager.configure_base_styles()

        # Create main structure
        self.tabs = self.widget_factory.create_notebook(self.main_frame)

        # Create main frames
        self.frames = {
            'functions': self.widget_factory.create_frame(self.tabs),
            'options': self.widget_factory.create_frame(self.tabs),
            'fun': self.widget_factory.create_frame(self.tabs)
        }

        # Add frames to tabs
        self.tabs.add(self.frames['functions'], text="Scripts")
        self.tabs.add(self.frames['options'], text="Options")
        self.tabs.add(self.frames['fun'], text="Misc")

        # Create content for each tab
        self._create_options_tab()
        self._create_functions_tab()
        self._create_fun_tab()
        self._create_bottom_frame()
        self._create_version_label()

    def _create_dropdowns(self, parent, dropdown_configs):
        """
        Create dropdown menus with proper initialization and event binding

        Args:
            parent: Parent widget
            dropdown_configs: List of dropdown configuration dictionaries
        """
        for config in dropdown_configs:
            var_name = config['var_name']
            widget_name = config['widget_name']
            options = config['options']
            callback = config['callback']
            row = config.get('row', 0)
            column = config.get('column', 0)

            # Create frame for dropdown
            dropdown_frame = ttk.Frame(parent, style='Custom.TFrame')
            dropdown_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

            # Initialize StringVar
            string_var = tk.StringVar(value=config['default'])
            setattr(self, var_name, string_var)

            # Create and configure dropdown with custom style
            dropdown = ttk.Combobox(
                dropdown_frame,
                textvariable=string_var,
                values=options,
                state="readonly",
                style='Custom.TCombobox'  # Add this line
            )
            dropdown.pack(fill="both", expand=True)

            # Store dropdown widget reference
            setattr(self, widget_name, dropdown)

            # Bind callback - ensure method exists
            if hasattr(self, callback):
                dropdown.bind('<<ComboboxSelected>>', getattr(self, callback))
            else:
                print(f"Warning: Callback method {callback} not found")

    # Create Tabs and Buttons
    def _create_functions_tab(self):
        # Create main container
        main_container = self.layout_manager.create_grid_container(self.frames['functions'])

        # Button configurations
        main_buttons = [
            ("AdGuard Install Helper", self.agh_curl),
            ("Autostart Locations", self.open_autostart_locations),
            ("Flush/Renew DNS", self.renew_ip_config),
            ("Logoff Local User(s)", self.logoff_users),
            ("Open Link Summary", self.open_links_window),
            ("Verify File Checksum", self.get_file_checksum),
            ("Wi-Fi Profile Info", self.show_wifi_networks),
            ("Clear Icon Cache", self.icon_cache),
            ("Quick Access Manager", self.quick_access_manager),
            ("Create CTT Shortcut", self.create_ctt_shortcut),
            ("Restore System Health", self.restore_health),
            ("Backup and Restore", self.create_backup_window)
        ]

        # Calculate rows needed for buttons (using first 3 columns)
        num_rows = (len(main_buttons) + 2) // 3
        for i in range(num_rows):
            main_container.grid_rowconfigure(i, weight=1, uniform="row")

        # Create buttons
        for i, (text, command) in enumerate(main_buttons):
            self.widget_factory.create_button(
                main_container,
                text=text,
                command=command,
                row=i // 3,
                column=i % 3
            )

        # Dropdown configurations
        dropdown_configs = [
            {
                'row': 0,
                'column': 3,
                'var_name': 'selected_function6',
                'widget_name': 'function_dropdown6',
                'default': '*Interactive Shells*',
                'options': ['*Interactive Shells*', '[1] CTT Winutils', '[2] Activate Win/Office',
                            '[3] Install/Upd. FFMPEG'],
                'callback': 'on_function_select6'
            },
            {
                'row': 1,
                'column': 3,
                'var_name': 'selected_function5',
                'widget_name': 'function_dropdown5',
                'default': '*IP & Online Status*',
                'options': ['*IP & Online Status*', '[1] PC online status', '[2] Website online status',
                            '[3] Current IP info', '[4] Apps with internet connection', '[5] Execute <ping> command'],
                'callback': 'on_function_select5'
            },
            {
                'row': 2,
                'column': 3,
                'var_name': 'selected_function7',
                'widget_name': 'function_dropdown7',
                'default': '*Disk Operations*',
                'options': ['*Disk Operations*', '[1] Disk Speedtest', '[2] Show Disk Info'],
                'callback': 'on_function_select7'
            },
            {
                'row': 0,
                'column': 4,
                'var_name': 'selected_function4',
                'widget_name': 'function_dropdown4',
                'default': '*Admin Shells*',
                'options': ['*Admin Shells*', '[1] cmd', '[2] PowerShell'],
                'callback': 'on_function_select4'
            },
            {
                'row': 1,
                'column': 4,
                'var_name': 'selected_function1',
                'widget_name': 'function_dropdown1',
                'default': '*System Info*',
                'options': ['*System Info*', '[1] Extract Sys Info', '[2] Compare Sys Info'],
                'callback': 'on_function_select1'
            },
            {
                'row': 2,
                'column': 4,
                'var_name': 'selected_function3',
                'widget_name': 'function_dropdown3',
                'default': '*God Mode*',
                'options': ['*God Mode*', '[1] Simple God mode', '[2] Super God mode'],
                'callback': 'on_function_select3'
            }
        ]

        # Create dropdowns
        self._create_dropdowns(main_container, dropdown_configs)

    def _create_options_tab(self):
        options_notebook = self.widget_factory.create_notebook(self.frames['options'])
        options_notebook.pack(fill='both', expand=True, padx=15, pady=15)

        categories = {
            'System Management': self.get_system_management_options(),
            'Network & Security': self.get_network_security_options(),
            'Troubleshooting': self.get_troubleshooting_options(),
            'Advanced Tools': self.get_advanced_tools_options()
        }

        for category, options in categories.items():
            frame = self.widget_factory.create_frame(options_notebook)
            options_notebook.add(frame, text=category)
            self._create_option_buttons(frame, options)

    def _create_option_buttons(self, frame, options_list):
        container = self.layout_manager.create_grid_container(frame)

        num_rows = (len(options_list) + 4) // 5
        for i in range(num_rows):
            container.grid_rowconfigure(i, weight=1, uniform="row")

        for i, option in enumerate(options_list):
            button_text, command = option
            self.widget_factory.create_button(
                container,
                text=button_text,
                command=lambda cmd=command: self.execute_command(cmd),
                row=i // 5,
                column=i % 5
            )

    def _create_fun_tab(self):
        # Create notebook within the fun tab
        fun_notebook = self.widget_factory.create_notebook(self.frames['fun'])
        fun_notebook.pack(fill='both', expand=True, padx=15, pady=15)

        # Create category frames
        fun_frames = {
            'apps': self.widget_factory.create_frame(fun_notebook),
            'fun_stuff': self.widget_factory.create_frame(fun_notebook)
        }

        # Add frames to notebook
        fun_notebook.add(fun_frames['apps'], text='Tools')
        fun_notebook.add(fun_frames['fun_stuff'], text='Fun Stuff')

        # Define buttons for each category
        apps_buttons = [
            ("Password Generator", self.open_pw_gen),
            ("Color Picker", self.open_color_picker),
        ]

        fun_stuff_buttons = [
            ("JChat GUI", self.open_chat),
            ("Hash Generator", self.open_hash_stuff),
            ("Funny ASCII Donut", self.open_donut),
            ("WinFunct Logo", self.show_logo)
        ]

        # Create buttons in their respective categories
        self._create_fun_buttons(fun_frames['apps'], apps_buttons)
        self._create_fun_buttons(fun_frames['fun_stuff'], fun_stuff_buttons)

    def _create_fun_buttons(self, frame, buttons_list):
        """Helper method to create buttons in the fun tab sections"""
        # Create main container with layout manager
        container = self.layout_manager.create_grid_container(frame)

        # Calculate and configure rows
        num_rows = (len(buttons_list) + 4) // 5  # 5 columns
        for i in range(num_rows):
            container.grid_rowconfigure(i, weight=1, uniform="row")

        # Create buttons
        for i, (text, command) in enumerate(buttons_list):
            self.widget_factory.create_button(
                container,
                text=text,
                command=command,
                row=i // 5,
                column=i % 5
            )

    # Create Bottom Frame and Label
    def _create_bottom_frame(self):
        # Create main bottom container with fixed height
        self.bottom_frame = self.widget_factory.create_fixed_height_frame(self.main_frame, height=80)

        # Create a content frame inside bottom_frame that will handle the grid layout
        content_frame = self.widget_factory.create_frame(self.bottom_frame)
        content_frame.pack(fill="both", expand=True)

        # Configure grid weights for the content frame
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)  # Middle spacer
        for i in [0, 2]:  # Left and right containers
            content_frame.grid_columnconfigure(i, weight=0)

        # Create three sections: left, middle (spacer), and right
        left_container = self.widget_factory.create_frame(content_frame)
        left_container.grid(row=0, column=0, sticky="nsew", padx=10)

        middle_container = self.widget_factory.create_frame(content_frame)
        middle_container.grid(row=0, column=1, sticky="nsew")

        right_container = self.widget_factory.create_frame(content_frame)
        right_container.grid(row=0, column=2, sticky="nsew", padx=10)

        # Set minimum widths for left and right containers
        left_container.grid_propagate(False)
        left_container.configure(width=300)  # Adjust this value as needed
        right_container.grid_propagate(False)
        right_container.configure(width=300)  # Adjust this value as needed

        # Configure grid weights for left container
        for i in range(2):  # 2 columns
            left_container.grid_columnconfigure(i, weight=1, uniform="left_col")
        for i in range(2):  # 2 rows
            left_container.grid_rowconfigure(i, weight=1, uniform="left_row")

        # Configure grid weights for right container
        for i in range(2):  # 2 columns
            right_container.grid_columnconfigure(i, weight=1, uniform="right_col")
        for i in range(2):  # 2 rows
            right_container.grid_rowconfigure(i, weight=1, uniform="right_row")

        # Create left-aligned buttons
        left_buttons = [
            ("Instant Shutdown", self.confirm_shutdown, 0, 0),
            ("Forced Reboot", self.confirm_reboot, 1, 0),
            ("Reboot to BIOS/UEFI", self.confirm_uefi, 1, 1),
            ("Enter Hibernation", self.confirm_sleep, 0, 1)
        ]

        for text, command, row, col in left_buttons:
            self.widget_factory.create_button(
                left_container,
                text=text,
                command=command,
                row=row,
                column=col
            )

        # Create right-aligned buttons and dropdown
        right_elements = [
            {
                'type': 'dropdown',
                'row': 0,
                'column': 1,
                'var_name': 'selected_function8',
                'widget_name': 'function_dropdown8',
                'default': '*GUI Options*',
                'options': ['*GUI Options*', '[1] Theme Selector', '[2] Reset UI'],
                'callback': 'on_function_select8'
            },
            {
                'type': 'button',
                'row': 1,
                'column': 0,
                'text': 'Open Root Folder',
                'command': self.open_app_root_folder
            },
            {
                'type': 'button',
                'row': 1,
                'column': 1,
                'text': 'Exit Application',
                'command': self.quit
            }
        ]

        for element in right_elements:
            if element['type'] == 'button':
                self.widget_factory.create_button(
                    right_container,
                    text=element['text'],
                    command=element['command'],
                    row=element['row'],
                    column=element['column'],
                    sticky="nsew"  # Ensure buttons scale properly
                )
            elif element['type'] == 'dropdown':
                self._create_dropdowns(right_container, [element])

    def _create_version_label(self):
        """Creates and configures the version label with clickable link"""
        # Create version label container
        version_container = self.widget_factory.create_frame(self.main_frame)
        version_container.pack(side="bottom", fill="x")

        # Create the version label
        self.version_label = tk.Label(
            version_container,
            text=VERSION,
            anchor="se",
            cursor="hand2",
            fg=VERSION_LABEL_TEXT,
            bg=UI_COLOR,
        )
        self.version_label.pack(side="right")

        # Add interactivity to the version label
        self._configure_version_label_bindings()

    def _configure_version_label_bindings(self):
        """Configures the mouse event bindings for the version label"""

        def open_link(event):
            webbrowser.open(WINFUNCT_LINK)

        def on_enter(event):
            self.version_label.config(fg="white")

        def on_leave(event):
            self.version_label.config(fg=VERSION_LABEL_TEXT)

        # Bind mouse events
        self.version_label.bind("<Button-1>", open_link)
        self.version_label.bind("<Enter>", on_enter)
        self.version_label.bind("<Leave>", on_leave)

    # Getter methods
    def get_system_management_options(self):
        from config import system_management_options
        return system_management_options

    def get_network_security_options(self):
        from config import network_security_options
        return network_security_options

    def get_troubleshooting_options(self):
        from config import troubleshooting_options
        return troubleshooting_options

    def get_advanced_tools_options(self):
        from config import advanced_tools_options
        return advanced_tools_options

    # Command execute method for Option-Buttons
    def execute_command(self, cmd):
        """Execute the command associated with an option button"""
        try:
            if hasattr(self, cmd):
                # If it's a class method, execute it
                method = getattr(self, cmd)
                method()
            else:
                # If it's a system command, run it with elevated privileges if needed
                try:
                    subprocess.Popen(cmd, shell=True)
                except WindowsError as we:
                    # Handle "Access Denied" error
                    if we.winerror == 5:
                        # Try running with elevated privileges
                        ctypes.windll.shell32.ShellExecuteW(
                            None, "runas", cmd, None, None, 1
                        )
                    else:
                        raise
        except Exception as e:
            error_msg = f"Error executing command '{cmd}': {str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
# ---------------------------------- GUI CLASSES END ----------------------------------


# Main App Window
# noinspection PyTypeChecker,RegExpRedundantEscape,PyMethodMayBeStatic,PyUnusedLocal,PyShadowingNames,PyAttributeOutsideInit,SpellCheckingInspection,PyGlobalUndefined,PyUnboundLocalVariable,PyBroadException
class Application(tk.Tk, GUI):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        GUI.__init__(self)

        # Initialize managers
        self.style_manager = StyleManager()
        self.widget_factory = WidgetFactory()
        self.layout_manager = LayoutManager()

        self.load_last_selected_theme()

        # Initial window setup
        self.resolution_main = "900x430"
        self.geometry(self.resolution_main)
        self.title("Windows Functionalities (ﾉ◕◡◕)ﾉ*:･ﾟ✧")
        self.configure(bg=UI_COLOR)
        self.resizable(True, True)

        # Create main container
        self.main_frame = tk.Frame(self, bg=BOTTOM_BORDER_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure main frame grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Initialize GUI components using the GUI class method
        super().create_widgets()

        # Load the last selected theme after the main UI is initialized & Center window
        self.after(100, self.load_last_selected_theme)
        self.after(100, self.center_window)

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
        # First update basic tk widgets
        self.configure(bg=UI_COLOR)
        self.main_frame.configure(bg=BOTTOM_BORDER_COLOR)

        # Reconfigure all ttk styles
        self.style_manager = StyleManager()
        self.style_manager.configure_base_styles()

        # Update traditional tk widgets
        def update_widget_colors(widget):
            if isinstance(widget, tk.Button):
                widget.configure(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                 activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=UI_COLOR, fg=BUTTON_TEXT_COLOR)
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=UI_COLOR)
            elif isinstance(widget, tk.OptionMenu):
                widget.configure(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                                 activebackground=UI_COLOR, activeforeground=BUTTON_TEXT_COLOR)
                widget["menu"].configure(bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR)

            for child in widget.winfo_children():
                update_widget_colors(child)

        update_widget_colors(self)

        # Update version label
        if hasattr(self, 'version_label'):
            self.version_label.configure(fg=VERSION_LABEL_TEXT, bg=UI_COLOR)

        # Force update of all widgets
        self.update_idletasks()

        # Recreate all ttk widgets that need immediate update
        self._recreate_ttk_widgets()

    def _recreate_ttk_widgets(self):
        """Recreate critical ttk widgets that need immediate theme update"""
        # Store current tab selection
        current_tab = self.tabs.select()

        # Store the old bottom frame reference and remove it
        old_bottom_frame = self.bottom_frame
        if old_bottom_frame:
            old_bottom_frame.pack_forget()

        # Recreate notebook and its contents
        old_tabs = self.tabs
        self.tabs = self.widget_factory.create_notebook(self.main_frame)
        self.tabs.pack(fill="both", expand=True)

        # Recreate all frames and their contents
        for frame_name, frame in self.frames.items():
            new_frame = self.widget_factory.create_frame(self.tabs)
            self.frames[frame_name] = new_frame
            self.tabs.add(new_frame, text=old_tabs.tab(frame, "text"))

        # Recreate content for each tab
        self._create_options_tab()
        self._create_functions_tab()
        self._create_fun_tab()

        # Remove old notebook
        old_tabs.destroy()

        # Recreate bottom frame with proper styling
        self._create_bottom_frame()  # This will create a new bottom frame with correct border

        # Try to restore previous tab selection
        try:
            self.tabs.select(current_tab)
        except:
            self.tabs.select(0)

        # Clean up old bottom frame if it exists
        if old_bottom_frame:
            old_bottom_frame.destroy()

        # ----------------------------------THEME SELECTOR FOR MAIN APP END----------------------------------

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
        print("Open Password Generator app.")
        pw_window = tk.Toplevel(self)
        pw_window.title("Password Generator")
        pw_window.attributes('-topmost', True)

        # Pass the style manager and theme colors to SimplePWGen
        SimplePWGen(
            pw_window,
            ui_color=UI_COLOR,
            button_bg_color=BUTTON_BG_COLOR,
            button_text_color=BUTTON_TEXT_COLOR,
            style_manager=self.style_manager  # Pass the style manager if available
        )

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

        # Constants
        TIMEOUT_INTERNET = 5
        TIMEOUT_PWSH_CHECK = 10
        TIMEOUT_INSTALL = 300
        TIMEOUT_PROCESS = 30

        def check_internet_connection():
            try:
                requests.get("https://www.google.com", timeout=TIMEOUT_INTERNET)
                return True
            except (requests.ConnectionError, requests.Timeout, requests.RequestException):
                return False

        def check_pwsh_installed():
            try:
                return subprocess.run(
                    ["where", "pwsh"],
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_PWSH_CHECK
                ).returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                return False

        def install_pwsh():
            if not check_internet_connection():
                messagebox.showerror("Error", "No internet connection. Cannot install PowerShell 7.")
                return False

            try:
                subprocess.run(
                    ["winget", "install", "--id", "Microsoft.Powershell", "--source", "winget"],
                    check=True,
                    timeout=TIMEOUT_INSTALL
                )
                return True
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
                error_messages = {
                    subprocess.TimeoutExpired: "PowerShell 7 installation timed out.",
                    subprocess.CalledProcessError: f"Failed to install PowerShell 7: {e}",
                    FileNotFoundError: "Winget not found. Cannot install PowerShell 7."
                }
                messagebox.showerror("Error", error_messages[type(e)])
                return False

        def get_location_command():
            if getattr(sys, 'frozen', False):
                directory = os.path.dirname(sys.executable)
            else:
                directory = os.path.dirname(os.path.abspath(__file__))
            return f'Set-Location "{directory}"'

        def run_command(use_pwsh):
            try:
                ps_command = get_location_command()
                encoded_command = base64.b64encode(ps_command.encode('utf-16le')).decode('ascii')
                shell_type = "pwsh" if use_pwsh else "powershell"

                command = (
                    f'{shell_type} -Command "Start-Process {shell_type} -Verb RunAs '
                    f'-ArgumentList \'-NoExit -EncodedCommand {encoded_command}\'"'
                )

                subprocess.run(command, shell=True, timeout=TIMEOUT_PROCESS)

            except Exception as e:
                error_message = ("Timeout while opening PowerShell window."
                                 if isinstance(e, subprocess.TimeoutExpired)
                                 else f"Failed to open PowerShell as admin: {e}")
                messagebox.showerror("Error", error_message)

        def threaded_run(use_pwsh):
            threading.Thread(target=run_command, args=(use_pwsh,), daemon=True).start()

        # Main execution flow
        if check_pwsh_installed():
            threaded_run(True)
        else:
            user_choice = messagebox.askyesno(
                "PowerShell 7 Not Found",
                "PowerShell 7 is not installed. Do you want to install it via winget?"
            )

            if user_choice and install_pwsh():
                messagebox.showinfo("Installation Successful",
                                    "PowerShell 7 has been installed successfully.")
                threaded_run(True)
            else:
                message = ("Failed to install PowerShell 7. " if user_choice
                           else "Using PowerShell 5.1 instead.")
                messagebox.showinfo("Using PowerShell 5.1", message)
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

    # ----------------------------------CHECK IP----------------------------------

    def format_ip_info(ip_info):
        """Format the IP information for better alignment and readability."""
        formatted_info = ""

        # Section headers
        sections = ip_info.split("\n\n")
        for section in sections:
            lines = section.split("\n")
            if lines:
                # Add section header
                formatted_info += f"{lines[0]}\n"
                # Format key-value pairs with consistent alignment
                for line in lines[1:]:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        formatted_info += f"{key.strip():<15}: {value.strip()}\n"
                    else:
                        formatted_info += f"{line}\n"
                formatted_info += "\n"

        return formatted_info.strip()

    def show_ip_info(self):
        print("Showing IP Information")

        def format_ip_info(ip_info):
            """Format the IP information for better alignment and readability."""
            formatted_info = ""

            # Section headers
            sections = ip_info.split("\n\n")
            for section in sections:
                lines = section.split("\n")
                if lines:
                    # Add section header
                    formatted_info += f"{lines[0]}\n"
                    # Format key-value pairs with consistent alignment
                    for line in lines[1:]:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            formatted_info += f"{key.strip():<15}: {value.strip()}\n"
                        else:
                            formatted_info += f"{line}\n"
                    formatted_info += "\n"

            return formatted_info.strip()

        def create_ip_window():
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

            return ip_window

        def create_text_widget(window):
            # Create a text widget with improved styling
            text_widget = scrolledtext.ScrolledText(
                window,
                wrap=tk.WORD,
                width=40,
                height=10,
                bg=UI_COLOR,
                fg=BUTTON_TEXT_COLOR,
                insertbackground=BUTTON_TEXT_COLOR,
                font=('Courier', 10)  # Use a monospaced font for better alignment
            )
            text_widget.pack(expand=True, fill='both', padx=10, pady=10)
            return text_widget

        def get_local_ip_info():
            """Fetch local IP information with error handling"""
            info = "============= Local ============\n"
            try:
                adapters = psutil.net_if_addrs()
                if not adapters:
                    return info + "No network adapters found.\n\n"

                for adapter, addresses in adapters.items():
                    ipv4_addresses = [addr for addr in addresses if addr.family == 2]  # IPv4
                    if ipv4_addresses:
                        info += f"{adapter}:\n"
                        for addr in ipv4_addresses:
                            info += f"  {addr.address}\n"
                        info += "\n"
                return info
            except Exception as e:
                return info + f"Error fetching local IP information: {str(e)}\n\n"

        def get_public_ip_info(max_retries=3, base_delay=1, timeout=5):
            """Fetch public IP information with improved error handling and multiple API fallbacks"""
            info = "\n============= Internet =============\n"

            # List of IP API services to try
            api_services = [
                {"url": "https://ipapi.co/json/", "handler": handle_ipapi_response},
                {"url": "https://ip-api.com/json/", "handler": handle_ipapi_alternative_response},
                {"url": "https://ipinfo.io/json", "handler": handle_ipinfo_response}
            ]

            for service in api_services:
                for attempt in range(max_retries):
                    try:
                        response = requests.get(
                            service["url"],
                            timeout=timeout,
                            headers={'User-Agent': 'Mozilla/5.0'}
                        )
                        response.raise_for_status()
                        data = response.json()
                        return info + service["handler"](data)
                    except requests.exceptions.Timeout:
                        if attempt == max_retries - 1:
                            continue  # Try next service
                    except requests.exceptions.RequestException as e:
                        if attempt == max_retries - 1:
                            continue  # Try next service
                    time.sleep(base_delay * (attempt + 1))

            return info + "Unable to fetch public IP information from any service.\n"

        def handle_ipapi_response(data):
            """Handle response from ipapi.co"""
            try:
                info = (
                    f"Public IP     : {data['ip']}\n"
                    f"ISP           : {data.get('org', 'N/A')}\n"
                    f"Country       : {data.get('country_name', 'N/A')}\n"
                    f"Region        : {data.get('region', 'N/A')}\n"
                    f"City          : {data.get('city', 'N/A')}\n"
                    f"Postal Code   : {data.get('postal', 'N/A')}\n\n"
                    f"\n============ Topology =============\n"
                    f"Latitude      : {data.get('latitude', 'N/A')}\n"
                    f"Longitude     : {data.get('longitude', 'N/A')}\n"
                    f"Timezone      : {data.get('timezone', 'N/A')}\n\n"
                    f"\n============= Additional Info =============\n"
                    f"Country Code  : {data.get('country', 'N/A')}\n"
                    f"Currency      : {data.get('currency', 'N/A')}\n"
                    f"Languages     : {data.get('languages', 'N/A')}\n"
                )
                return info
            except Exception as e:
                return f"Error parsing ipapi.co response: {str(e)}\n"

        def handle_ipapi_alternative_response(data):
            """Handle response from ip-api.com"""
            try:
                info = (
                    f"Public IP     : {data.get('query', 'N/A')}\n"
                    f"ISP           : {data.get('isp', 'N/A')}\n"
                    f"Country       : {data.get('country', 'N/A')}\n"
                    f"Region        : {data.get('regionName', 'N/A')}\n"
                    f"City          : {data.get('city', 'N/A')}\n"
                    f"Postal Code   : {data.get('zip', 'N/A')}\n\n"
                    f"\n============ Topology =============\n"
                    f"Latitude      : {data.get('lat', 'N/A')}\n"
                    f"Longitude     : {data.get('lon', 'N/A')}\n"
                    f"Timezone      : {data.get('timezone', 'N/A')}\n"
                )
                return info
            except Exception as e:
                return f"Error parsing ip-api.com response: {str(e)}\n"

        def handle_ipinfo_response(data):
            """Handle response from ipinfo.io"""
            try:
                loc = data.get('loc', '').split(',')
                lat, lon = loc if len(loc) == 2 else ('N/A', 'N/A')
                info = (
                    f"Public IP     : {data.get('ip', 'N/A')}\n"
                    f"ISP           : {data.get('org', 'N/A')}\n"
                    f"Country       : {data.get('country', 'N/A')}\n"
                    f"Region        : {data.get('region', 'N/A')}\n"
                    f"City          : {data.get('city', 'N/A')}\n"
                    f"Postal Code   : {data.get('postal', 'N/A')}\n\n"
                    f"\n============ Topology =============\n"
                    f"Latitude      : {lat}\n"
                    f"Longitude     : {lon}\n"
                    f"Timezone      : {data.get('timezone', 'N/A')}\n"
                )
                return info
            except Exception as e:
                return f"Error parsing ipinfo.io response: {str(e)}\n"

        try:
            # Create window and widgets
            ip_window = create_ip_window()
            ip_info_text = create_text_widget(ip_window)

            # Gather IP information
            ip_info = get_local_ip_info()
            ip_info += get_public_ip_info()

            # Format and display IP information
            formatted_ip_info = format_ip_info(ip_info)
            ip_info_text.insert(tk.END, formatted_ip_info)
            ip_info_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    # ----------------------------------CHECK IP END----------------------------------
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
    # ----------------------------------WIFI PASSWORDS-------------------------------------------------

    def decode_output(self, output_bytes):
        """
        Attempt to decode command output using multiple encodings
        """
        encodings = [
            'utf-8', 'cp1252', 'iso-8859-1', 'cp850', 'cp437',
            'ascii', 'latin1'
        ]

        for encoding in encodings:
            try:
                return output_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue

        return output_bytes.decode('utf-8', errors='ignore')

    def get_wifi_profiles(self):
        """
        Retrieve all Wi-Fi profiles from the system
        """
        commands = [
            ["netsh", "wlan", "show", "profiles"],
            ["netsh", "wlan", "show", "profile"]
        ]

        for cmd in commands:
            try:
                output = subprocess.check_output(
                    cmd,
                    stderr=subprocess.STDOUT,
                    timeout=10,
                    shell=True  # Keeping shell=True for compatibility
                )
                output_text = self.decode_output(output)
                if "Profile" in output_text:
                    return output_text
            except:
                continue
        return None

    def show_wifi_networks(self):
        print("Extracting Wifi profiles...")
        try:
            cmd_output = self.get_wifi_profiles()
            if not cmd_output:
                messagebox.showerror("Error", "Could not retrieve WiFi profiles")
                return

            # Enhanced pattern for profile detection
            networks = re.findall(
                r"(?:Profile|Profil|Perfil|プロファイル|配置文件)\s*[:：]\s*([^\r\n]+)",
                cmd_output
            )

        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Command timed out. Network service might be unresponsive.")
            return
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute netsh command: {self.decode_output(e.output)}")
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
            network_listbox = tk.Listbox(
                list_frame,
                yscrollcommand=scrollbar.set,
                exportselection=False,
                bg=UI_COLOR,
                fg=BUTTON_TEXT_COLOR
            )

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
                    password_match = re.search(r"Key Content\s*[:：]\s*([^\r\n]+)", cmd_output)

                    if password_match:
                        password_text = password_match.group(1).strip()
                        self.clipboard_clear()
                        self.clipboard_append(password_text)
                        messagebox.showinfo("Success", f"Password for '{selected_network}' copied to clipboard.")
                    else:
                        messagebox.showinfo("No Password", f"No password found for '{selected_network}'.")

                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Failed to execute command for {selected_network}")

            def cancel_button_click():
                network_window.destroy()

            def extract_all_passwords():
                ssid_passwords = {}
                for network in networks:
                    network_profile = network.strip()
                    try:
                        cmd_output = subprocess.check_output(
                            ["netsh", "wlan", "show", "profile", network_profile, "key=clear"],
                            stderr=subprocess.STDOUT
                        )
                        cmd_output = self.decode_output(cmd_output)
                        password = re.search(r"Key Content\s*[:：]\s*([^\r\n]+)", cmd_output)
                        if password:
                            password_text = password.group(1).strip()
                            ssid_passwords[network_profile] = password_text
                    except:
                        continue

                if ssid_passwords:
                    hostname = socket.gethostname()
                    default_filename = f"pwlist_{hostname}.json"
                    file_path = filedialog.asksaveasfilename(
                        defaultextension='.json',
                        initialfile=default_filename,
                        filetypes=[("JSON Files", '*.json'), ("All Files", '*.*')]
                    )
                    if file_path:
                        with open(file_path, 'w', encoding='utf-8') as json_file:
                            json.dump(ssid_passwords, json_file, indent=4, ensure_ascii=False)
                else:
                    messagebox.showinfo("No Passwords", "No passwords found to extract.")

            def fast_extract_passwords():
                ssid_passwords = {}
                for network in networks:
                    network_profile = network.strip()
                    try:
                        cmd_output = subprocess.check_output(
                            ["netsh", "wlan", "show", "profile", network_profile, "key=clear"],
                            stderr=subprocess.STDOUT
                        )
                        cmd_output = self.decode_output(cmd_output)
                        password = re.search(r"Key Content\s*[:：]\s*([^\r\n]+)", cmd_output)
                        if password:
                            password_text = password.group(1).strip()
                            ssid_passwords[network_profile] = password_text
                    except:
                        continue

                if ssid_passwords:
                    hostname = socket.gethostname()
                    if getattr(sys, 'frozen', False):
                        executable_dir = os.path.dirname(sys.executable)
                    else:
                        executable_dir = os.path.dirname(os.path.abspath(__file__))

                    file_path = os.path.join(executable_dir, f"pwlist_{hostname}.json")
                    with open(file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(ssid_passwords, json_file, indent=4, ensure_ascii=False)
                else:
                    messagebox.showinfo("No Passwords", "No passwords found to extract.")

            # Button layout
            button_frame = tk.Frame(network_window, bg=UI_COLOR)
            button_frame.pack(side="bottom", fill="x", padx=5, pady=10)

            single_button = tk.Button(
                button_frame, text="<Single>", command=extract_single_password,
                width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE
            )
            single_button.pack(side="left", padx=5)

            extract_all_button = tk.Button(
                button_frame, text="<All>", command=extract_all_passwords,
                width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE
            )
            extract_all_button.pack(side="left", padx=5)

            fast_extract_button = tk.Button(
                button_frame, text="<Auto>", command=fast_extract_passwords,
                width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE
            )
            fast_extract_button.pack(side="left", padx=5)

            cancel_button = tk.Button(
                button_frame, text="Cancel", command=cancel_button_click,
                width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR,
                borderwidth=BORDER_WIDTH, relief=BUTTON_STYLE
            )
            cancel_button.pack(side="right", padx=5)

        else:
            messagebox.showinfo("Wi-Fi Networks", "No Wi-Fi networks found.")

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
        height = min(790, window.winfo_screenheight() - 100)
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_ok(self, window):
        for link, var in self.checkbox_vars.items():
            if var.get():
                webbrowser.open_new_tab(link)
        window.destroy()  # Close the window

    # -----------------------------------------------LINK SUMMARY END--------------------------------------------------


app = Application()
app.mainloop()
