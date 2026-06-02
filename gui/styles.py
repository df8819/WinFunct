"""Theme and style management."""
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from tkinter import ttk
from typing import Optional

from core.utils import get_app_root


@dataclass
class Theme:
    UI_COLOR: str = "#F3F4F6"
    PANEL_COLOR: str = "#EAEBEE"
    BUTTON_BG_COLOR: str = "#D2D5DB"
    BUTTON_TEXT_COLOR: str = "#111111"
    INPUT_BG_COLOR: str = "#FFFFFF"
    INPUT_TEXT_COLOR: str = "#1C1C1E"
    ACCENT_COLOR: str = "#0A84FF"
    BOTTOM_BORDER_COLOR: str = "#0A84FF"
    VERSION_LABEL_TEXT: str = "#7D7F85"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Theme":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


THEME_FILE = get_app_root() / "last_selected_theme.json"
THEMES_FILE = get_app_root() / "UI_themes.json"


def load_saved_theme() -> Theme:
    """Load the last saved theme, or return default."""
    try:
        data = json.loads(THEME_FILE.read_text())
        return Theme.from_dict(data)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return Theme()


def save_theme(theme: Theme):
    """Persist theme to disk."""
    THEME_FILE.write_text(json.dumps(theme.to_dict(), indent=2))


def load_theme_presets() -> list[dict]:
    """Load theme presets from UI_themes.json."""
    try:
        data = json.loads(THEMES_FILE.read_text())
        return data.get("themes", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


class StyleManager:
    """Configure ttk styles based on current theme."""

    def __init__(self, theme: Theme):
        self.theme = theme
        self.style = ttk.Style()

    def apply(self):
        """Apply all styles based on current theme."""
        t = self.theme
        self.style.theme_use("default")

        # Notebook tabs
        self.style.configure("TNotebook", background=t.UI_COLOR)
        self.style.configure("TNotebook.Tab", padding=[10, 7],
                             background=t.PANEL_COLOR, foreground=t.BUTTON_TEXT_COLOR)
        self.style.map("TNotebook.Tab",
                       background=[("selected", t.UI_COLOR)],
                       foreground=[("selected", t.BUTTON_TEXT_COLOR)])

        # Frames
        self.style.configure("TFrame", background=t.UI_COLOR)
        self.style.configure("Panel.TFrame", background=t.PANEL_COLOR)
        self.style.configure("Bottom.TFrame", background=t.BOTTOM_BORDER_COLOR)

        # Buttons
        self.style.configure("TButton",
                             padding=(10, 5),
                             background=t.BUTTON_BG_COLOR,
                             foreground=t.BUTTON_TEXT_COLOR,
                             relief="solid",
                             borderwidth=2)
        self.style.map("TButton",
                       background=[("active", t.ACCENT_COLOR), ("pressed", t.ACCENT_COLOR)],
                       foreground=[("active", t.BUTTON_TEXT_COLOR)],
                       relief=[("pressed", "sunken")])

        # Accent Button (for primary actions)
        self.style.configure("Accent.TButton",
                             padding=(10, 5),
                             background=t.ACCENT_COLOR,
                             foreground=t.BUTTON_TEXT_COLOR,
                             relief="solid",
                             borderwidth=2)
        self.style.map("Accent.TButton",
                       background=[("active", t.BUTTON_BG_COLOR), ("pressed", t.BUTTON_BG_COLOR)],
                       foreground=[("active", t.BUTTON_TEXT_COLOR)])

        # Combobox
        self.style.configure("TCombobox",
                             fieldbackground=t.INPUT_BG_COLOR,
                             background=t.INPUT_BG_COLOR,
                             foreground=t.INPUT_TEXT_COLOR,
                             arrowcolor=t.INPUT_TEXT_COLOR)
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", t.INPUT_BG_COLOR)],
                       foreground=[("readonly", t.INPUT_TEXT_COLOR)])

        # Entry
        self.style.configure("TEntry",
                             fieldbackground=t.INPUT_BG_COLOR,
                             foreground=t.INPUT_TEXT_COLOR,
                             insertcolor=t.INPUT_TEXT_COLOR)

        # Separator
        self.style.configure("TSeparator", background=t.ACCENT_COLOR)

        # Treeview
        self.style.configure("Treeview",
                             background=t.PANEL_COLOR,
                             foreground=t.BUTTON_TEXT_COLOR,
                             fieldbackground=t.PANEL_COLOR)
        self.style.configure("Treeview.Heading",
                             background=t.BUTTON_BG_COLOR,
                             foreground=t.BUTTON_TEXT_COLOR)

        # LabelFrame
        self.style.configure("TLabelframe", background=t.UI_COLOR)
        self.style.configure("TLabelframe.Label", background=t.UI_COLOR, foreground=t.BUTTON_TEXT_COLOR)