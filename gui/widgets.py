"""Reusable widget factories and layout helpers."""
import tkinter as tk
from tkinter import ttk


class WidgetFactory:
    """Creates consistently styled widgets."""

    @staticmethod
    def button(parent, text: str, command, **grid_kwargs) -> ttk.Button:
        btn = ttk.Button(parent, text=text, command=command)
        if grid_kwargs:
            btn.grid(**grid_kwargs)
        return btn

    @staticmethod
    def accent_button(parent, text: str, command, **grid_kwargs) -> ttk.Button:
        """Primary action button using accent style."""
        btn = ttk.Button(parent, text=text, command=command, style="Accent.TButton")
        if grid_kwargs:
            btn.grid(**grid_kwargs)
        return btn

    @staticmethod
    def dropdown(parent, values: list[str], default: str, on_select, **grid_kwargs) -> ttk.Combobox:
        var = tk.StringVar(value=default)
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        if grid_kwargs:
            combo.grid(**grid_kwargs)

        def _handler(event):
            val = var.get()
            if val != default:
                on_select(val)
                var.set(default)

        combo.bind("<<ComboboxSelected>>", _handler)
        return combo

    @staticmethod
    def labeled_entry(parent, label: str, default: str, theme, row: int, col: int = 0) -> tk.Entry:
        tk.Label(parent, text=label, bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).grid(
            row=row, column=col, padx=5, pady=4, sticky="e"
        )
        entry = tk.Entry(parent, bg=theme.INPUT_BG_COLOR, fg=theme.INPUT_TEXT_COLOR,
                         insertbackground=theme.INPUT_TEXT_COLOR)
        entry.insert(0, default)
        entry.grid(row=row, column=col + 1, padx=5, pady=4, sticky="ew")
        return entry


class GridContainer:
    """Helper to create a uniform grid container."""

    def __init__(self, parent, bg: str, columns: int = 5, padx: int = 15, pady: int = 15):
        self.frame = tk.Frame(parent, bg=bg, padx=padx, pady=pady)
        self.frame.pack(fill="both", expand=True)
        self.columns = columns
        for i in range(columns):
            self.frame.grid_columnconfigure(i, weight=1, uniform="col")

    def add_button(self, text: str, command, index: int):
        row, col = divmod(index, self.columns)
        self.frame.grid_rowconfigure(row, weight=1, uniform="row")
        btn = ttk.Button(self.frame, text=text, command=command)
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        return btn

    def add_dropdown(self, values: list[str], default: str, on_select, index: int):
        row, col = divmod(index, self.columns)
        self.frame.grid_rowconfigure(row, weight=1, uniform="row")
        return WidgetFactory.dropdown(
            self.frame, values, default, on_select,
            row=row, column=col, padx=4, pady=4, sticky="nsew"
        )