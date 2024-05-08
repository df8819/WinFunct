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
        # Initialize the tab control and add the tabs
        self.tab_control = ttk.Notebook(self.root)

        self.password_tab = ttk.Frame(self.tab_control)
        self.number_tab = ttk.Frame(self.tab_control)
        self.passphrase_tab = ttk.Frame(self.tab_control)  # New Tab

        self.tab_control.add(self.password_tab, text='Password Generator')
        self.tab_control.add(self.passphrase_tab, text='Passphrase Generator')  # Add New Tab
        self.tab_control.add(self.number_tab, text='Random Number Generator')

        # Create UI elements for each tab
        self.create_password_generator_ui()
        self.create_number_generator_ui()
        self.create_passphrase_generator_ui()  # Create Passphrase UI

        # Pack the tabs into the main window
        self.tab_control.pack(expand=1, fill='both')

    def create_password_generator_ui(self):
        # UI for Password Generator Tab
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

    def create_passphrase_generator_ui(self):
        # UI for Passphrase Generator Tab
        self.passphrase_entry = tk.Entry(self.passphrase_tab, width=24)
        self.passphrase_entry.pack(fill='x', padx=10, pady=10)

        self.word_count_scale = tk.Scale(self.passphrase_tab, from_=3, to_=20, orient='horizontal', label='Number of Words')
        self.word_count_scale.set(6)
        self.word_count_scale.pack(fill='x', padx=10)

        self.var_include_number = tk.BooleanVar(value=True)
        self.check_include_number = tk.Checkbutton(self.passphrase_tab, text="Include Number", variable=self.var_include_number, anchor='w')
        self.check_include_number.pack(fill='x', padx=10)

        self.var_include_special = tk.BooleanVar(value=False)
        self.check_include_special = tk.Checkbutton(self.passphrase_tab, text="Include Special Character", variable=self.var_include_special, anchor='w')
        self.check_include_special.pack(fill='x', padx=10)

        self.var_include_upper = tk.BooleanVar(value=False)
        self.check_include_upper = tk.Checkbutton(self.passphrase_tab, text="Include Uppercase Letter", variable=self.var_include_upper, anchor='w')
        self.check_include_upper.pack(fill='x', padx=10)

        self.button_frame_passphrase = tk.Frame(self.passphrase_tab)
        self.button_frame_passphrase.pack(pady=20)

        self.reset_button_passphrase = tk.Button(self.button_frame_passphrase, text="Reset UI", command=self.reset_ui, bg='grey', fg='white')
        self.reset_button_passphrase.pack(side='left', padx=(0, 50))

        self.generate_button_passphrase = tk.Button(self.button_frame_passphrase, text="Generate Passphrase", command=self.update_passphrase, bg='light blue')
        self.generate_button_passphrase.pack(side='right', padx=5)

        self.copy_passphrase_button = tk.Button(self.button_frame_passphrase, text="Copy Passphrase", command=lambda: self.copy_to_clipboard(self.passphrase_entry))
        self.copy_passphrase_button.pack(side='right', pady=5)

    def update_passphrase(self):
        word_count = int(self.word_count_scale.get())
        include_number = self.var_include_number.get()
        include_special = self.var_include_special.get()
        include_upper = self.var_include_upper.get()

        new_passphrase = self.generate_passphrase(word_count, include_number, include_special, include_upper)
        self.passphrase_entry.delete(0, tk.END)
        self.passphrase_entry.insert(0, new_passphrase)

    def generate_passphrase(self, word_count, include_number, include_special, include_upper):
        """Generate a passphrase using the EFF wordlist format."""
        eff_wordlist = self.load_eff_wordlist('eff_wordlist.txt')  # Path to the EFF wordlist
        words = []

        # Generate random five-digit numbers and map to words
        for _ in range(word_count):
            roll = ''.join([str(random.randint(1, 6)) for _ in range(5)])
            word = eff_wordlist.get(roll)
            if word:
                words.append(word)

        # If requested, capitalize a random word
        if include_upper and words:
            index = random.randint(0, len(words) - 1)
            words[index] = words[index].capitalize()

        # Add number and/or special character at the end of a random word if required
        if include_number:
            index = random.randint(0, len(words) - 1)
            words[index] += str(random.randint(0, 9))

        if include_special:
            index = random.randint(0, len(words) - 1)
            words[index] += secrets.choice(string.punctuation)

        passphrase = '-'.join(words)
        return passphrase

    def load_eff_wordlist(self, filepath):
        """Load the EFF wordlist into a dictionary."""
        eff_dict = {}
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    eff_dict[parts[0]] = parts[1]
        return eff_dict

    def create_number_generator_ui(self):
        # UI for Random Number Generator Tab
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
        # Password generation logic
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
            messagebox.showwarning("Warning", "Please select at least one character type, and ensure password length is sufficient!")
            return ""

    def update_password(self):
        # Update the password
        length = int(self.length_scale.get())
        use_uppercase = self.var_upper.get()
        use_lowercase = self.var_lower.get()
        use_digits = self.var_digit.get()
        use_specials = self.var_special.get()
        new_password = self.generate_password(length, use_uppercase, use_lowercase, use_digits, use_specials)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)

    def generate_random_number(self, digits):
        # Random number generation logic
        if digits == 0:
            return ''
        return ''.join([str(random.randint(0, 9)) for _ in range(digits)])

    def update_random_number(self):
        # Update the random number
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
        # Copy the generated value to the clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(entry_widget.get())

    def center_window(self, width=400, height=300):
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def reset_ui(self):
        # Reset the UI to its default state
        self.center_window(400, 300)

# Main function to run the application
def main():
    root = tk.Tk()
    root.title("Password and Random Number Generator")
    app = SimplePWGen(root)
    app.center_window(400, 300)

    root.resizable(True, True)
    root.mainloop()

if __name__ == "__main__":
    main()
