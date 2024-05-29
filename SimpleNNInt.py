import numpy as np

import tkinter as tk
from tkinter import ttk, messagebox, font

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow.keras as keras


class GUI:
    def __init__(self, root):
        self.x_train = None
        self.root = root
        self.root.title("Number Classifier - 'Feed forward neural network' for educational purposes")
        self.center_window()  # Center the main window

        self.threshold_label = tk.Label(self.root, text="Reference Number - Threshold (between 0 and 1):")
        self.threshold_entry = tk.Entry(self.root)
        self.threshold_entry.insert(0, "0.5")

        self.number_label = tk.Label(self.root, text="Number to predict (between 0 and 1):")
        self.number_entry = tk.Entry(self.root)
        self.number_entry.insert(0, "0.537")

        self.layers_label = tk.Label(self.root, text="Layers:")
        self.layers_entry = tk.Entry(self.root)
        self.layers_entry.insert(0, "4")

        self.nodes_label = tk.Label(self.root, text="Nodes per Layer:")
        self.nodes_entry = tk.Entry(self.root)
        self.nodes_entry.insert(0, "6")

        self.random_count_label = tk.Label(self.root, text="Random number count for training:")
        self.random_count_entry = tk.Entry(self.root)
        self.random_count_entry.insert(0, "500")

        self.predict_button = tk.Button(self.root, text="Predict", command=self.predict, padx=5, pady=5)
        self.reset_button = tk.Button(self.root, text="Reset Graph", command=self.reset_graph, padx=5, pady=5)
        self.visualize_button = tk.Button(self.root, text="Visualize Brain", command=self.visualize_brain, padx=5, pady=5)
        self.training_data_button = tk.Button(self.root, text="Training Data", command=self.show_training_data_command, padx=5, pady=5)
        self.guide_button = tk.Button(self.root, text="Guide", command=self.show_guide, padx=5, pady=5)
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program, padx=5, pady=5)

        self.threshold_label.grid(row=0, column=0, padx=10, pady=10)
        self.threshold_entry.grid(row=0, column=1, padx=10, pady=10)

        self.number_label.grid(row=4, column=0, padx=10, pady=10)
        self.number_entry.grid(row=4, column=1, padx=10, pady=10)

        self.layers_label.grid(row=2, column=0, padx=10, pady=10)
        self.layers_entry.grid(row=2, column=1, padx=10, pady=10)

        self.nodes_label.grid(row=3, column=0, padx=10, pady=10)
        self.nodes_entry.grid(row=3, column=1, padx=10, pady=10)

        self.random_count_label.grid(row=1, column=0, padx=10, pady=10)
        self.random_count_entry.grid(row=1, column=1, padx=10, pady=10)

        self.predict_button.grid(row=5, column=0, padx=10, pady=10)
        self.reset_button.grid(row=5, column=1, padx=10, pady=10)
        self.visualize_button.grid(row=6, column=0, padx=10, pady=10)
        self.training_data_button.grid(row=6, column=1, padx=10, pady=10)
        self.guide_button.grid(row=14, column=0, padx=(10, 20), pady=10)
        self.exit_button.grid(row=14, column=1, padx=(10, 20), pady=10)

        self.progress_label = tk.Label(self.root, text="Training Progress:")
        self.progress_bar = ttk.Progressbar(self.root, mode="determinate", length=500)

        self.fig, self.ax = plt.subplots(2, 1, figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.progress_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.progress_bar.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.prediction_label = tk.Label(self.root, text="Prediction certainty for 'Number to predict':")
        self.prediction_entry = tk.Entry(self.root, state="readonly")

        self.prediction_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        self.prediction_entry.grid(row=10, column=1, columnspan=2, padx=10, pady=10)

        self.final_loss_label = tk.Label(self.root, text="Overall Loss:")
        self.final_loss_entry = tk.Entry(self.root, state="readonly")

        self.final_accuracy_label = tk.Label(self.root, text="Overall Accuracy:")
        self.final_accuracy_entry = tk.Entry(self.root, state="readonly")

        self.final_loss_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
        self.final_loss_entry.grid(row=11, column=1, columnspan=2, padx=10, pady=10)
        self.final_accuracy_label.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
        self.final_accuracy_entry.grid(row=12, column=1, columnspan=2, padx=10, pady=10)

        # Add the following lines in your __init__ method
        self.calculations_label = tk.Label(self.root, text="Total Calculations:")
        self.calculations_entry = tk.Entry(self.root, state="readonly")

        # Position the label and entry in the grid
        self.calculations_label.grid(row=13, column=0, columnspan=2, padx=10, pady=10)
        self.calculations_entry.grid(row=13, column=1, columnspan=2, padx=10, pady=10)

    def visualize_brain(self):
        # Display a messagebox and get the user's response
        response = tk.messagebox.askyesno("WARNING - High CPU demand",
                                          "WARNING:\n\nA big brain size (16 * 128 Neurons for example)"
                                          " can take VERY long to create the visualization. (And will"
                                          " probably lag harder than 'Redfall' on release) \n\nContinue?")

        # If the user clicked 'No', return without doing anything
        if not response:
            return

        plt.close('all')  # Close all existing figures

        # Get the number of layers and nodes per layer from the input fields
        layers = int(self.layers_entry.get()) + 1  # Add one more hidden layer
        nodes_per_layer = int(self.nodes_entry.get())

        # Create a new graph
        g = nx.DiGraph()

        # Add node for input layer
        g.add_node((0, 0), pos=(0, 0.5), color='g')

        # Add nodes and edges for each hidden layer
        for layer in range(1, layers + 1):
            if layer == layers:  # output layer
                g.add_node((layer, 0), pos=(layer, 0.5), color='b')
                for prev_node in range(nodes_per_layer):
                    g.add_edge((layer - 1, prev_node), (layer, 0))
            else:  # hidden layers
                for node in range(nodes_per_layer):
                    # Calculate the position of the node
                    pos = (layer, node / (nodes_per_layer - 1) if nodes_per_layer > 1 else 0.5)

                    # Add the node to the graph
                    g.add_node((layer, node), pos=pos, color='y')

                    # Connect the node to all nodes in the previous layer
                    for prev_node in range(nodes_per_layer if layer > 1 else 1):
                        g.add_edge((layer - 1, prev_node), (layer, node))

        # Get node positions and colors
        pos = nx.get_node_attributes(g, 'pos')
        colors = [color for _, color in nx.get_node_attributes(g, 'color').items()]

        # Create a new figure and draw the graph
        fig, ax = plt.subplots()
        nx.draw(g, pos, node_color=colors, with_labels=True, ax=ax)

        # Create a new window
        new_window = tk.Toplevel(self.root)
        new_window.title('Brain Visualization')

        # Create a new FigureCanvasTkAgg object in the new window
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()

        # Add the canvas to the window and allow it to expand and fill both directions
        canvas.get_tk_widget().pack(expand=True, fill='both')

        # Add Navigation Toolbar
        toolbar = NavigationToolbar2Tk(canvas, new_window)
        toolbar.update()

        # Center the new window
        new_window.update_idletasks()  # Update window size before centering
        width = 1600
        height = 900
        new_window.geometry('{}x{}'.format(width, height))  # Width x Height
        x = (new_window.winfo_screenwidth() // 2) - (width // 2)
        y = (new_window.winfo_screenheight() // 2) - (height // 2)
        new_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 620  # Adjust the window width here
        window_height = 1050  # Adjust the window height here
        self.root.resizable(False, False)
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def predict(self):

        threshold = float(self.threshold_entry.get())
        number = float(self.number_entry.get())
        layers_input = int(self.layers_entry.get())
        nodes_input = int(self.nodes_entry.get())
        random_count = int(self.random_count_entry.get())

        x_train = np.random.uniform(0, 1, size=(random_count, 1)).round(8)
        self.x_train = x_train
        y_train = (x_train >= threshold).astype(int)

        model = Sequential()
        layers_nodes = [nodes_input] * layers_input
        model.add(Dense(layers_nodes[0], input_dim=1, activation='relu'))
        for nodes in layers_nodes[1:]:
            model.add(Dense(nodes, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        progress_callback = self.ProgressCallback(self)
        history = model.fit(x_train, y_train, epochs=100, batch_size=10, verbose=0, callbacks=[progress_callback])

        prediction = model.predict(np.array([[number]]))
        prediction_value = "{:.3%}".format(prediction[0][0])
        self.prediction_entry.configure(state="normal")
        self.prediction_entry.delete(0, tk.END)
        self.prediction_entry.insert(0, prediction_value)
        self.prediction_entry.configure(state="readonly")

        self.final_loss_entry.configure(state="normal")
        self.final_loss_entry.delete(0, tk.END)
        loss_value = "{:.3%}".format(history.history['loss'][-1])
        self.final_loss_entry.insert(0, loss_value)
        self.final_loss_entry.configure(state="readonly")

        self.final_accuracy_entry.configure(state="normal")
        self.final_accuracy_entry.delete(0, tk.END)
        accuracy_value = "{:.3%}".format(history.history['accuracy'][-1])
        self.final_accuracy_entry.insert(0, accuracy_value)
        self.final_accuracy_entry.configure(state="readonly")

        self.ax[0].plot(history.history['loss'], label='Loss')
        self.ax[1].plot(history.history['accuracy'], label='Accuracy', color='green')
        self.ax[0].legend()
        self.ax[1].legend()

        # Change line color for each prediction
        lines = self.ax[1].get_lines()
        last_line = lines[-1]
        last_line.set_color(np.random.rand(3))

        self.fig.tight_layout()
        self.canvas.draw()

        # Calculate the total number of parameters
        total_parameters = 2 * nodes_input + layers_input * (nodes_input ** 2 + nodes_input) + nodes_input + 1

        # Calculate the total number of calculations per epoch
        calculations_per_epoch = 4 * total_parameters * (random_count / 10)

        # Calculate the total number of calculations over the entire training process
        total_calculations = 100 * calculations_per_epoch

        # Format the number with single quotes as thousands separators
        formatted_calculations = "{:,}".format(int(total_calculations)).replace(",", "'")

        self.calculations_entry.configure(state="normal")
        self.calculations_entry.delete(0, tk.END)
        self.calculations_entry.insert(0, formatted_calculations)
        self.calculations_entry.configure(state="readonly")

    def show_training_data(self, random_count):
        training_data_str = ", ".join(map(str, self.x_train.flatten()))

        # Create new Toplevel window
        new_window = tk.Toplevel(self.root)
        new_window.title("Training Data Set from 'Random number count'")

        # Position the window in the center of the screen
        window_width = 1200
        window_height = 900
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        new_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Create a Scrollbar
        scroll_bar = tk.Scrollbar(new_window)

        # Add text widget with training data
        text_widget = tk.Text(new_window, width=1000, height=800, yscrollcommand=scroll_bar.set)
        text_widget.insert(tk.END, training_data_str)

        # Configure the Scrollbar
        scroll_bar.config(command=text_widget.yview)

        # Add 'Copy' button with padding
        copy_button = tk.Button(new_window, text="Copy", command=lambda: self.copy_to_clipboard(training_data_str),
                                padx=5, pady=5)

        # Create label and read-only entry for total random numbers generated
        random_count_label = tk.Label(new_window, text="Random Numbers generated: ")
        random_count_entry = tk.Entry(new_window)
        random_count_entry.insert(0, str(random_count))
        random_count_entry.configure(state="readonly")

        # Use grid layout manager
        text_widget.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')
        scroll_bar.grid(row=0, column=3, sticky='ns')
        copy_button.grid(row=1, column=0, padx=20, pady=20, sticky='e')
        benford_button = tk.Button(new_window, text="Digit Distribution", command=self.benford_analysis, padx=5, pady=5)
        benford_button.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        random_count_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")
        random_count_entry.grid(row=2, column=1, padx=20, pady=20, sticky='w')

        # Configure grid column and row weights
        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_columnconfigure(1, weight=1)
        new_window.grid_columnconfigure(2, weight=1)
        new_window.grid_rowconfigure(0, weight=1)

        # Enable 'Ctrl+C' for copying from the text widget
        new_window.bind('<Control-c>', lambda e: self.copy_to_clipboard(text_widget.get("1.0", tk.END)))

    def show_training_data_command(self):
        random_count = int(self.random_count_entry.get())
        self.show_training_data(random_count)

    def benford_analysis(self):
        from matplotlib.figure import Figure

        # Extract the first digit after the decimal point from each number in the training set
        first_digits = [int(str(x)[2]) for x in self.x_train.flatten() if str(x)[2].isdigit()]

        # Compute the distribution of the first digits
        digit_counts = np.bincount(first_digits)[1:]  # Exclude the count for the digit 0
        digit_percentages = digit_counts / np.sum(digit_counts)

        # Create a new figure and display a bar graph of the digit distribution
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.bar(range(1, 10), digit_percentages, tick_label=range(1, 10))
        ax.set_xlabel('First Digit After Decimal Point')
        ax.set_ylabel('Percentage')
        ax.set_title("Distribution of First Digits After Decimal Point in Training Data")

        # Create new Toplevel window
        benford_window = tk.Toplevel(self.root)
        benford_window.title("Experimental feature")

        # Position the window in the center of the screen
        window_width = 800
        window_height = 600
        screen_width = benford_window.winfo_screenwidth()
        screen_height = benford_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        benford_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Create a new FigureCanvasTkAgg object in the new window
        canvas = FigureCanvasTkAgg(fig, master=benford_window)
        canvas.draw()

        # Add the canvas to the window and allow it to expand and fill both directions
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def reset_graph(self):
        self.ax[0].clear()
        self.ax[1].clear()
        self.canvas.draw()

        # Clear the prediction certainty field
        self.prediction_entry.configure(state='normal')
        self.prediction_entry.delete(0, tk.END)
        self.prediction_entry.configure(state='readonly')

        # Clear the overall loss field
        self.final_loss_entry.configure(state='normal')
        self.final_loss_entry.delete(0, tk.END)
        self.final_loss_entry.configure(state='readonly')

        # Clear the overall accuracy field
        self.final_accuracy_entry.configure(state='normal')
        self.final_accuracy_entry.delete(0, tk.END)
        self.final_accuracy_entry.configure(state='readonly')

        # Clear the Calculations field
        self.calculations_entry.configure(state='normal')
        self.calculations_entry.delete(0, tk.END)
        self.calculations_entry.configure(state='readonly')

    def exit_program(self):
        self.root.destroy()

    def show_guide(self):
        guide = """
        Number Classifier - 'Feed forward neural network' - User Guide

        1. Reference Number - Threshold (between 0 and 1):
           - Enter a decimal number between 0 and 1.
           - This number serves as a reference for the classification.

        2. Number to predict if >= 'Reference number' (between 0 and 1):
           - Enter a decimal number between 0 and 1.
           - This number will be classified as higher or lower than the reference number.
           - The neural network will be trained to predict if this number is >= 'Reference Number'.

        3. Layers:
           - Enter the number of layers.
           - {layers} * {nodes} = Neurons.

        4. Nodes:
            - Enter the numbers of nodes in each layer.
            - {layers} * {nodes} = Neurons.

        5. Random number count for training:
           - Enter the count of random numbers to generate for training the model.

        6. Predict Button:
           - Click this button to perform the prediction based on the provided inputs.

        7. Reset Graph Button:
           - Click this button to clear the training progress graph.

        8. Visualize Brain Button:
            - Opens a window for a visual representation of the current model.

        9. Training Data Button:
            - Opens a window to show the random numbers used for the training.       

        Note:
        - This app is for educational purposes and people who
            want to have a small insight in the world of neural networks.
        - The prediction value closer to 1 indicates a higher prediction,
            while closer to 0 indicates a lower prediction.
        - This model is set to 100 epochs and a batch size of 10.     
        """

        guide_window = tk.Toplevel(self.root)
        guide_window.title("User Guide")
        guide_window.geometry("+{}+{}".format(self.root.winfo_x() + 50, self.root.winfo_y() + 50))
        guide_window.resizable(False, False)
        font_style = font.Font(family="Arial", size=10)  # Adjust the font size here

        text = tk.Text(guide_window, font=font_style, width=80, height=42)  # Adjust the height to your desired value
        text.insert(tk.END, guide)
        text.pack()

    class ProgressCallback(keras.callbacks.Callback):
        def __init__(self, gui_instance):
            super().__init__()
            self.gui_instance = gui_instance
            self.progress = 0

        def on_epoch_end(self, epoch, logs=None):
            self.progress += 1
            self.gui_instance.progress_bar["value"] = self.progress
            self.gui_instance.progress_bar.update()

        def set_model(self, model):
            pass


def run_simple_nn():
    nn_window = tk.Toplevel()
    GUI(nn_window)
