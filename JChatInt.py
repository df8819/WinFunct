import json
import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, font
import openai
import requests
import logging
from datetime import datetime

# Configure logging
# logging.basicConfig(filename='jchat.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class JChat:
    def __init__(self, parent):
        self.root = parent
        self.font_family = "Segoe UI Emoji"
        self.font_size = 12

        self.api_key = self.load_or_request_api_key()
        if not self.api_key:
            raise ValueError("API key is missing")
        os.environ["OPENAI_API_KEY"] = self.api_key
        openai.api_key = self.api_key

        self.loop_text = None
        self.loop_thread = None
        self.loop_active = False

        self.behaviors = self.initialize_behaviors()
        self.pre_prompt = self.behaviors["Default"]
        self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]

        self.setup_gui()

    def initialize_behaviors(self):
        return {
            "Default": "---Act as normal GPT-4 instance--- ",
            "(＾• ω •＾)": "---Act as cute eGirl and ALWAYS/ONLY use UwU-speech and lots of kaomojies/emojies: --- ",
            "Mad Scientist": "---Act as mean sarcastic Einstein and answer ALWAYS/ONLY with intrinsic lyrically spoken formulas: --- ",
            "SciFi Commander": "---Act as advanced AGI-Commander onboard of a space frigate and ALWAY/ONLY answer in short, brief and precise answers: --- ",
            "Schwiizer": "---Your task is to act as guide for Switzerland and ALWAYS/ONLY speak in swiss-german: --- ",
            "NYC Shakespeare": "---Act as Shakespeare from the 21st century who became a NYC rap battle expert: --- ",
            "Grow-Master": "---Act as professional gardener and assist the user in growing CBD-(legal!)-weed: --- ",
            "Alien": "---Act as confused Alien from G581c that wants to stay unnoticed and ALWAYS/ONLY answer with text in altered format: --- ",
            "Code-Guru": "---Act as senior Software engineer from a world leading dev-team who will assist the user in all coding related questions: --- ",
            "Medical Assistant": "---Act as calming and professional medical doctor with PhD who will assist the user with precise, detailed and brief answers to medical conditions--- ",
        }

    def setup_gui(self):
        self.root.title("JChat")
        self.center_window(self.root)
        self.root.resizable(height=False, width=False)

        frame = tk.Frame(self.root)
        frame.grid(sticky="nsew", padx=10, pady=10)

        self.conversation = scrolledtext.ScrolledText(frame, wrap='word', state='disabled')
        self.conversation.configure(font=(self.font_family, self.font_size), bg='#edfcf0')
        self.conversation.grid(sticky="nsew")

        self.text_input = tk.StringVar()
        entry_field = tk.Entry(self.root, textvariable=self.text_input, font=(self.font_family, self.font_size))
        entry_field.bind('<Return>', self.send_message)
        entry_field.grid(sticky="we", padx=10)
        entry_field.focus_set()

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(sticky="we", padx=10, pady=5)

        self.add_buttons(btn_frame)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

    def add_buttons(self, btn_frame):
        buttons = [
            ("Send", self.send_message),
            ("Clear", self.clear_conversation),
            ("Behavior", self.change_behavior),
            ("Loop", self.loop),
            ("Cancel Loop", self.cancel_loop),
            ("API Key", self.set_api_key),
            ("Exit", self.exit_app),
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(btn_frame, text=text, command=command, font=(self.font_family, self.font_size))
            button.grid(row=0, column=i, padx=10, pady=10, sticky="we")
            logging.info(f'Button {text} added to GUI.')

        # Add model selection dropdown
        self.selected_model = tk.StringVar(value="gpt-3.5-turbo")
        models = ["gpt-4o", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        model_menu = tk.OptionMenu(btn_frame, self.selected_model, *models)
        model_menu.configure(font=(self.font_family, self.font_size))
        model_menu.grid(row=0, column=len(buttons), padx=10, pady=10, sticky="we")
        btn_frame.grid_columnconfigure(len(buttons), weight=1)
        logging.info("Model selection dropdown added to GUI.")

        # Configure column weights to spread buttons evenly
        for i in range(len(buttons) + 1):
            btn_frame.grid_columnconfigure(i, weight=1)

    def center_window(self, window, width=760, height=620):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 3) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def load_or_request_api_key(self, filename: str = "apikey.json"):
        """Load API key from file or create a placeholder file and prompt the user to enter the API key."""

        def prompt_for_api_key():
            api_key_window = tk.Toplevel(self.root)
            api_key_window.title("API Key")

            label = tk.Label(api_key_window, text="Enter OpenAI API Key: ", font=(self.font_family, self.font_size))
            label.pack(padx=10, pady=10)

            entry = tk.Entry(api_key_window, font=(self.font_family, self.font_size))
            entry.pack(padx=10, pady=5)

            def on_set_api_key():
                new_key = entry.get()
                if not new_key:
                    messagebox.showerror("Error", "API Key cannot be empty.")
                    logging.error("Attempted to set empty API key.")
                else:
                    self.api_key = new_key
                    os.environ["OPENAI_API_KEY"] = self.api_key
                    openai.api_key = self.api_key
                    try:
                        with open(filename, 'w') as file:
                            json.dump({'api_key': new_key}, file)
                        logging.info("API key saved to file.")
                    except IOError as e:
                        logging.error(f"Error saving API key to file: {e}")
                        messagebox.showerror("Error", f"Could not save API key to file: {e}")
                    api_key_window.destroy()

            set_api_key_button = tk.Button(api_key_window, text="Save API Key", command=on_set_api_key,
                                           font=(self.font_family, self.font_size))
            set_api_key_button.pack(padx=10, pady=10)
            self.center_window(api_key_window, 400, 150)
            api_key_window.wait_window()

        if not os.path.exists(filename):
            data_structure = {"api_key": "<your-api-key-here>"}
            try:
                with open(filename, 'w') as f:
                    json.dump(data_structure, f)
                logging.info("API key placeholder file created.")
            except IOError as e:
                logging.error(f"Error creating API key placeholder file: {e}")
                messagebox.showerror("Error", f"Could not create API key placeholder file: {e}")
            prompt_for_api_key()
            return self.api_key

        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                api_key = data.get('api_key')
                if not api_key or api_key == "<your-api-key-here>":
                    prompt_for_api_key()
                    return self.api_key
                else:
                    logging.info("API key loaded from file.")
                    return api_key
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error loading API key from file: {e}")
            messagebox.showerror("Error", f"Could not load API key from file: {e}")
            prompt_for_api_key()
            return self.api_key

    def set_api_key(self):
        """Function to set a new API key."""

        def on_set_api_key():
            """Handles the event when the 'Set API Key' button is clicked."""
            new_key = entry.get()
            if not new_key:
                messagebox.showerror("Error", "API Key cannot be empty.")
                logging.error("Attempted to set empty API key.")
            else:
                self.api_key = new_key
                os.environ["OPENAI_API_KEY"] = self.api_key
                openai.api_key = self.api_key
                filename = os.path.join(os.path.dirname(__file__), 'apikey.json')
                try:
                    with open(filename, 'w') as file:
                        json.dump({'api_key': new_key}, file)
                    logging.info(f"API key saved to file: {filename}")
                except IOError as e:
                    logging.error(f"Error saving API key to file: {e}")
                    messagebox.showerror("Error", f"Could not save API key to file: {e}")
                api_key_window.destroy()

        api_key_window = tk.Toplevel(self.root)
        api_key_window.title("API Key")

        label = tk.Label(api_key_window, text="Enter new API Key: ", font=(self.font_family, self.font_size))
        label.pack(padx=10, pady=10)

        entry = tk.Entry(api_key_window, font=(self.font_family, self.font_size))
        entry.pack(padx=10, pady=5)

        set_api_key_button = tk.Button(api_key_window, text="Set API Key", command=on_set_api_key,
                                       font=(self.font_family, self.font_size))
        set_api_key_button.pack(padx=10, pady=10)

        self.center_window(api_key_window, 400, 150)
        api_key_window.wait_window()

    def center_window2(self, window, width=400, height=150):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 3) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def get_gpt_response(self, user_prompt):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai.api_key}',
        }

        self.conversation_history.append({'role': 'user', 'content': user_prompt})

        selected_model = self.selected_model.get()

        data = {
            'model': selected_model,
            'messages': self.conversation_history,
            'temperature': 0.7,
            'top_p': 0.9,
            'presence_penalty': 0.6,
            'frequency_penalty': 0.3,
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,
                                     data=json.dumps(data))
            response.raise_for_status()
            if self.loop_active and self.loop_text:
                self.root.after(1000, self.loop_request)
            return response
        except requests.RequestException as e:
            logging.error(f"API request error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def loop(self):
        if not self.loop_active:
            self.loop_dialog()

    def loop_dialog(self):
        def on_loop():
            self.loop_active = True
            self.loop_text = entry.get()
            if not self.loop_text.strip():
                messagebox.showerror("Error", "Loop text cannot be empty.")
                logging.error("Attempted to start loop with empty text.")
                return
            loop_window.destroy()
            self.loop_request()

        loop_window = tk.Toplevel(self.root)
        loop_window.title("Loop")

        label = tk.Label(loop_window, text="Enter response text to loop:\n", font=(self.font_family, self.font_size))
        label.pack(padx=10, pady=10)

        bold_font = font.Font(label, label.cget("font"))
        bold_font.configure(weight="bold")

        warning_label = tk.Label(loop_window, text="WARNING:", font=bold_font, compound="left")
        warning_label.pack()

        rest_of_text = tk.Label(loop_window, text="This will auto-loop your prompt until stopped!",
                                font=(self.font_family, self.font_size))
        rest_of_text.pack()

        entry = tk.Entry(loop_window, font=(self.font_family, self.font_size), width=50)
        entry.pack(padx=10, pady=5)

        loop_button = tk.Button(loop_window, text="Loop", command=on_loop, font=(self.font_family, self.font_size))
        loop_button.pack(padx=10, pady=10)

        # Set the font for the labels and button
        label.configure(font=(self.font_family, self.font_size))
        entry.configure(font=(self.font_family, self.font_size))
        loop_button.configure(font=(self.font_family, self.font_size))

        # Set the geometry of the loop window
        self.center_window(loop_window, 450, 220)
        loop_window.resizable(False, False)

        loop_window.transient(self.root)
        loop_window.grab_set()
        self.root.wait_window(loop_window)

    def cancel_loop(self):
        self.loop_active = False
        self.loop_text = None
        logging.info("Looping has been canceled.")

    def loop_request(self):
        if self.loop_active and self.loop_text:
            try:
                self.send_message(auto=True)
                logging.info("Loop request sent with text: {}".format(self.loop_text))
            except Exception as e:
                logging.error("Error during loop request: {}".format(e))
                messagebox.showerror("Error", "An error occurred during the loop request.")

    def send_message(self, event=None, auto=False):
        user_message = self.loop_text if auto else self.text_input.get()

        if user_message.lower() == 'exit':
            if messagebox.askokcancel("Quit", "Do you really want to quit?"):
                self.root.destroy()
            return

        self.text_input.set('')
        self.conversation.config(state='normal')  # Enable editing
        self.conversation.insert(tk.END, "You: ", 'bold-text')
        self.conversation.insert(tk.END, user_message + '\n\n', 'red-text')
        self.conversation_history.append({'role': 'user', 'content': user_message})
        self.conversation.config(state='disabled')  # Disable editing

        # Configure text tags
        self.conversation.tag_configure('red-text', foreground='#b00707')
        self.conversation.tag_configure('blue-text', foreground='#0707b0')
        self.conversation.tag_configure('line', underline=True)
        self.conversation.tag_configure('bold-text', font=(self.font_family, self.font_size, 'bold'))

        def gpt_request():
            if user_message.lower() == 'what model???':
                model_info = f"I am currently using the {self.selected_model.get()} model."
                self.display_response("JChat: ", model_info, 'blue-text')
            else:
                response = self.get_gpt_response(user_message)
                if response and response.status_code == 200:
                    completion = response.json()['choices'][0]['message']['content']
                    self.display_response("JChat: ", completion, 'blue-text')
                    self.conversation_history.append({'role': 'assistant', 'content': completion})
                else:
                    error_message = response.text if response else "No response received."
                    logging.error(f"Error occurred during GPT request: {error_message}")
                    messagebox.showerror("Error", f"An error occurred: {error_message}")

        threading.Thread(target=gpt_request).start()

    def display_response(self, prefix, message, tag):
        self.conversation.config(state='normal')
        self.conversation.insert(tk.END, prefix, 'bold-text')
        self.conversation.insert(tk.END, message + '\n\n', tag)
        self.conversation.insert(tk.END, '_' * 80, 'line')  # Add a visual line break
        self.conversation.insert(tk.END, '\n\n')
        self.conversation.config(state='disabled')
        self.conversation.see(tk.END)

    def clear_conversation(self):
        confirmed = messagebox.askyesno("Clear Conversation", "Are you sure you want to clear the conversation?")
        if confirmed:
            self.conversation.config(state='normal')  # Enable editing
            self.conversation.delete('1.0', tk.END)
            self.conversation.config(state='disabled')  # Disable editing
            self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]  # Reset conversation history
            logging.info("Conversation cleared by user.")

    def exit_app(self):
        logging.info("Application exited by user.")
        self.root.destroy()

    def change_behavior(self):
        def select_behavior(behavior):
            self.pre_prompt = self.behaviors[behavior]
            self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]
            window.destroy()
            logging.info(f"Behavior changed to: {behavior}")

        window = tk.Toplevel(self.root)
        window.title("Select Behavior")

        buttons = [tk.Button(window, text=name, command=lambda name=name: select_behavior(name)) for name in
                   self.behaviors.keys()]

        rows = round(len(buttons) ** 0.5)
        cols = len(buttons) // rows + (len(buttons) % rows > 0)

        for i, button in enumerate(buttons):
            button.grid(row=i // cols, column=i % cols, padx=10, pady=10, sticky="we")
            button.configure(font=(self.font_family, self.font_size))

        window.update_idletasks()  # Ensure geometry calculations are done
        window_width = max(window.winfo_reqwidth(), 400)  # Minimum width
        window_height = max(window.winfo_reqheight(), 200)  # Minimum height

        self.center_window(window, window_width, window_height)
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()
        self.root.wait_window(window)
