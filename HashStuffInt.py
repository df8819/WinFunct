import tkinter as tk
from tkinter import ttk
import hashlib
import threading

class HashStuff:
    def __init__(self, parent):
        self.root = parent
        self.setup_ui()
        self.calculation_thread = None

    def hash_text(self):
        input_string = self.entry_text.get()
        selected_algo = self.hash_algo.get()
        hasher = getattr(hashlib, selected_algo)()  # Dynamically get the hashing function
        hasher.update(input_string.encode('utf-8'))
        self.hash_output.set(hasher.hexdigest())

    def calculate_password(self):
        self.calculation_thread = threading.Thread(target=self.brute_force_search, daemon=True)
        self.calculation_thread.start()

    def brute_force_search(self):
        target_hash = self.password_hash.get()
        selected_algo = self.hash_algo.get()
        found = False

        # Adjusting the range to include numbers from 0 to 99
        for number in range(0, 99999999):
            test_string = str(number)
            hasher = getattr(hashlib, selected_algo)()
            hasher.update(test_string.encode())
            if hasher.hexdigest() == target_hash:
                self.possible_password.set(test_string)
                found = True
                break

        if not found:
            self.possible_password.set("Not found")

    def stop_calculation(self):
        if self.calculation_thread is not None:
            # Not directly stoppable, so we'll use this method to demonstrate functionality
            # You would need a more complex setup to safely interrupt and manage thread state
            self.calculation_thread = None

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
        self.hash_algo = tk.StringVar(value='sha512')
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
