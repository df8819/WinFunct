"""Main Application window."""
import os
import requests
import subprocess
import threading
import ctypes
import shutil
import webbrowser
from pathlib import Path
from tkinter import messagebox, filedialog, ttk
import tkinter as tk

from config import (
    LOGO, VERSION, VERSION_NUMBER, WINFUNCT_LINK,
    links, system_management_options, network_security_options,
    troubleshooting_options, advanced_tools_options,
)
from gui.styles import Theme, StyleManager, load_saved_theme, save_theme
from gui.dialogs import (
    show_ip_info_dialog, show_disk_info_dialog, show_wifi_dialog,
    show_ping_dialog, show_netstat_dialog, show_internet_check_dialog,
    show_backup_dialog, show_checksum_dialog, show_links_dialog,
    show_quick_access_dialog, show_disk_speedtest_dialog,
    show_website_checker_dialog, show_logoff_dialog,
)
from core.system import (
    get_system_info, save_system_info_html, save_system_info_csv,
    flush_dns, restore_system_health, clear_icon_cache, open_autostart_locations,
)
from core.utils import get_app_root, get_powershell_path


# noinspection PyTypeChecker
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load theme
        self.theme = load_saved_theme()
        self.style_mgr = StyleManager(self.theme)
        self.style_mgr.apply()

        # Window setup
        self.title(f"WinFunct v{VERSION_NUMBER} (ﾉ◕◡◕)ﾉ*:･ﾟ✧")
        self.geometry("800x400")
        # self.minsize(750, 450)
        self.configure(bg=self.theme.UI_COLOR)
        self.resizable(False, False)

        # Main frame - clean, no colored border
        self.main_frame = tk.Frame(self, bg=self.theme.UI_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=6, pady=6)

        self._build_ui()
        self.after(50, self._center_window)

    def _center_window(self):
        self.eval("tk::PlaceWindow . center")

    def _build_ui(self):
        """Build the entire UI."""
        # Version at very bottom of window (outside main_frame = no border)
        self._build_version_label()

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Tab frames
        self.scripts_frame = ttk.Frame(self.notebook)
        self.options_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.scripts_frame, text="Scripts")
        self.notebook.add(self.options_frame, text="Options")

        self._build_scripts_tab()
        self._build_options_tab()
        self._build_bottom_bar()

    def _build_scripts_tab(self):
        """Build the Scripts tab with buttons left, dropdowns right."""
        outer = tk.Frame(self.scripts_frame, bg=self.theme.UI_COLOR)
        outer.pack(fill="both", expand=True, padx=10, pady=10)
        outer.grid_columnconfigure(0, weight=3)
        outer.grid_columnconfigure(1, weight=0)
        outer.grid_columnconfigure(2, weight=1)
        outer.grid_rowconfigure(0, weight=1)

        # --- Left: Buttons ---
        btn_frame = tk.Frame(outer, bg=self.theme.UI_COLOR)
        btn_frame.grid(row=0, column=0, sticky="nsew")

        buttons = [
            ("AdGuard Install Helper", self._agh_curl),
            ("Autostart Locations", lambda: threading.Thread(target=open_autostart_locations, daemon=True).start()),
            ("Backup and Restore", lambda: show_backup_dialog(self, self.theme)),
            ("Clear Icon Cache", lambda: threading.Thread(target=clear_icon_cache, daemon=True).start()),
            ("Flush/Renew DNS", self._flush_dns),
            ("Logoff Local User(s)", self._logoff_users),
            ("Open Link Summary", lambda: show_links_dialog(self, self.theme)),
            ("Quick Access Manager", lambda: show_quick_access_dialog(self, self.theme)),
            ("Restore System Health", self._restore_health),
            ("Set PS to Unrestricted", self._set_ps_unrestricted),
            ("Verify File Checksum", lambda: show_checksum_dialog(self, self.theme)),
            ("Wi-Fi Profile Info", lambda: show_wifi_dialog(self, self.theme)),
        ]

        cols = 3
        for i in range(cols):
            btn_frame.grid_columnconfigure(i, weight=1, uniform="btn")
        for idx, (text, cmd) in enumerate(buttons):
            row, col = divmod(idx, cols)
            btn_frame.grid_rowconfigure(row, weight=1, uniform="brow")
            ttk.Button(btn_frame, text=text, command=cmd).grid(
                row=row, column=col, padx=4, pady=4, sticky="nsew"
            )

        # --- Separator ---
        sep = ttk.Separator(outer, orient="vertical")
        sep.grid(row=0, column=1, sticky="ns", padx=8)

        # --- Right: Dropdowns ---
        dd_frame = tk.LabelFrame(outer, text="Select Command", bg=self.theme.PANEL_COLOR,
                                 fg=self.theme.BUTTON_TEXT_COLOR, padx=8, pady=8)
        dd_frame.grid(row=0, column=2, sticky="nsew")

        dropdowns = [
            ("*Interactive Shells*", ["CTT Winutils", "MTT Winhance", "Activate Win/Office", "Install/Upd. FFMPEG"], self._on_shell_select),
            ("*IP & Online Status*", ["PC online status", "Online Status", "IP info", "App Connections", "Ping command"], self._on_network_select),
            ("*Disk Operations*", ["Disk Speedtest", "Show Disk Info"], self._on_disk_select),
            ("*Admin Shells*", ["cmd as Admin", "PowerShell as Admin"], self._on_admin_shell_select),
            ("*System Info*", ["Extract Sys Info", "Compare Sys Info"], self._on_sysinfo_select),
            ("*God Mode*", ["Windows God mode", "ThioJoe God mode"], self._on_godmode_select),
        ]

        for i, (default, options, callback) in enumerate(dropdowns):
            dd_frame.grid_rowconfigure(i, weight=1)
            dd_frame.grid_columnconfigure(0, weight=1)
            var = tk.StringVar(value=default)
            combo = ttk.Combobox(dd_frame, textvariable=var, values=[default] + options, state="readonly")
            combo.grid(row=i, column=0, padx=4, pady=5, sticky="ew")
            combo.bind("<<ComboboxSelected>>", lambda e, v=var, d=default, cb=callback: self._handle_dropdown(v, d, cb))

    def _handle_dropdown(self, var: tk.StringVar, default: str, callback):
        value = var.get()
        if value != default:
            callback(value)
            var.set(default)

    def _build_options_tab(self):
        """Build the Options tab with sub-notebook."""
        sub_nb = ttk.Notebook(self.options_frame)
        sub_nb.pack(fill="both", expand=True, padx=10, pady=10)

        categories = {
            "System Management": system_management_options,
            "Network & Security": network_security_options,
            "Troubleshooting": troubleshooting_options,
            "Advanced Tools": advanced_tools_options,
        }

        for cat_name, options in categories.items():
            frame = ttk.Frame(sub_nb)
            sub_nb.add(frame, text=cat_name)
            container = tk.Frame(frame, bg=self.theme.UI_COLOR, padx=10, pady=10)
            container.pack(fill="both", expand=True)

            cols = 5
            for i in range(cols):
                container.grid_columnconfigure(i, weight=1, uniform="opt")

            for idx, (text, cmd) in enumerate(options):
                row, col = divmod(idx, cols)
                container.grid_rowconfigure(row, weight=1, uniform="orow")
                btn = ttk.Button(container, text=text, command=lambda c=cmd: self._execute_option(c))
                btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

    def _build_bottom_bar(self):
        """Bottom bar with bordered frame."""
        # Bordered container
        border_frame = tk.Frame(self.main_frame, bg=self.theme.BOTTOM_BORDER_COLOR)
        border_frame.pack(fill="x", side="bottom", padx=6, pady=(6, 2))

        # Inner frame (creates border effect)
        bar = tk.Frame(border_frame, bg=self.theme.UI_COLOR)
        bar.pack(fill="both", expand=True, padx=2, pady=2)

        # Left: power buttons
        left = tk.Frame(bar, bg=self.theme.UI_COLOR)
        left.pack(side="left", padx=8, pady=6)

        power_btns = [
            ("Shutdown", "shutdown /s /f /t 1"),
            ("Reboot", "shutdown /r /f /t 1"),
            ("BIOS/UEFI", "shutdown /r /fw /t 1"),
            ("Hibernate", "shutdown /h"),
        ]
        for i, (text, cmd) in enumerate(power_btns):
            ttk.Button(left, text=text, width=14, command=lambda c=cmd: os.system(c)).grid(
                row=i // 2, column=i % 2, padx=4, pady=4
            )

        # Right: app controls
        right = tk.Frame(bar, bg=self.theme.UI_COLOR)
        right.pack(side="right", padx=8, pady=6)

        ttk.Button(right, text="Theme Selector", width=14, command=self._open_theme_selector).grid(row=0, column=0, padx=4, pady=4)
        ttk.Button(right, text="Root Folder", width=14, command=lambda: os.startfile(str(get_app_root()))).grid(row=0, column=1, padx=4, pady=4)
        ttk.Button(right, text="Exit", width=14, command=self.quit).grid(row=1, column=1, padx=4, pady=4)

    def _build_version_label(self):
        """Version label - sits below main_frame, no border."""
        lbl = tk.Label(self, text=VERSION, anchor="e", cursor="hand2",
                       fg=self.theme.VERSION_LABEL_TEXT, bg=self.theme.UI_COLOR,
                       font=("Segoe UI", 8))
        lbl.pack(side="bottom", fill="x", padx=10, pady=(0, 2))
        lbl.bind("<Button-1>", lambda e: webbrowser.open(WINFUNCT_LINK))
        lbl.bind("<Enter>", lambda e: lbl.config(fg="white"))
        lbl.bind("<Leave>", lambda e: lbl.config(fg=self.theme.VERSION_LABEL_TEXT))

    # --- Command handlers ---

    def _execute_option(self, cmd: str):
        """Execute a system command from the Options tab."""
        print(f"  Executing: {cmd}")
        try:
            needs_output = any(cmd.startswith(prefix) for prefix in (
                "netstat", "netsh", "powershell.exe", "bcdedit", "arp",
            ))

            if needs_output:
                threading.Thread(target=lambda: subprocess.run(cmd, shell=True), daemon=True).start()
            elif cmd.startswith("start "):
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except OSError:
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {cmd}", None, 1)

    def _on_shell_select(self, value: str):
        ps = get_powershell_path()
        cmds = {
            "CTT Winutils": "irm christitus.com/win | iex",
            "MTT Winhance": "irm https://github.com/memstechtips/Winhance/raw/main/Winhance.ps1 | iex",
            "Activate Win/Office": "irm https://get.activated.win | iex",
            "Install/Upd. FFMPEG": "iex (irm ffmpeg.tc.ht)",
        }
        ps_cmd = cmds.get(value)
        if not ps_cmd:
            return
        if not Path(ps).exists() and not shutil.which(ps):
            messagebox.showerror("Shell", f"PowerShell not found: {ps}")
            return

        args = f'-NoExit -NoProfile -ExecutionPolicy Bypass -Command "{ps_cmd}"'
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", ps, args, None, 1)  # SW_SHOWNORMAL
        if ret <= 32:
            messagebox.showerror("Shell", f"Launch failed (ShellExecuteW={ret}).\n"
                                          "Check cmd.exe/powershell.exe ACLs and ASR rules.")

    def _on_network_select(self, value: str):
        actions = {
            "PC online status": lambda: show_internet_check_dialog(self, self.theme),
            "Online Status": lambda: show_website_checker_dialog(self, self.theme),
            "IP info": lambda: show_ip_info_dialog(self, self.theme),
            "App Connections": lambda: show_netstat_dialog(self, self.theme),
            "Ping command": lambda: show_ping_dialog(self, self.theme),
        }
        if action := actions.get(value):
            action()

    def _on_disk_select(self, value: str):
        if value == "Disk Speedtest":
            show_disk_speedtest_dialog(self, self.theme)
        elif value == "Show Disk Info":
            show_disk_info_dialog(self, self.theme)

    def _on_admin_shell_select(self, value: str):
        root = str(get_app_root())
        if value == "cmd as Admin":
            subprocess.Popen(f'start cmd.exe /k cd "{root}"', shell=True)
        elif value == "PowerShell as Admin":
            ps = get_powershell_path()
            subprocess.Popen(
                f'{ps} -Command "Start-Process {ps} -Verb RunAs -ArgumentList \'-NoExit -Command Set-Location \\\"{root}\\\"\'"',
                shell=True
            )

    def _on_sysinfo_select(self, value: str):
        if value == "Extract Sys Info":
            self._gather_sysinfo()
        elif value == "Compare Sys Info":
            self._compare_sysinfo()

    def _on_godmode_select(self, value: str):
        if value == "Windows God mode":
            subprocess.Popen("explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}", shell=True)
        elif value == "ThioJoe God mode":
            self._super_godmode()

    def _flush_dns(self):
        if messagebox.askyesno("Flush DNS", "This will temporarily disconnect the network. Continue?"):
            threading.Thread(target=flush_dns, daemon=True).start()

    def _restore_health(self):
        if messagebox.askyesno("Restore Health", "Run DISM cleanup + restorehealth? This may take a while."):
            threading.Thread(target=restore_system_health, daemon=True).start()

    def _set_ps_unrestricted(self):
        try:
            subprocess.run(
                ["powershell", "-Command", "Set-ExecutionPolicy Unrestricted -Force -Scope CurrentUser"],
                check=True, capture_output=True
            )
            messagebox.showinfo("Success", "Execution Policy set to Unrestricted.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def _agh_curl(self):
        cmd = "curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v"
        if messagebox.askyesno("AdGuard Home", f"Copy install command to clipboard?\n\n{cmd}"):
            self.clipboard_clear()
            self.clipboard_append(cmd)
            print("  AdGuard command copied to clipboard.")

    def _logoff_users(self):
        show_logoff_dialog(self, self.theme)

    def _gather_sysinfo(self):
        print("  Gathering system info...")
        info = get_system_info()
        hostname = os.environ.get("COMPUTERNAME", "system")
        path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML", "*.html"), ("CSV", "*.csv")],
            initialfile=f"{hostname}.html"
        )
        if path:
            p = Path(path)
            if p.suffix == ".csv":
                save_system_info_csv(info, p)
            else:
                save_system_info_html(info, p)
            os.startfile(str(p))

    def _compare_sysinfo(self):
        paths = filedialog.askopenfilenames(filetypes=[("CSV", "*.csv")])
        if len(paths) < 2:
            messagebox.showinfo("Info", "Select at least 2 CSV files to compare.")
            return
        messagebox.showinfo("TODO", "Comparison feature - load CSVs and diff them.")

    def _super_godmode(self):
        repo_path = get_app_root() / "Windows-Super-God-Mode"
        if not repo_path.exists():
            if messagebox.askyesno("Clone?", "Clone ThioJoe's Super God Mode repo?"):
                subprocess.run(["git", "clone", "https://github.com/ThioJoe/Windows-Super-God-Mode", str(repo_path)])
        if repo_path.exists():
            bat = repo_path / "SuperGodMode-EasyLauncher.bat"
            if bat.exists():
                subprocess.Popen(f'cmd /c "{bat}"', shell=True, cwd=str(repo_path))

    def _open_theme_selector(self):
        from gui.styles import THEMES_FILE
        if not THEMES_FILE.exists():
            if messagebox.askyesno("Missing Themes", "Theme presets file not found.\nDownload from GitHub?"):
                threading.Thread(target=self._download_themes_file, daemon=True).start()
                return
        from gui.theme_selector import ThemeSelector
        ThemeSelector(self, self.theme, self._apply_new_theme)

    def _download_themes_file(self):
        import requests
        from gui.styles import THEMES_FILE
        url = "https://raw.githubusercontent.com/df8819/WinFunct/main/UI_themes.json"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            THEMES_FILE.write_text(r.text, encoding="utf-8")
            self.after(0, lambda: (
                self._open_theme_selector()
            ))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Download Failed", f"Could not download themes:\n{e}"))

    def _apply_new_theme(self, new_theme: Theme):
        self.theme = new_theme
        save_theme(new_theme)
        self.style_mgr = StyleManager(new_theme)
        self.style_mgr.apply()
        self.configure(bg=new_theme.UI_COLOR)
        self.main_frame.configure(bg=new_theme.UI_COLOR)
        # Destroy main_frame contents
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Destroy old version label (lives on self, not main_frame)
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        self._build_ui()
