import tkinter as tk
from tkinter import colorchooser


class SimpleColorPicker:
    def __init__(self, parent):
        self.root = parent
        self.init_ui()
        self.center_window(400, 200)  # Increased size and centered

    def init_ui(self):
        # Label to display chosen color
        self.color_label = tk.Label(self.root, text="Color Preview", bg="#ffffff", width=30)
        self.color_label.pack(pady=20)

        # Button to open color picker
        self.pick_color_button = tk.Button(self.root, text="Select Color", command=self.pick_color)
        self.pick_color_button.pack(pady=10)

        # Button to copy color code
        self.copy_button = tk.Button(self.root, text="Copy Color Code", command=self.copy_color_code, state=tk.DISABLED)
        self.copy_button.pack(pady=10)

        self.chosen_color = None  # To store the chosen color code

    def pick_color(self):
        # Open color picker dialog
        color_code = colorchooser.askcolor(title="Choose a color")

        # If a color was chosen (user didn't cancel)
        if color_code:
            self.chosen_color = color_code[1]  # Extract the hex color code

            # Update the background of the label to the chosen color
            self.color_label.config(bg=self.chosen_color, text=f"Color: {self.chosen_color}")

            # Enable the copy button
            self.copy_button.config(state=tk.NORMAL)

    def copy_color_code(self):
        if self.chosen_color:
            self.root.clipboard_clear()  # Clear clipboard
            self.root.clipboard_append(self.chosen_color)  # Copy color code to clipboard
            self.root.update()  # Keeps the clipboard content available after the app closes
            self.copy_button.config(text="Copied!")

    def center_window(self, width, height):
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")


def main():
    root = tk.Tk()
    root.title("Color Picker")
    app = SimpleColorPicker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
