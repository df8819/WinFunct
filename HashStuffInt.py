import tkinter as tk
from tkinter import ttk
import hashlib


class HashStuff:
    def __init__(self, parent):
        self.root = parent
        self.setup_ui()

    def hash_text(self):
        input_string = self.entry_text.get()
        selected_algo = self.hash_algo.get()
        hasher = getattr(hashlib, selected_algo)()  # Dynamically get the hashing function
        hasher.update(input_string.encode('utf-8'))
        self.hash_output.set(hasher.hexdigest())

    def exit_app(self):
        self.root.destroy()

    def setup_ui(self):
        self.root.title("Hash Generator")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 960
        window_height = 200
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        self.root.resizable(width=False, height=False)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.entry_text = tk.StringVar()
        self.hash_output = tk.StringVar()
        self.hash_algo = tk.StringVar(value='sha512')

        ttk.Label(self.root, text="Hash Algorithm:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        hash_options = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
        dropdown = ttk.Combobox(self.root, textvariable=self.hash_algo, values=hash_options, state="readonly", width=60)
        dropdown.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

        ttk.Label(self.root, text="Enter Password to Hash:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry = ttk.Entry(self.root, textvariable=self.entry_text, width=60)
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.root, text="Hashed Output:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        output = ttk.Entry(self.root, textvariable=self.hash_output, state="readonly", width=60)
        output.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        hash_button = ttk.Button(button_frame, text="Hash", command=self.hash_text)
        hash_button.pack(side=tk.LEFT, padx=(0, 10))

        exit_button = ttk.Button(button_frame, text="Exit", command=self.exit_app)
        exit_button.pack(side=tk.LEFT)

        self.root.grid_columnconfigure(1, weight=1)


def main():
    root = tk.Tk()
    app = HashStuff(root)
    root.mainloop()


if __name__ == "__main__":
    main()
