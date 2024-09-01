import tkinter as tk
from tkinter import colorchooser, messagebox
import json


class UISelector:
    def __init__(self, master, current_theme, update_callback):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Theme Selector")
        self.window.geometry("380x230")
        self.window.configure(bg=current_theme["UI_COLOR"])


        self.current_theme = current_theme
        self.update_callback = update_callback
        self.theme_elements = [
            "UI_COLOR", "BUTTON_BG_COLOR", "BUTTON_TEXT_COLOR",
            "BOTTOM_BORDER_COLOR", "VERSION_LABEL_TEXT"
        ]

        self.themes = self.load_themes_from_json()
        self.create_widgets()

    def load_themes_from_json(self):
        try:
            with open('UI_themes.json', 'r') as f:
                data = json.load(f)
                if 'themes' in data and isinstance(data['themes'], list):
                    return data['themes']
                else:
                    messagebox.showwarning("Invalid Format", "UI_themes.json is not in the correct format. Starting with empty theme list.")
                    return []
        except FileNotFoundError:
            messagebox.showerror("Error", "UI_themes.json file not found.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in UI_themes.json.")
            return []

    def create_widgets(self):
        for i, element in enumerate(self.theme_elements):
            tk.Label(self.window, text=element, bg=self.current_theme["UI_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"]).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(self.window, bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"], insertbackground=self.current_theme["BUTTON_TEXT_COLOR"])
            entry.insert(0, self.current_theme.get(element, ""))
            entry.grid(row=i, column=1, padx=5, pady=5)
            tk.Button(self.window, text="Pick", command=lambda e=entry: self.pick_color(e),
                      bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"],
                      activebackground=self.current_theme["UI_COLOR"], activeforeground=self.current_theme["BUTTON_TEXT_COLOR"],
                      width=7).grid(row=i, column=2, padx=5, pady=5)

        self.theme_var = tk.StringVar(self.window)
        self.theme_var.set("Select a theme")
        self.theme_dropdown = tk.OptionMenu(self.window, self.theme_var, "Select a theme", *[theme['name'] for theme in self.themes], command=self.on_theme_select)
        self.theme_dropdown.config(width=20, bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"],
                                   activebackground=self.current_theme["UI_COLOR"], activeforeground=self.current_theme["BUTTON_TEXT_COLOR"])
        self.theme_dropdown["menu"].config(bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"])
        self.theme_dropdown.grid(row=len(self.theme_elements), column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        tk.Button(self.window, text="Set UI", command=self.set_ui, width=10,
                  bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"],
                  activebackground=self.current_theme["UI_COLOR"], activeforeground=self.current_theme["BUTTON_TEXT_COLOR"]).grid(row=len(self.theme_elements), column=2, pady=10, padx=5, sticky="e")
        self.center_window()

    def center_window(self):
        # Get the window size
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()

        # Get the screen size
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window position
        self.window.geometry(f'+{x}+{y}')
        self.window.deiconify()  # Show the window

    def pick_color(self, entry):
        color = colorchooser.askcolor()[1]
        if color:
            entry.delete(0, tk.END)
            entry.insert(0, color)

    def set_ui(self):
        new_theme = {}
        for i, element in enumerate(self.theme_elements):
            new_theme[element] = self.window.grid_slaves(row=i, column=1)[0].get()

        self.update_callback(new_theme)
        self.current_theme = new_theme
        self.update_ui()  # Update the UISelector's own UI
        self.master.update_ui(new_theme)  # Update the Application's UI

    def update_ui(self):
        self.window.configure(bg=self.current_theme["UI_COLOR"])
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.current_theme["UI_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"])
        self.theme_dropdown.configure(bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"])
        self.theme_dropdown["menu"].configure(bg=self.current_theme["BUTTON_BG_COLOR"], fg=self.current_theme["BUTTON_TEXT_COLOR"])

    def on_theme_select(self, theme_name):
        selected_theme = next((theme for theme in self.themes if theme['name'] == theme_name), None)
        if selected_theme:
            for i, element in enumerate(self.theme_elements):
                entry = self.window.grid_slaves(row=i, column=1)[0]
                entry.delete(0, tk.END)
                entry.insert(0, selected_theme[element])

            # Automatically apply the selected theme
            self.set_ui()
