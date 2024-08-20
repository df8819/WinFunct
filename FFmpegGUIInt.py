# Testng integration of a converter🙂
# Idk if this stays or will be integrated/finished at all..🤷‍♂️

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class FFmpegGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg GUI")
        self.file_path = ""

        # Center the GUI
        self.center_window(400, 300)

        # Check if FFmpeg is installed
        self.check_ffmpeg_installation()

        # Create and place widgets
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Button to select file
        self.select_file_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # Dropdown menu for operations
        self.operation_var = tk.StringVar(self.root)
        self.operation_var.set("Select Operation")
        self.operations = [
            "Convert to MP4", "Extract Audio", "Convert to GIF",
            "Resize Video", "Change Bitrate", "Trim Video"
        ]
        self.operation_menu = tk.OptionMenu(self.root, self.operation_var, *self.operations, command=self.show_options)
        self.operation_menu.pack(pady=10)

        # Frame for additional options
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

        # Button to execute the selected operation
        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute_operation)
        self.execute_button.pack(pady=20)

    def check_ffmpeg_installation(self):
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            install = messagebox.askyesno("FFmpeg Not Found", "FFmpeg is not installed. Do you want to install it?")
            if install:
                self.install_ffmpeg()

    def install_ffmpeg(self):
        # Replace with your method to install ffmpeg
        print("Installing FFmpeg...")

    def select_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a file")
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {self.file_path}")

    def show_options(self, operation):
        # Clear any existing option fields
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Add fields depending on the operation selected
        if operation == "Resize Video":
            tk.Label(self.options_frame, text="Width:").grid(row=0, column=0)
            self.width_entry = tk.Entry(self.options_frame)
            self.width_entry.grid(row=0, column=1)

            tk.Label(self.options_frame, text="Height:").grid(row=1, column=0)
            self.height_entry = tk.Entry(self.options_frame)
            self.height_entry.grid(row=1, column=1)

        elif operation == "Convert to GIF":
            tk.Label(self.options_frame, text="Frame Rate (fps):").grid(row=0, column=0)
            self.fps_entry = tk.Entry(self.options_frame)
            self.fps_entry.grid(row=0, column=1)

        elif operation == "Change Bitrate":
            tk.Label(self.options_frame, text="Bitrate (e.g., 1M, 500k):").grid(row=0, column=0)
            self.bitrate_entry = tk.Entry(self.options_frame)
            self.bitrate_entry.grid(row=0, column=1)

        elif operation == "Trim Video":
            tk.Label(self.options_frame, text="Start Time (HH:MM:SS):").grid(row=0, column=0)
            self.start_time_entry = tk.Entry(self.options_frame)
            self.start_time_entry.grid(row=0, column=1)

            tk.Label(self.options_frame, text="End Time (HH:MM:SS):").grid(row=1, column=0)
            self.end_time_entry = tk.Entry(self.options_frame)
            self.end_time_entry.grid(row=1, column=1)

    def execute_operation(self):
        if not self.file_path:
            messagebox.showwarning("No File Selected", "Please select a file first.")
            return

        operation = self.operation_var.get()
        if operation == "Select Operation":
            messagebox.showwarning("No Operation Selected", "Please select an operation from the dropdown menu.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".mp4", title="Save Output As")
        if not output_file:
            return

        # Determine command based on selected operation
        if operation == "Convert to MP4":
            command = f'ffmpeg -i "{self.file_path}" "{output_file}"'

        elif operation == "Extract Audio":
            command = f'ffmpeg -i "{self.file_path}" -q:a 0 -map a "{output_file}"'

        elif operation == "Convert to GIF":
            fps = self.fps_entry.get() if self.fps_entry else "10"
            command = f'ffmpeg -i "{self.file_path}" -vf "fps={fps},scale=320:-1" "{output_file}"'

        elif operation == "Resize Video":
            width = self.width_entry.get() if self.width_entry else "640"
            height = self.height_entry.get() if self.height_entry else "480"
            command = f'ffmpeg -i "{self.file_path}" -vf "scale={width}:{height}" "{output_file}"'

        elif operation == "Change Bitrate":
            bitrate = self.bitrate_entry.get() if self.bitrate_entry else "1M"
            command = f'ffmpeg -i "{self.file_path}" -b:v {bitrate} "{output_file}"'

        elif operation == "Trim Video":
            start_time = self.start_time_entry.get() if self.start_time_entry else "00:00:00"
            end_time = self.end_time_entry.get() if self.end_time_entry else "00:00:10"
            command = f'ffmpeg -i "{self.file_path}" -ss {start_time} -to {end_time} -c copy "{output_file}"'

        else:
            messagebox.showerror("Error", "Unknown operation.")
            return

        # Run the command
        subprocess.run(command, shell=True)
        messagebox.showinfo("Operation Completed", f"Operation '{operation}' completed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FFmpegGUI(root)
    root.mainloop()
