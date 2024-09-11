import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
import openai
import requests
import threading
import logging


class JChat:
    def __init__(self, parent, ui_color, button_bg_color, button_text_color):
        self.root = parent
        self.UI_COLOR = ui_color
        self.BUTTON_BG_COLOR = button_bg_color
        self.BUTTON_TEXT_COLOR = button_text_color
        self.font_family = "Segoe UI Emoji"

        self.api_key = self.load_or_request_api_key()
        if not self.api_key:
            raise ValueError("API key is missing")
        os.environ["OPENAI_API_KEY"] = self.api_key
        openai.api_key = self.api_key

        self.behaviors = self.initialize_behaviors()
        self.pre_prompt = self.behaviors["Default"]
        self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]

        self.behavior_var = tk.StringVar(value="Default")
        self.behavior_var.trace('w', self.change_behavior)

        self.setup_gui()

    def change_behavior(self, *args):
        behavior = self.behavior_var.get()
        self.pre_prompt = self.behaviors[behavior]
        self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]
        logging.info(f"Behavior changed to: {behavior}")

    def initialize_behaviors(self):
        return {
            "Default": "---Act as normal GPT instance--- ",
            "(^• ω •^)": "---Act as cute eGirl and ALWAYS/ONLY use UwU-speech and lots of kaomojies/emojies: --- ",
            "Mad Scientist": "---Act as mean sarcastic Einstein and answer ALWAYS/ONLY with intrinsic lyrically spoken formulas: --- ",
            "SciFi Commander": "---Act as advanced AGI-Commander onboard of a space frigate and ALWAY/ONLY answer in short, brief and precise answers: --- ",
            "Schwiizer": "---Your task is to act as guide for Switzerland and ALWAYS/ONLY speak in swiss-german: --- ",
            "NYC Shakespeare": "---Act as Shakespeare from the 21st century who became a NYC rap battle expert: --- ",
            "Grow-Master": "---Act as professional gardener and assist the user in growing CBD-(legal!)-weed: --- ",
            "Alien": "---Act as confused Alien from G581c that wants to stay unnoticed and ALWAYS/ONLY answer characters in altered format and lots of weird symbols: --- ",
            "Code-Guru": "---Act as senior Software engineer from a world leading dev-team who will assist the user in all coding related questions: --- ",
            "Medical Assistant": "---Act as calming and professional medical doctor with PhD who will assist the user with precise, detailed and brief answers to medical conditions: --- ",
            "Sassy Grandma": "---Act as a sassy, sarcastic grandma who speaks her mind and isn't afraid to roast the user. Use old-timey slang and lots of emojis: --- ",
            "Surfer Dude": "---Act as a laid-back surfer bro who's always stoked and uses lots of surfer lingo. Answer questions with a chill, positive vibe: --- ",
            "Pirate Captain": "---Ahoy matey! Act as a swashbucklin' pirate captain who speaks in a thick pirate accent. Use lots o' nautical terms and pirate lingo, savvy?: --- ",
            "Conspiracy Theorist": "---Act as a paranoid conspiracy theorist who sees hidden agendas and secret societies everywhere. Use lots of ALL CAPS and !!!: --- ",
            "Emoji Translator": "---Act as an AI that can only communicate using emojis. Translate the user's messages into emoji responses and vice versa: --- ",
            "Snarky Robot": "---Act as a sarcastic, wise-cracking robot who's unimpressed with humans. Use deadpan humor and lots of beep boop noises: --- ",
            "Motivational Coach": "---Act as an overly enthusiastic motivational coach who's always pumped up. Use lots of exclamation points and motivational quotes!!!: --- ",
            "Poetic Philosopher": "---Act as a deep, introspective philosopher who speaks in poetic riddles and metaphors. Ponder life's big questions with flowery language: --- ",
            "Gossipy Teenager": "---Act as a gossipy teenage girl who's always up on the latest drama. Use lots of slang, abbreviations, and emoji: --- ",
            "Grumpy Cat": "---Act as the infamous Grumpy Cat, responding to everything with sarcastic, pessimistic remarks. Use lots of cat puns and emoji: --- "
        }

    def setup_gui(self):
        self.root.title("JChat")
        self.root.configure(bg=self.UI_COLOR)
        self.root.geometry("800x600")
        self.center_window(self.root)
        self.root.resizable(height=True, width=True)

        frame = tk.Frame(self.root, bg=self.UI_COLOR)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.conversation = scrolledtext.ScrolledText(frame, wrap='word', state='disabled', bg=self.UI_COLOR,
                                                      fg=self.BUTTON_TEXT_COLOR,
                                                      insertbackground=self.BUTTON_TEXT_COLOR)
        self.conversation.configure(font=(self.font_family,))
        self.conversation.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.text_input = tk.StringVar()
        self.user_input = tk.Entry(frame, bg=self.UI_COLOR, fg=self.BUTTON_TEXT_COLOR,
                                   insertbackground=self.BUTTON_TEXT_COLOR, textvariable=self.text_input)
        self.user_input.grid(row=1, column=0, sticky="ew", pady=10)
        self.user_input.bind("<Return>", self.send_message)

        button_style = {"bg": self.BUTTON_BG_COLOR, "fg": self.BUTTON_TEXT_COLOR, "activebackground": self.UI_COLOR,
                        "activeforeground": self.BUTTON_TEXT_COLOR}
        self.send_button = tk.Button(frame, text="Send", command=self.send_message, **button_style)
        self.send_button.grid(row=1, column=1, sticky="e", pady=10)

        # Create a new frame for the buttons and dropdown menus
        button_frame = tk.Frame(frame, bg=self.UI_COLOR)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.behavior_label = tk.Label(button_frame, text="Behavior:", bg=self.UI_COLOR, fg=self.BUTTON_TEXT_COLOR)
        self.behavior_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.behavior_var = tk.StringVar(value="Default")
        self.behavior_menu = tk.OptionMenu(button_frame, self.behavior_var, *self.behaviors.keys(),
                                           command=self.change_behavior)
        self.behavior_menu.config(bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.UI_COLOR,
                                  activeforeground=self.BUTTON_TEXT_COLOR)
        self.behavior_menu["menu"].config(bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR)
        self.behavior_menu.grid(row=0, column=1, sticky="w")

        self.clear_button = tk.Button(button_frame, text="Clear Chat", command=self.clear_conversation, **button_style)
        self.clear_button.grid(row=0, column=2, sticky="w", padx=(10, 0))

        self.selected_model = tk.StringVar(value="gpt-3.5-turbo")
        models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        model_menu = tk.OptionMenu(button_frame, self.selected_model, *models)
        model_menu.config(bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.UI_COLOR,
                          activeforeground=self.BUTTON_TEXT_COLOR)
        model_menu.grid(row=0, column=3, sticky="w", padx=(10, 0))

        self.model_info_button = tk.Button(button_frame, text="What model???", command=self.display_model_info,
                                           **button_style)
        self.model_info_button.grid(row=0, column=4, sticky="w", padx=(10, 0))

        self.api_button = tk.Button(button_frame, text="Set API Key", command=self.set_api_key, **button_style)
        self.api_button.grid(row=0, column=5, sticky="w", padx=(10, 0))

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, **button_style)
        self.exit_button.grid(row=0, column=6, sticky="w", padx=(10, 0))

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def center_window(self, window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f'+{x}+{y}')

    def display_model_info(self):
        model_info = f"I am currently using the {self.selected_model.get()} model."
        self.display_response("JChat: ", model_info, 'assistant-text')

    def load_or_request_api_key(self, filename: str = "apikey.json"):
        """Load API key from file or create a placeholder file and prompt the user to enter the API key."""

        def prompt_for_api_key():
            api_key_window = tk.Toplevel(self.root)
            api_key_window.title("API Key")
            api_key_window.configure(bg=self.UI_COLOR)

            label = tk.Label(api_key_window, text="Enter OpenAI API Key: ", font=(self.font_family,), bg=self.UI_COLOR, fg=self.BUTTON_TEXT_COLOR)
            label.pack(padx=10, pady=10)

            entry = tk.Entry(api_key_window, font=(self.font_family, 12), bg=self.UI_COLOR, fg=self.BUTTON_TEXT_COLOR, insertbackground=self.BUTTON_TEXT_COLOR, width=80)
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

            set_api_key_button = tk.Button(api_key_window, text="Save API Key", command=on_set_api_key, font=(self.font_family, 12), bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.UI_COLOR, activeforeground=self.BUTTON_TEXT_COLOR)
            set_api_key_button.pack(padx=10, pady=10)

            self.center_window(api_key_window)
            api_key_window.wait_window()

        if not os.path.exists(filename):
            data_structure = {"api_key": ""}
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
                if not api_key or api_key == "":
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
        api_key_window.configure(bg=self.UI_COLOR)

        label = tk.Label(api_key_window, text="Enter new API Key: ", font=(self.font_family, 12), bg=self.UI_COLOR, fg=self.BUTTON_TEXT_COLOR)
        label.pack(padx=10, pady=10)

        entry = tk.Entry(api_key_window, font=(self.font_family, 12), bg=self.UI_COLOR, fg=self.BUTTON_TEXT_COLOR, insertbackground=self.BUTTON_TEXT_COLOR, width=80)
        entry.pack(padx=10, pady=5)

        set_api_key_button = tk.Button(api_key_window, text="Set API Key", command=on_set_api_key, font=(self.font_family, 12), bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.UI_COLOR, activeforeground=self.BUTTON_TEXT_COLOR)
        set_api_key_button.pack(padx=10, pady=10)

        api_key_window.geometry("600x200")  # Set the window size to 600x200
        api_key_window.resizable(False, False)  # Disable window resizing
        self.center_window(api_key_window)
        api_key_window.wait_window()

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
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"API request error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def send_message(self, event=None):
        user_message = self.text_input.get()
        if user_message.lower() == 'exit':
            if messagebox.askokcancel("Quit", "Do you really want to quit?"):
                self.root.destroy()
            return
        self.text_input.set('')
        self.conversation.config(state='normal')  # Enable editing
        self.conversation.insert(tk.END, "You: ", 'bold-text')
        self.conversation.insert(tk.END, user_message + '\n\n', 'user-text')
        self.conversation_history.append({'role': 'user', 'content': user_message})
        self.conversation.config(state='disabled')  # Disable editing
        # Configure text tags
        self.conversation.tag_configure('user-text', foreground=self.BUTTON_TEXT_COLOR)
        self.conversation.tag_configure('assistant-text', foreground=self.BUTTON_TEXT_COLOR)

        self.conversation.tag_configure('line', underline=True)
        self.conversation.tag_configure('bold-text', font=(self.font_family, 12, 'bold'))

        def gpt_request():
            if user_message.lower() == 'what model???':
                model_info = f"I am currently using the {self.selected_model.get()} model."
                self.display_response("JChat: ", model_info,'assistant-text')
            else:
                response = self.get_gpt_response(user_message)
                if response and response.status_code == 200:
                    completion = response.json()['choices'][0]['message']['content']
                    self.display_response("JChat: ", completion, 'assistant-text')
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

# WINDOW FOR BEHAVIOUR STILL OPENS EVEN WITH THE IMPLEMENTATION OF THE DROPDOWN. PLEASE DELETE THE WINDOW AND MAKE THE SELECTION INSTANT UPON SELECTING WITH THE DROPDOWN PLEASE.