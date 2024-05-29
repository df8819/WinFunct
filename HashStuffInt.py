import tkinter as tk
from tkinter import ttk
import hashlib
import threading
import itertools
import string
from tkinter import messagebox
from tkinter import simpledialog


class HashStuff:
    def __init__(self, parent):
        self.root = parent
        self.setup_ui()
        self.stop_event = threading.Event()  # Event to signal the thread to stop

    def hash_text(self):
        input_string = self.entry_text.get()
        selected_algo = self.hash_algo.get()
        hasher = getattr(hashlib, selected_algo)()
        hasher.update(input_string.encode('utf-8'))
        self.hash_output.set(hasher.hexdigest())

    def transfer_hash(self):
        # Transfer the hash from the "Hashed Output" to the "Enter Hash for Password"
        self.password_hash.set(self.hash_output.get())
        # Clear the "Hashed Output" field
        self.hash_output.set('')

    def calculate_password(self):
        self.character_options()

    def character_options(self):
        # Dialog to select character types
        self.chars_to_use = {'Letters': False, 'Digits': False, 'Special': False}

        options_window = tk.Toplevel(self.root)
        options_window.title("Character Types in Password?")

        # Use the options_window's screen dimensions to center it
        screen_width = options_window.winfo_screenwidth()
        screen_height = options_window.winfo_screenheight()
        window_width = 360
        window_height = 120
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        # Adjust options_window size and position, not self.root
        options_window.resizable(width=False, height=False)
        options_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        tk.Checkbutton(options_window, text="Letters (A/a)", variable=tk.BooleanVar(value=False),
                       command=lambda: self.toggle_chars('Letters')).grid(row=0, column=0, sticky="w")
        tk.Checkbutton(options_window, text="Digits (0-9)", variable=tk.BooleanVar(value=False),
                       command=lambda: self.toggle_chars('Digits')).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(options_window, text="Special (#*!..)", variable=tk.BooleanVar(value=False),
                       command=lambda: self.toggle_chars('Special')).grid(row=2, column=0, sticky="w")

        ttk.Button(options_window, text="OK", command=lambda: [options_window.destroy(), self.start_brute_force_search()]).grid(row=3, column=0, sticky="ew")

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

        # Proceed with the calculation if at least one character type is selected
        if chars:
            self.stop_event.clear()  # Reset the stop event for a new calculation
            self.calculation_thread = threading.Thread(target=lambda: self.brute_force_search(chars), daemon=True)
            self.calculation_thread.start()
        else:
            messagebox.showwarning("Warning", "Please select at least one character type for the password.")

    def brute_force_search(self, chars):
        target_hash = self.password_hash.get()
        selected_algo = self.hash_algo.get()
        found = False
        max_length = 8

        for length in range(1, max_length + 1):
            for test_string in itertools.product(chars, repeat=length):
                test_string = ''.join(test_string)
                hasher = getattr(hashlib, selected_algo)()
                hasher.update(test_string.encode())
                if self.stop_event.is_set():
                    self.possible_password.set("Calculation stopped by user.")
                    return
                if hasher.hexdigest() == target_hash:
                    self.possible_password.set(test_string)
                    return
        if not found:
            if self.stop_event.is_set():
                self.possible_password.set("Calculation stopped by user.")
            else:
                self.possible_password.set("Not found")

    def stop_calculation(self):
        self.stop_event.set()  # Signal the thread to stop

    def exit_app(self):
        self.root.destroy()

    def setup_ui(self):
        self.root.title("Hash Generator")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 960
        window_height = 250
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        self.root.resizable(width=False, height=False)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.entry_text = tk.StringVar()
        self.hash_output = tk.StringVar()
        self.possible_password = tk.StringVar()
        self.hash_algo = tk.StringVar(value='sha256')
        self.password_hash = tk.StringVar()

        hash_options = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
        layout_options = {'padx': 10, 'pady': 10, 'sticky': 'ew'}

        ttk.Label(self.root, text="Hash Algorithm:").grid(row=0, column=0, **layout_options)
        ttk.Combobox(self.root, textvariable=self.hash_algo, values=hash_options, state="readonly", width=60).grid(row=0, column=1, **layout_options)

        ttk.Label(self.root, text="Enter Password to Hash:").grid(row=1, column=0, **layout_options)
        ttk.Entry(self.root, textvariable=self.entry_text, width=60).grid(row=1, column=1, **layout_options)

        ttk.Label(self.root, text="Hashed Output:").grid(row=2, column=0, **layout_options)
        ttk.Entry(self.root, textvariable=self.hash_output, state="readonly", width=60).grid(row=2, column=1, **layout_options)

        ttk.Label(self.root, text="Enter Hash for Password:").grid(row=3, column=0, **layout_options)
        ttk.Entry(self.root, textvariable=self.password_hash, width=60).grid(row=3, column=1, **layout_options)

        ttk.Label(self.root, text="Possible Password:").grid(row=4, column=0, **layout_options)
        ttk.Entry(self.root, textvariable=self.possible_password, state="readonly", width=60).grid(row=4, column=1, **layout_options)

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=5, column=0, columnspan=2, **layout_options)

        ttk.Button(button_frame, text="Hash", command=self.hash_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Transfer Hash", command=self.transfer_hash).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calculate Password", command=self.calculate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.exit_app).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Stop Calculation", command=self.stop_calculation).pack(side=tk.RIGHT, padx=5)

        self.root.grid_columnconfigure(1, weight=1)


def main():
    root = tk.Tk()
    app = HashStuff(root)
    root.mainloop()


if __name__ == "__main__":
    main()
