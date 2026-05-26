"""Theme selector dialog."""
import tkinter as tk
from tkinter import colorchooser

from gui.styles import Theme, load_theme_presets


class ThemeSelector:
    FIELDS = ["UI_COLOR", "BUTTON_BG_COLOR", "BUTTON_TEXT_COLOR", "BOTTOM_BORDER_COLOR", "VERSION_LABEL_TEXT"]

    def __init__(self, master, current_theme: Theme, on_apply):
        self.on_apply = on_apply
        self.entries = {}

        self.win = tk.Toplevel(master)
        self.win.title("Theme Selector")
        self.win.geometry("380x250")
        self.win.configure(bg=current_theme.UI_COLOR)

        t = current_theme
        for i, field in enumerate(self.FIELDS):
            tk.Label(self.win, text=field, bg=t.UI_COLOR, fg=t.BUTTON_TEXT_COLOR).grid(row=i, column=0, padx=5, pady=4)
            entry = tk.Entry(self.win, bg=t.BUTTON_BG_COLOR, fg=t.BUTTON_TEXT_COLOR, insertbackground=t.BUTTON_TEXT_COLOR)
            entry.insert(0, getattr(t, field))
            entry.grid(row=i, column=1, padx=5, pady=4)
            self.entries[field] = entry
            tk.Button(self.win, text="Pick", width=5, bg=t.BUTTON_BG_COLOR, fg=t.BUTTON_TEXT_COLOR,
                      command=lambda e=entry: self._pick(e)).grid(row=i, column=2, padx=5, pady=4)

        # Preset dropdown
        presets = load_theme_presets()
        preset_names = [p["name"] for p in presets]
        self.presets = {p["name"]: p for p in presets}

        row = len(self.FIELDS)
        self.preset_var = tk.StringVar(value="Select preset...")
        if preset_names:
            menu = tk.OptionMenu(self.win, self.preset_var, *preset_names, command=self._on_preset)
            menu.config(bg=t.BUTTON_BG_COLOR, fg=t.BUTTON_TEXT_COLOR)
            menu.grid(row=row, column=0, columnspan=2, padx=5, pady=8, sticky="ew")

        tk.Button(self.win, text="Apply", bg=t.BUTTON_BG_COLOR, fg=t.BUTTON_TEXT_COLOR,
                  command=self._apply).grid(row=row, column=2, padx=5, pady=8)

    def _pick(self, entry: tk.Entry):
        color = colorchooser.askcolor()[1]
        if color:
            entry.delete(0, tk.END)
            entry.insert(0, color)

    def _on_preset(self, name: str):
        preset = self.presets.get(name, {})
        for field, entry in self.entries.items():
            if field in preset:
                entry.delete(0, tk.END)
                entry.insert(0, preset[field])
        self._apply()

    def _apply(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        self.on_apply(Theme.from_dict(data))
        self.win.destroy()
