"""Dialog windows for various tools."""
import os
import re
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
from pathlib import Path

from gui.styles import Theme
from core.network import (
    check_internet, get_local_ip_info, get_public_ip_info,
    get_wifi_profiles, get_wifi_password, get_netstat_connections,
)
from core.disk import get_disk_info, get_available_drives, run_winsat_disk
from config import batch_script, chkdsk_help_content, ping_help_content, links


def _center(win):
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"+{x}+{y}")


def _make_window(parent, title: str, theme: Theme, size: str = "450x400") -> tk.Toplevel:
    win = tk.Toplevel(parent)
    win.title(title)
    win.geometry(size)
    win.configure(bg=theme.UI_COLOR)
    win.after(50, lambda: _center(win))
    return win


def show_ip_info_dialog(parent, theme: Theme):
    win = _make_window(parent, "IP Information", theme, "430x500")
    text = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg=theme.UI_COLOR,
                                     fg=theme.BUTTON_TEXT_COLOR, font=("Consolas", 10))
    text.pack(fill="both", expand=True, padx=10, pady=10)

    def fetch():
        info = get_local_ip_info() + "\n\n"
        pub = get_public_ip_info()
        if "error" in pub:
            info += pub["error"]
        else:
            info += "═══ Public IP ═══\n"
            for k, v in pub.items():
                info += f"  {k:<10}: {v}\n"
        win.after(0, lambda: (text.insert("end", info), text.config(state="disabled")))

    threading.Thread(target=fetch, daemon=True).start()


def show_disk_info_dialog(parent, theme: Theme):
    """Disk info window with chkdsk, SFC, and refresh."""
    win = _make_window(parent, "Disk Information", theme, "620x650")

    # Text area for disk info
    text = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg=theme.UI_COLOR,
                                     fg=theme.BUTTON_TEXT_COLOR, font=("Consolas", 10))
    text.pack(fill="both", expand=True, padx=10, pady=10)

    def fetch():
        info = get_disk_info()
        win.after(0, lambda: (
            text.config(state="normal"),
            text.delete("1.0", "end"),
            text.insert("end", info),
            text.config(state="disabled")
        ))

    # Button frame
    btn_frame = tk.Frame(win, bg=theme.UI_COLOR)
    btn_frame.pack(fill="x", padx=10, pady=5)

    # Row 0: SFC + chkdsk button + drive label + drive entry
    tk.Button(btn_frame, text="System File Checker", width=20,
              command=lambda: _run_sfc(), bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR
              ).grid(row=0, column=0, padx=(5, 40), pady=5)

    tk.Button(btn_frame, text="Execute CheckDisk", width=20,
              command=lambda: _run_chkdsk(), bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR
              ).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(btn_frame, text="Drive Letter:", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR
             ).grid(row=0, column=2, padx=5, pady=5)

    drive_entry = tk.Entry(btn_frame, width=8, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                           insertbackground=theme.BUTTON_TEXT_COLOR)
    drive_entry.insert(0, "C:")
    drive_entry.grid(row=0, column=3, padx=5, pady=5)

    # Row 1: Refresh + Argument Helper + args label + args entry
    tk.Button(btn_frame, text="Refresh all Disks", width=20,
              command=lambda: threading.Thread(target=fetch, daemon=True).start(),
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR
              ).grid(row=1, column=0, padx=(5, 40), pady=5)

    tk.Button(btn_frame, text="Argument Helper", width=20,
              command=lambda: _show_chkdsk_help(), bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR
              ).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(btn_frame, text="Arguments:", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR
             ).grid(row=1, column=2, padx=5, pady=5)

    args_entry = tk.Entry(btn_frame, width=8, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                          insertbackground=theme.BUTTON_TEXT_COLOR)
    args_entry.insert(0, "/f /r /x")
    args_entry.grid(row=1, column=3, padx=5, pady=5)

    def _run_sfc():
        if messagebox.askyesno("Confirm", "Run 'sfc /scannow'?"):
            subprocess.Popen("start cmd /k sfc /scannow", shell=True)

    def _run_chkdsk():
        drive = drive_entry.get().strip()
        options = args_entry.get().strip()
        if messagebox.askyesno("Confirm", f"Run 'chkdsk {drive} {options}'?"):
            subprocess.Popen(f"start cmd /k chkdsk {drive} {options}", shell=True)

    def _show_chkdsk_help():
        help_win = _make_window(win, "CHKDSK Parameters", theme, "925x700")
        help_text = scrolledtext.ScrolledText(help_win, wrap=tk.WORD, bg=theme.UI_COLOR,
                                              fg=theme.BUTTON_TEXT_COLOR, font=("Consolas", 9))
        help_text.pack(fill="both", expand=True, padx=10, pady=10)
        help_text.insert("end", chkdsk_help_content)
        help_text.config(state="disabled")

    # Initial fetch
    threading.Thread(target=fetch, daemon=True).start()


def show_wifi_dialog(parent, theme: Theme):
    """Wi-Fi profile viewer with password extraction."""
    profiles = get_wifi_profiles()
    if isinstance(profiles, str):
        messagebox.showinfo("Wi-Fi", profiles)
        return

    win = _make_window(parent, "Wi-Fi Networks", theme, "420x350")
    tk.Label(win, text="Select a network:", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=5)

    listbox = tk.Listbox(win, bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR)
    listbox.pack(fill="both", expand=True, padx=10, pady=5)
    for p in profiles:
        listbox.insert(tk.END, p)

    def extract_single():
        sel = listbox.curselection()
        if not sel:
            return
        profile = listbox.get(sel[0])
        pw = get_wifi_password(profile)
        if pw:
            parent.clipboard_clear()
            parent.clipboard_append(pw)
            messagebox.showinfo("Password", f"Password for '{profile}' copied to clipboard.")
        else:
            messagebox.showinfo("No Password", f"No password found for '{profile}'.")

    btn_frame = tk.Frame(win, bg=theme.UI_COLOR)
    btn_frame.pack(fill="x", padx=10, pady=10)
    tk.Button(btn_frame, text="Copy Password", command=extract_single,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Close", command=win.destroy,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="right", padx=5)


def show_internet_check_dialog(parent, theme: Theme):
    win = _make_window(parent, "Internet Status", theme, "400x220")
    text = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg=theme.UI_COLOR,
                                     fg=theme.BUTTON_TEXT_COLOR, font=("Consolas", 10))
    text.pack(fill="both", expand=True, padx=10, pady=10)

    def run():
        results = check_internet()
        online = any(r[0] for r in results)
        header = "✓ ONLINE" if online else "✗ OFFLINE"
        lines = [f"══ {header} ══\n"]
        for ok, msg, lat in results:
            status = "✓" if ok else "✗"
            lines.append(f"  {status} {msg} ({lat}ms)")
        win.after(0, lambda: (text.insert("end", "\n".join(lines)), text.config(state="disabled")))

    threading.Thread(target=run, daemon=True).start()


def show_ping_dialog(parent, theme: Theme):
    """Ping dialog with target, args, and argument helper."""
    win = _make_window(parent, "Ping", theme, "420x160")
    frame = tk.Frame(win, bg=theme.UI_COLOR)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame, text="Target:", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    target_entry = tk.Entry(frame, width=25, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                            insertbackground=theme.BUTTON_TEXT_COLOR)
    target_entry.insert(0, "8.8.8.8")
    target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(frame, text="Arguments:", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    args_entry = tk.Entry(frame, width=25, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                          insertbackground=theme.BUTTON_TEXT_COLOR)
    args_entry.insert(0, "-n 4")
    args_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def run_ping():
        target = target_entry.get().strip()
        args = args_entry.get().strip()
        if target:
            subprocess.Popen(f'start cmd /k ping {target} {args}', shell=True)

    def show_help():
        help_win = _make_window(win, "Ping Parameters", theme, "925x700")
        help_text = scrolledtext.ScrolledText(help_win, wrap=tk.WORD, bg=theme.UI_COLOR,
                                              fg=theme.BUTTON_TEXT_COLOR, font=("Consolas", 9))
        help_text.pack(fill="both", expand=True, padx=10, pady=10)
        help_text.insert("end", ping_help_content)
        help_text.config(state="disabled")

    btn_frame = tk.Frame(frame, bg=theme.UI_COLOR)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(btn_frame, text="Ping", width=14, command=run_ping,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Argument Helper", width=14, command=show_help,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=5)


def show_netstat_dialog(parent, theme: Theme):
    win = _make_window(parent, "Active Connections", theme, "900x500")
    tree = ttk.Treeview(win, columns=("Proto", "Local", "Remote", "State", "PID", "App"), show="headings")
    for col in ("Proto", "Local", "Remote", "State", "PID", "App"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def fetch():
        conns = get_netstat_connections()
        for c in conns:
            win.after(0, lambda c=c: tree.insert("", "end", values=c))

    threading.Thread(target=fetch, daemon=True).start()


def show_disk_speedtest_dialog(parent, theme: Theme):
    win = _make_window(parent, "Disk Speedtest", theme, "350x130")
    drives = get_available_drives()
    if not drives:
        messagebox.showinfo("Disk Speedtest", "No drives found.")
        win.destroy()
        return

    var = tk.StringVar(value=drives[0])
    tk.Label(win, text="Select drive:", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=5)
    tk.OptionMenu(win, var, *drives).pack(pady=5)

    def run():
        run_winsat_disk(var.get()[0])
        win.destroy()

    tk.Button(win, text="Run Test", command=run,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=10)


def show_backup_dialog(parent, theme: Theme):
    win = _make_window(parent, "Backup Options", theme, "380x100")
    tk.Button(win, text="Restore Point",
              command=lambda: os.startfile(os.path.join(os.environ["WINDIR"], "system32", "SystemPropertiesProtection.exe")),
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=20, pady=20)
    tk.Button(win, text="System Image",
              command=lambda: subprocess.run(["control.exe", "/name", "Microsoft.BackupAndRestore"]),
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="right", padx=20, pady=20)


def show_checksum_dialog(parent, theme: Theme):
    path = filedialog.askopenfilename()
    if not path:
        return
    win = _make_window(parent, "File Checksum", theme, "450x180")
    algo_var = tk.StringVar(value="SHA256")
    tk.OptionMenu(win, algo_var, "MD5", "SHA1", "SHA256", "SHA384", "SHA512").pack(pady=5)

    result_text = tk.Text(win, height=3, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR, wrap=tk.WORD)
    result_text.pack(fill="x", padx=10, pady=5)

    def compute():
        try:
            out = subprocess.check_output(f'certutil -hashfile "{path}" {algo_var.get()}', shell=True, text=True)
            checksum = out.splitlines()[1].strip()
            win.after(0, lambda: (result_text.delete("1.0", "end"), result_text.insert("1.0", checksum)))
        except subprocess.CalledProcessError as e:
            win.after(0, lambda: messagebox.showerror("Error", str(e)))

    tk.Button(win, text="Compute", command=lambda: threading.Thread(target=compute, daemon=True).start(),
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=5)


def show_links_dialog(parent, theme: Theme):
    """Clean link summary dialog with categories and open buttons."""
    import webbrowser

    win = _make_window(parent, "Download Links", theme, "550x500")
    win.minsize(450, 400)

    # Main container
    main = tk.Frame(win, bg=theme.UI_COLOR)
    main.pack(fill="both", expand=True, padx=10, pady=10)
    main.grid_rowconfigure(0, weight=1)
    main.grid_columnconfigure(0, weight=1)

    # Scrollable canvas
    canvas = tk.Canvas(main, bg=theme.UI_COLOR, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=theme.UI_COLOR)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    win.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Make scroll_frame expand to canvas width
    def _on_canvas_resize(event):
        canvas.itemconfig(canvas.find_all()[0], width=event.width)
    canvas.bind("<Configure>", _on_canvas_resize)

    # Build categories
    vars_map = {}
    for category, items in links.items():
        lf = tk.LabelFrame(scroll_frame, text=category, bg=theme.UI_COLOR,
                           fg=theme.BUTTON_TEXT_COLOR, font=("Segoe UI", 9, "bold"),
                           padx=10, pady=6)
        lf.pack(fill="x", padx=5, pady=6)

        for text, url in items.items():
            row_frame = tk.Frame(lf, bg=theme.UI_COLOR)
            row_frame.pack(fill="x", pady=2)

            var = tk.IntVar()
            cb = tk.Checkbutton(row_frame, text=text, variable=var,
                                bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                                selectcolor=theme.BUTTON_BG_COLOR, anchor="w",
                                activebackground=theme.UI_COLOR, activeforeground=theme.BUTTON_TEXT_COLOR)
            cb.pack(side="left", fill="x", expand=True)

            # Direct open button per link
            tk.Button(row_frame, text="↗", width=2, font=("Segoe UI", 8),
                      command=lambda u=url: webbrowser.open_new_tab(u),
                      bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                      relief="flat").pack(side="right", padx=2)

            vars_map[url] = var

    # Bottom button bar (fixed, outside scroll area)
    bar = tk.Frame(win, bg=theme.UI_COLOR)
    bar.pack(fill="x", padx=10, pady=(0, 10))

    def open_selected():
        opened = 0
        for url, var in vars_map.items():
            if var.get():
                webbrowser.open_new_tab(url)
                opened += 1
        if opened:
            win.destroy()

    def select_all():
        for var in vars_map.values():
            var.set(1)

    def deselect_all():
        for var in vars_map.values():
            var.set(0)

    tk.Button(bar, text="Select All", width=12, command=select_all,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=4)
    tk.Button(bar, text="Deselect All", width=12, command=deselect_all,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=4)
    tk.Button(bar, text="Open Selected", width=14, command=open_selected,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="right", padx=4)
    tk.Button(bar, text="Close", width=10, command=win.destroy,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="right", padx=4)


def show_quick_access_dialog(parent, theme: Theme):
    win = _make_window(parent, "Quick Access Manager", theme, "380x120")
    src = Path.home() / "AppData/Roaming/Microsoft/Windows/Recent/AutomaticDestinations/f01b4d95cf55d32a.automaticDestinations-ms"

    def export_qa():
        dest = filedialog.asksaveasfilename(initialfile=src.name, filetypes=[("Auto Dest", "*.automaticDestinations-ms")])
        if dest:
            shutil.copy2(src, dest)
            messagebox.showinfo("Done", f"Exported to:\n{dest}")
            win.destroy()

    def import_qa():
        file = filedialog.askopenfilename(filetypes=[("Auto Dest", "*.automaticDestinations-ms")])
        if file:
            shutil.copy2(file, src)
            subprocess.run("taskkill /f /im explorer.exe", shell=True)
            subprocess.Popen("explorer.exe")
            win.destroy()

    tk.Button(win, text="Export", command=export_qa, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="left", padx=30, pady=30)
    tk.Button(win, text="Import", command=import_qa, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(side="right", padx=30, pady=30)


def show_website_checker_dialog(parent, theme: Theme):
    win = _make_window(parent, "Website Checker", theme, "400x130")
    tk.Label(win, text="URL (e.g. example.com):", bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=5)
    entry = tk.Entry(win, width=40, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                     insertbackground=theme.BUTTON_TEXT_COLOR)
    entry.pack(pady=5)
    entry.focus_set()

    def check():
        url = entry.get().strip()
        if not url:
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        import tempfile
        script = batch_script.replace("{{website_url}}", url)
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".bat", delete=False, encoding="utf-8")
        tmp.write(script)
        tmp.close()
        subprocess.Popen(["cmd", "/c", "start", "cmd", "/c", tmp.name], shell=True)
        win.after(2000, lambda: os.unlink(tmp.name))
        win.destroy()

    tk.Button(win, text="Check", command=check, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=10)


def show_logoff_dialog(parent, theme: Theme):
    """Show dialog to select and logoff users."""
    try:
        result = subprocess.run(["quser"], capture_output=True, text=True, errors="replace")
        lines = result.stdout.strip().splitlines()[1:]
    except (subprocess.SubprocessError, OSError):
        messagebox.showerror("Error", "Failed to query users.")
        return

    users = []
    for line in lines:
        match = re.match(r"[> ]\s*(\S+)\s+.*?(\d+)\s+", line)
        if match:
            users.append((match.group(1), match.group(2)))

    if not users:
        messagebox.showinfo("Info", "No users found.")
        return

    win = _make_window(parent, "Logoff Users", theme, "350x250")
    listbox = tk.Listbox(win, selectmode=tk.MULTIPLE, bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)
    for name, sid in users:
        listbox.insert(tk.END, f"{name} (Session {sid})")

    def logoff():
        for idx in listbox.curselection():
            name, session_id = users[idx]
            subprocess.run(["logoff", session_id], check=False)
            print(f"  Logged off: {name}")
        win.destroy()

    tk.Button(win, text="Logoff Selected", command=logoff,
              bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR).pack(pady=10)
