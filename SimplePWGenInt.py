import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import string
import random


class SimplePWGen:
    def __init__(self, parent):
        self.root = parent
        self.init_ui()
        self.reset_ui()

    def init_ui(self):
        self.tab_control = ttk.Notebook(self.root)

        self.password_tab = ttk.Frame(self.tab_control)
        self.number_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.password_tab, text='Password Generator')
        self.tab_control.add(self.number_tab, text='Random Number Generator')

        self.create_password_generator_ui()
        self.create_number_generator_ui()

        self.tab_control.pack(expand=1, fill='both')

    def create_password_generator_ui(self):
        self.password_entry = tk.Entry(self.password_tab, width=24)
        self.password_entry.pack(fill='x', padx=10, pady=10)

        self.length_scale = tk.Scale(self.password_tab, from_=6, to_=128, orient='horizontal', label='Password length')
        self.length_scale.set(20)
        self.length_scale.pack(fill='x', padx=10)

        self.var_upper = tk.BooleanVar(value=True)
        self.check_upper = tk.Checkbutton(self.password_tab, text="Uppercase Letters", variable=self.var_upper, anchor='w')
        self.check_upper.pack(fill='x', padx=10)

        self.var_lower = tk.BooleanVar(value=True)
        self.check_lower = tk.Checkbutton(self.password_tab, text="Lowercase Letters", variable=self.var_lower, anchor='w')
        self.check_lower.pack(fill='x', padx=10)

        self.var_digit = tk.BooleanVar(value=True)
        self.check_digit = tk.Checkbutton(self.password_tab, text="Digits", variable=self.var_digit, anchor='w')
        self.check_digit.pack(fill='x', padx=10)

        self.var_special = tk.BooleanVar(value=False)
        self.check_special = tk.Checkbutton(self.password_tab, text="Special Characters", variable=self.var_special, anchor='w')
        self.check_special.pack(fill='x', padx=10)
        self.button_frame_password = tk.Frame(self.password_tab)
        self.button_frame_password.pack(pady=20)

        self.reset_button = tk.Button(self.button_frame_password, text="Reset UI", command=self.reset_ui, bg='grey', fg='white')
        self.reset_button.pack(side='left', padx=(0, 50))

        self.generate_button = tk.Button(self.button_frame_password, text="Generate Password", command=self.update_password, bg='light blue')
        self.generate_button.pack(side='right', padx=5)

        self.copy_password_button = tk.Button(self.button_frame_password, text="Copy Password", command=lambda: self.copy_to_clipboard(self.password_entry))
        self.copy_password_button.pack(side='right', pady=5)

    def create_number_generator_ui(self):
        self.number_entry_label = tk.Label(self.number_tab, text="Random Number:")
        self.number_entry_label.pack(side='top', pady=(10, 0))

        self.number_entry = tk.Entry(self.number_tab, width=24)
        self.number_entry.pack(fill='x', padx=10, pady=5)

        self.digits_label = tk.Label(self.number_tab, text="Amount of Digits:")
        self.digits_label.pack(side='top', pady=(10, 0))

        self.digits_entry = tk.Entry(self.number_tab, width=12)
        self.digits_entry.pack(padx=10, pady=5)

        self.button_frame_number = tk.Frame(self.number_tab)
        self.button_frame_number.pack(pady=20)

        self.reset_button = tk.Button(self.button_frame_number, text="Reset UI", command=self.reset_ui, bg='grey', fg='white')
        self.reset_button.pack(side='left', padx=(0, 50))

        self.generate_number_button = tk.Button(self.button_frame_number, text="Generate Number", command=self.update_random_number, bg='light blue')
        self.generate_number_button.pack(side='right', padx=5)

        self.copy_number_button = tk.Button(self.button_frame_number, text="Copy Number", command=lambda: self.copy_to_clipboard(self.number_entry))
        self.copy_number_button.pack(side='right', pady=5)

    def generate_password(self, length, use_uppercase, use_lowercase, use_digits, use_specials):
        characters = ""
        guaranteed_characters = []

        if use_uppercase:
            characters += string.ascii_uppercase
            guaranteed_characters.append(secrets.choice(string.ascii_uppercase))
        if use_lowercase:
            characters += string.ascii_lowercase
            guaranteed_characters.append(secrets.choice(string.ascii_lowercase))
        if use_digits:
            characters += string.digits
            guaranteed_characters.append(secrets.choice(string.digits))
        if use_specials:
            characters += string.punctuation
            guaranteed_characters.append(secrets.choice(string.punctuation))

        if characters and length >= len(guaranteed_characters):
            remaining_length = length - len(guaranteed_characters)
            random_characters = ''.join(secrets.choice(characters) for _ in range(remaining_length))
            final_password = guaranteed_characters + list(random_characters)
            random.shuffle(final_password)
            return ''.join(final_password)
        else:
            messagebox.showwarning("Warning",
                                   "Please select at least one character type, and ensure password length is sufficient!")
            return ""

    def update_password(self):
        length = int(self.length_scale.get())
        use_uppercase = self.var_upper.get()
        use_lowercase = self.var_lower.get()
        use_digits = self.var_digit.get()
        use_specials = self.var_special.get()
        new_password = self.generate_password(length, use_uppercase, use_lowercase, use_digits, use_specials)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)

    def generate_random_number(self, digits):
        if digits == 0:
            return ''
        return ''.join([str(random.randint(0, 9)) for _ in range(digits)])

    def update_random_number(self):
        digits_str = self.digits_entry.get()

        if not digits_str.isdigit() or not digits_str:
            messagebox.showinfo("Error", "Please enter a number.")
            return

        digits = int(digits_str)
        if digits > 0:
            random_number = self.generate_random_number(digits)
            self.number_entry.delete(0, tk.END)
            self.number_entry.insert(0, random_number)
        else:
            messagebox.showinfo("Error", "Number must be greater than 0.")

    def copy_to_clipboard(self, entry_widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(entry_widget.get())

    def center_window(self, width=400, height=300):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def reset_ui(self):
        self.center_window(400, 300)


def main():
    root = tk.Tk()
    root.title("Password and Random Number Generator")
    app = SimplePWGen(root)
    app.center_window(400, 300)

    root.resizable(True, True)
    root.mainloop()


if __name__ == "__main__":
    main()
