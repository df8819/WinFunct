"""Theme and style management."""
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from tkinter import ttk
from typing import Optional


@dataclass
class Theme:
    UI_COLOR: str = "#e4e4e4"
    BUTTON_BG_COLOR: str = "#d4d4d4"
    BUTTON_TEXT_COLOR: str = "#000000"
    BOTTOM_BORDER_COLOR: str = "#5b5b5b"
    VERSION_LABEL_TEXT: str = "#5f5f5f"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Theme":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


THEME_FILE = Path("last_selected_theme.json")
THEMES_FILE = Path("UI_themes.json")


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
                             background=t.BUTTON_BG_COLOR, foreground=t.BUTTON_TEXT_COLOR)
        self.style.map("TNotebook.Tab",
                       background=[("selected", t.UI_COLOR)],
                       foreground=[("selected", t.BUTTON_TEXT_COLOR)])

        # Frames
        self.style.configure("TFrame", background=t.UI_COLOR)
        self.style.configure("Bottom.TFrame", background=t.BOTTOM_BORDER_COLOR)

        # Buttons
        self.style.configure("TButton",
                             padding=(10, 5),
                             background=t.BUTTON_BG_COLOR,
                             foreground=t.BUTTON_TEXT_COLOR,
                             relief="solid", # flat, raised, sunken, ridge, groove, solid
                             borderwidth=2)
        self.style.map("TButton",
                       background=[("active", t.UI_COLOR), ("pressed", t.BOTTOM_BORDER_COLOR)],
                       foreground=[("active", t.BUTTON_TEXT_COLOR)],
                       relief=[("pressed", "sunken")])

        # Combobox
        self.style.configure("TCombobox",
                             fieldbackground=t.BUTTON_BG_COLOR,
                             background=t.BUTTON_BG_COLOR,
                             foreground=t.BUTTON_TEXT_COLOR,
                             arrowcolor=t.BUTTON_TEXT_COLOR)
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", t.BUTTON_BG_COLOR)],
                       foreground=[("readonly", t.BUTTON_TEXT_COLOR)])

        # Separator
        self.style.configure("TSeparator", background=t.BOTTOM_BORDER_COLOR)
