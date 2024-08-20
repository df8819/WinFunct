import tkinter as tk
from tkinter import colorchooser

class SimpleColorPicker:
    def __init__(self, parent):
        self.root = parent
        self.init_ui()
        self.center_window(515, 475)

    def init_ui(self):
        # Label for "Color Preview" text
        self.text_label = tk.Label(self.root, text="Click Window to select a color:")
        self.text_label.pack(pady=10)

        # Frame to hold the color preview
        self.preview_frame = tk.Frame(self.root, width=480, height=320, bd=2, relief=tk.SOLID)
        self.preview_frame.pack(pady=20)
        self.preview_frame.pack_propagate(False)  # Prevent the frame from shrinking

        # Label for "Color Preview" text
        self.text_label = tk.Label(self.root, text="Color Preview: None")
        self.text_label.pack()

        # Label to display chosen color (inside the frame)
        self.color_label = tk.Label(self.preview_frame, bg="#ffffff")
        self.color_label.pack(fill=tk.BOTH, expand=True)

        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Button to copy color code
        self.copy_button = tk.Button(button_frame, text="Copy Color Code", command=self.copy_color_code, state=tk.DISABLED, width=20)
        self.copy_button.pack(side=tk.LEFT, padx=10)

        # Button to exit the application
        self.exit_button = tk.Button(button_frame, text="Exit", command=self.close_window, width=20)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        self.chosen_color = None  # To store the chosen color code

        # Bind click event to the color label (which fills the entire preview frame)
        self.color_label.bind("<Button-1>", self.pick_color)

    def pick_color(self, event=None):
        # Open color picker dialog
        color_code = colorchooser.askcolor(title="Choose a color")

        # If a color was chosen (user didn't cancel)
        if color_code:
            self.chosen_color = color_code[1]  # Extract the hex color code

            # Update the background of the color label to the chosen color
            self.color_label.config(bg=self.chosen_color)

            # Update the "Color Preview" text
            self.text_label.config(text=f"Color Code: {self.chosen_color}")

            # Enable the copy button
            self.copy_button.config(state=tk.NORMAL)

    def copy_color_code(self):
        if self.chosen_color:
            self.root.clipboard_clear()  # Clear clipboard
            self.root.clipboard_append(self.chosen_color)  # Copy color code to clipboard
            self.root.update()  # Keeps the clipboard content available after the app closes
            self.copy_button.config(text="Copied!")
            # Reset the button text after a short delay
            self.root.after(1500, lambda: self.copy_button.config(text="Copy Color Code"))

    def close_window(self):
        self.root.destroy()

    def center_window(self, width, height):
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 4
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

def main():
    root = tk.Tk()
    root.title("Color Picker")
    app = SimpleColorPicker(root)
    root.mainloop()

if __name__ == "__main__":
    main()