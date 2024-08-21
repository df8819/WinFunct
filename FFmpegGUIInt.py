import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


class FFmpegGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg GUI")
        self.file_paths = []  # List to hold selected file paths

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
        # Button to select files
        self.select_files_button = tk.Button(self.root, text="Select Files", command=self.select_files)
        self.select_files_button.pack(pady=10)

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

    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(title="Select files")
        if self.file_paths:
            messagebox.showinfo("Files Selected", f"Selected files: {', '.join(self.file_paths)}")

    def show_options(self, operation):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Add appropriate options based on the selected operation
        if operation == "Resize Video":
            tk.Label(self.options_frame, text="Width (default 640):").grid(row=0, column=0)
            self.width_entry = tk.Entry(self.options_frame)
            self.width_entry.insert(0, "640")
            self.width_entry.grid(row=0, column=1)

            tk.Label(self.options_frame, text="Height (default 480):").grid(row=1, column=0)
            self.height_entry = tk.Entry(self.options_frame)
            self.height_entry.insert(0, "480")
            self.height_entry.grid(row=1, column=1)

        elif operation == "Convert to GIF":
            tk.Label(self.options_frame, text="Frame Rate (fps, e.g. 10):").grid(row=0, column=0)
            self.fps_entry = tk.Entry(self.options_frame)
            self.fps_entry.insert(0, "10")
            self.fps_entry.grid(row=0, column=1)

        elif operation == "Change Bitrate":
            tk.Label(self.options_frame, text="Bitrate (e.g., 1M or 500k):").grid(row=0, column=0)
            self.bitrate_entry = tk.Entry(self.options_frame)
            self.bitrate_entry.insert(0, "1M")
            self.bitrate_entry.grid(row=0, column=1)

        elif operation == "Trim Video":
            tk.Label(self.options_frame, text="Start Time (HH:MM:SS, default 00:00:00):").grid(row=0, column=0)
            self.start_time_entry = tk.Entry(self.options_frame)
            self.start_time_entry.insert(0, "00:00:00")
            self.start_time_entry.grid(row=0, column=1)

            tk.Label(self.options_frame, text="End Time (HH:MM:SS, default 00:00:10):").grid(row=1, column=0)
            self.end_time_entry = tk.Entry(self.options_frame)
            self.end_time_entry.insert(0, "00:00:10")
            self.end_time_entry.grid(row=1, column=1)

    def execute_operation(self):
        if not self.file_paths:
            messagebox.showwarning("No File Selected", "Please select files first.")
            return

        operation = self.operation_var.get()
        if operation == "Select Operation":
            messagebox.showwarning("No Operation Selected", "Please select an operation from the dropdown menu.")
            return

        output_paths = []
        for file_path in self.file_paths:
            output_file = filedialog.asksaveasfilename(defaultextension=".mp4", title="Save Output As")
            if not output_file:
                return

            # Build and run command
            command = self.build_command(operation, file_path, output_file)
            if command:
                subprocess.run(command, shell=True)
                output_paths.append(output_file)

        messagebox.showinfo("Operation Completed", f"Operation '{operation}' completed successfully for files: {', '.join(output_paths)}!")

    def build_command(self, operation, file_path, output_file):
        if operation == "Convert to MP4":
            return f'ffmpeg -i "{file_path}" "{output_file}"'

        elif operation == "Extract Audio":
            return f'ffmpeg -i "{file_path}" -q:a 0 -map a "{output_file}"'

        elif operation == "Convert to GIF":
            fps = self.fps_entry.get() if self.fps_entry else "10"
            return f'ffmpeg -i "{file_path}" -vf "fps={fps},scale=320:-1" "{output_file}"'

        elif operation == "Resize Video":
            width = self.width_entry.get() if self.width_entry else "640"
            height = self.height_entry.get() if self.height_entry else "480"
            return f'ffmpeg -i "{file_path}" -vf "scale={width}:{height}" "{output_file}"'

        elif operation == "Change Bitrate":
            bitrate = self.bitrate_entry.get() if self.bitrate_entry else "1M"
            return f'ffmpeg -i "{file_path}" -b:v {bitrate} "{output_file}"'

        elif operation == "Trim Video":
            start_time = self.start_time_entry.get() if self.start_time_entry else "00:00:00"
            end_time = self.end_time_entry.get() if self.end_time_entry else "00:00:10"
            return f'ffmpeg -i "{file_path}" -ss {start_time} -to {end_time} -c copy "{output_file}"'

        return None

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


if __name__ == "__main__":
    root = tk.Tk()
    app = FFmpegGUI(root)
    root.mainloop()
