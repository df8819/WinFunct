"""Reusable widget factories and layout helpers."""
import tkinter as tk
from tkinter import ttk


class WidgetFactory:
    """Creates consistently styled widgets."""

    @staticmethod
    def button(parent, text: str, command, **grid_kwargs) -> ttk.Button:
        """Create a ttk Button and optionally grid it."""
        btn = ttk.Button(parent, text=text, command=command)
        if grid_kwargs:
            btn.grid(**grid_kwargs)
        return btn

    @staticmethod
    def dropdown(parent, values: list[str], default: str, on_select, **grid_kwargs) -> ttk.Combobox:
        """Create a readonly Combobox with callback."""
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
        """Create a Label + Entry pair on a grid."""
        tk.Label(parent, text=label, bg=theme.UI_COLOR, fg=theme.BUTTON_TEXT_COLOR).grid(
            row=row, column=col, padx=5, pady=4, sticky="e"
        )
        entry = tk.Entry(parent, bg=theme.BUTTON_BG_COLOR, fg=theme.BUTTON_TEXT_COLOR,
                         insertbackground=theme.BUTTON_TEXT_COLOR)
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
        """Add a button at the given linear index."""
        row, col = divmod(index, self.columns)
        self.frame.grid_rowconfigure(row, weight=1, uniform="row")
        btn = ttk.Button(self.frame, text=text, command=command)
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        return btn

    def add_dropdown(self, values: list[str], default: str, on_select, index: int):
        """Add a dropdown at the given linear index."""
        row, col = divmod(index, self.columns)
        self.frame.grid_rowconfigure(row, weight=1, uniform="row")
        return WidgetFactory.dropdown(
            self.frame, values, default, on_select,
            row=row, column=col, padx=4, pady=4, sticky="nsew"
        )
