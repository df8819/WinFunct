import tkinter as tk
from tkinter import ttk
import hashlib
import threading
import itertools
import string
from tkinter import messagebox
from config import UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR


class HashStuff:
    def __init__(self, parent, ui_color, button_bg_color, button_text_color):
        print("Initializing Hash Generator")
        self.root = parent
        self.UI_COLOR = ui_color
        self.BUTTON_BG_COLOR = button_bg_color
        self.BUTTON_TEXT_COLOR = button_text_color
        self.setup_ui()
        self.stop_event = threading.Event()

    def setup_ui(self):
        hash_options = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
        layout_options = {'padx': 10, 'pady': 10, 'sticky': 'nsew'}
        label_style = {"bg": self.UI_COLOR, "fg": self.BUTTON_TEXT_COLOR}
        entry_style = {"bg": self.BUTTON_BG_COLOR, "fg": self.BUTTON_TEXT_COLOR, "insertbackground": self.BUTTON_TEXT_COLOR}
        text_style = {"bg": self.BUTTON_BG_COLOR, "fg": self.BUTTON_TEXT_COLOR, "insertbackground": self.BUTTON_TEXT_COLOR, "relief": tk.SUNKEN, "borderwidth": 1}
        button_style = {"bg": self.BUTTON_BG_COLOR, "fg": self.BUTTON_TEXT_COLOR, "activebackground": self.UI_COLOR, "activeforeground": self.BUTTON_TEXT_COLOR, "width": 18}

        self.root.title("Hash Generator")
        self.root.configure(bg=self.UI_COLOR)
        window_width = 590
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.entry_text = tk.StringVar()
        self.hash_output = tk.StringVar()
        self.possible_password = tk.StringVar()
        self.hash_algo = tk.StringVar(value='Select Algorithm')
        self.password_hash = tk.StringVar()

        # Password to Hash
        tk.Label(self.root, text="Enter random Password:", **label_style).grid(row=1, column=0, **layout_options)
        self.password_entry = tk.Entry(self.root, textvariable=self.entry_text, width=50, **entry_style)
        self.password_entry.grid(row=1, column=1, **layout_options)

        # Hashed Output
        tk.Label(self.root, text="Hashed Output:", **label_style).grid(row=2, column=0, **layout_options)
        self.hashed_text = tk.Text(self.root, height=2, width=50, wrap=tk.WORD, **text_style)
        self.hashed_text.grid(row=2, column=1, **layout_options)
        self.hashed_text.config(state='disabled')

        # Hash for Password
        tk.Label(self.root, text="Enter Hash for Password:", **label_style).grid(row=3, column=0, **layout_options)
        self.hash_text = tk.Text(self.root, height=2, width=50, wrap=tk.WORD, **text_style)
        self.hash_text.grid(row=3, column=1, **layout_options)

        # Possible Password
        tk.Label(self.root, text="Possible Password:", **label_style).grid(row=4, column=0, **layout_options)
        self.possible_entry = tk.Entry(self.root, textvariable=self.possible_password, width=50, **entry_style)
        self.possible_entry.grid(row=4, column=1, **layout_options)

        # Buttons and Options Menu
        button_frame = tk.Frame(self.root, bg=self.UI_COLOR)
        button_frame.grid(row=5, column=0, columnspan=2, **layout_options)

        # First line of buttons
        tk.Button(button_frame, text="Crack Password", command=self.character_options, **button_style).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Transfer Hash", command=self.transfer_hash, **button_style).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Hash Password", command=self.hash_text_func, **button_style).pack(side=tk.RIGHT, padx=5)

        # Second line with option menu and additional buttons
        options_frame = tk.Frame(self.root, bg=self.UI_COLOR)
        options_frame.grid(row=6, column=0, columnspan=2, **layout_options)
        tk.Button(options_frame, text="Exit", command=self.exit_app, **button_style).pack(side=tk.RIGHT, padx=5)
        tk.Button(options_frame, text="Stop Calculation", command=self.stop_calculation, **button_style).pack(side=tk.RIGHT, padx=5)
        self.algo_combo = tk.OptionMenu(options_frame, self.hash_algo, *hash_options)
        self.algo_combo.config(width=16, bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.UI_COLOR, activeforeground=self.BUTTON_TEXT_COLOR, highlightthickness=0)
        self.algo_combo["menu"].config(bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR)
        self.algo_combo.pack(side=tk.RIGHT, padx=5)

        # Center the button and options frames
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

    def hash_text_func(self):
        selected_algo = self.hash_algo.get()
        if selected_algo == 'Select Algorithm':
            messagebox.showwarning("Warning", "Please select a hash algorithm.", parent=self.root)
            return

        input_string = self.entry_text.get()
        hasher = getattr(hashlib, selected_algo)()
        hasher.update(input_string.encode('utf-8'))
        self.hashed_text.config(state='normal')
        self.hashed_text.delete("1.0", tk.END)
        self.hashed_text.insert(tk.END, hasher.hexdigest())
        self.hashed_text.config(state='disabled')

    def transfer_hash(self):
        hashed_output = self.hashed_text.get("1.0", tk.END).strip()
        self.hash_text.delete("1.0", tk.END)
        self.hash_text.insert(tk.END, hashed_output)
        self.hashed_text.config(state='normal')
        self.hashed_text.delete("1.0", tk.END)
        self.hashed_text.config(state='disabled')

    def character_options(self):
        self.chars_to_use = {'Letters': False, 'Digits': False, 'Special': False}
        options_window = tk.Toplevel(self.root)
        options_window.title("Character Types in Password?")
        options_window.configure(bg=self.UI_COLOR)
        options_window.attributes('-topmost', True)

        window_width = 350
        window_height = 160
        screen_width = options_window.winfo_screenwidth()
        screen_height = options_window.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        options_window.resizable(width=False, height=False)
        options_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        checkbutton_style = {
            "bg": self.UI_COLOR,
            "fg": self.BUTTON_TEXT_COLOR,
            "activebackground": self.UI_COLOR,
            "activeforeground": self.BUTTON_TEXT_COLOR,
            "selectcolor": self.BUTTON_BG_COLOR
        }
        button_style = {
            "bg": self.BUTTON_BG_COLOR,
            "fg": self.BUTTON_TEXT_COLOR,
            "activebackground": self.UI_COLOR,
            "activeforeground": self.BUTTON_TEXT_COLOR,
            "width": 18
        }

        options_frame = tk.Frame(options_window, bg=self.UI_COLOR)
        options_frame.pack(expand=True)

        tk.Checkbutton(options_frame, text="Letters (A/a)", variable=tk.BooleanVar(value=False),
                       command=lambda: self.toggle_chars('Letters'), **checkbutton_style).grid(row=0, column=0, pady=5)
        tk.Checkbutton(options_frame, text="Digits (0-9)", variable=tk.BooleanVar(value=False),
                       command=lambda: self.toggle_chars('Digits'), **checkbutton_style).grid(row=1, column=0, pady=5)
        tk.Checkbutton(options_frame, text="Special (#*!..)", variable=tk.BooleanVar(value=False),
                       command=lambda: self.toggle_chars('Special'), **checkbutton_style).grid(row=2, column=0, pady=5)

        tk.Button(options_frame, text="OK", command=lambda: [options_window.destroy(), self.start_brute_force_search()], **button_style).grid(row=3, column=0, pady=10)

        options_frame.grid_rowconfigure(0, weight=1)
        options_frame.grid_rowconfigure(1, weight=1)
        options_frame.grid_rowconfigure(2, weight=1)
        options_frame.grid_rowconfigure(3, weight=1)
        options_frame.grid_columnconfigure(0, weight=1)

    def toggle_chars(self, char_type):
        self.chars_to_use[char_type] = not self.chars_to_use[char_type]

    def start_brute_force_search(self):
        chars = ""
        if self.chars_to_use['Letters']:
            chars += string.ascii_letters
        if self.chars_to_use['Digits']:
            chars += string.digits
        if self.chars_to_use['Special']:
            chars += string.punctuation

        if chars:
            self.stop_event.clear()
            self.calculation_thread = threading.Thread(target=self.brute_force_search, args=(chars,), daemon=True)
            self.calculation_thread.start()
        else:
            messagebox.showwarning("Warning", "Please select at least one character type for the password.")

    def brute_force_search(self, chars):
        target_hash = self.hash_text.get("1.0", tk.END).strip()
        selected_algo = self.hash_algo.get()
        found = False
        max_length = 8

        for length in range(1, max_length + 1):
            for test_string in itertools.product(chars, repeat=length):
                test_string = ''.join(test_string)
                hasher = getattr(hashlib, selected_algo)()
                hasher.update(test_string.encode())

                if self.stop_event.is_set():
                    self.possible_entry.config(state='normal')
                    self.possible_entry.delete(0, tk.END)
                    self.possible_entry.insert(tk.END, "Calculation stopped by user.")
                    self.possible_entry.config(state='readonly', readonlybackground=self.BUTTON_BG_COLOR)
                    return

                if hasher.hexdigest() == target_hash:
                    self.possible_entry.config(state='normal')
                    self.possible_entry.delete(0, tk.END)
                    self.possible_entry.insert(tk.END, test_string)
                    self.possible_entry.config(state='readonly', readonlybackground=self.BUTTON_BG_COLOR)
                    return

        if not found:
            self.possible_entry.config(state='normal')
            self.possible_entry.delete(0, tk.END)
            self.possible_entry.insert(tk.END, "Not found")
            self.possible_entry.config(state='readonly', readonlybackground=self.BUTTON_BG_COLOR)

    def stop_calculation(self):
        print("""
    ╔══════════════════════╗
    ║ Calculation Stopped! ║
    ╚══════════════════════╝        
""")
        self.stop_event.set()

    def exit_app(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = HashStuff(root, UI_COLOR, BUTTON_BG_COLOR, BUTTON_TEXT_COLOR)
    root.mainloop()

if __name__ == "__main__":
    main()
