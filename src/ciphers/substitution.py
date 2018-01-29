import random
import tkinter as tk
from string import ascii_uppercase

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import LinearLocator, PercentFormatter

from cipher_window import CipherWindow
from utilities import SUBTITLE_LABEL_OPTIONS
from widgets.tooltip import Tooltip

NEEDED_MAPPING_COLOR = "yellow"
DUPLICATE_MAPPING_COLOR = "red"


def substitution(text, mapping):
    """Performs Substitution cipher on the input text. mapping should be a dictionary containing input_letter:output_letter"""
    text = text.upper()
    for k, v in mapping.items():
        text = text.replace(k.upper(), v.lower())
    return text


def valid_mapping_entry(text):
    """Returns if the text is valid inside a mapping entry box"""
    if len(text) > 1:
        # Cannot be more than 1 long
        return False
    if len(text) == 0:
        # Allow empty (no mapping)
        return True
    # Otherwise check if it is a letter
    chr_code = ord(text)
    return 65 <= chr_code <= 90 or 97 <= chr_code <= 122


class SubstitutionCipher(CipherWindow):
    """Cipher Window for the Substitution Cipher Encryption and Decryption"""

    def __init__(self, application):
        self.stringvars = {}
        self.entries = {}
        self.tooltips = []
        self.default_colours = {}

        self.freq_subplot = None
        self.freq_bars = None
        self.freq_canvas = None

        super(SubstitutionCipher, self).__init__(application, "Substitution Cipher")

    def get_key(self):
        """Returns the mapping and shows which entries need to be filled in,
        or have the identical mappings"""

        # destroy any previous tooltips
        for tooltip in self.tooltips:
            tooltip.remove()
        self.tooltips.clear()
        # set all the entries back to default foreground and background colours
        for letter in ascii_uppercase:
            self.entries[letter].configure(**self.default_colours)

        # iterate over every letter and store mappings
        mapping = {}
        reverse_mapping_lists = {letter:[] for letter in ascii_uppercase}
        input_text = self.get_input_text().upper()
        for letter in ascii_uppercase:
            string = self.stringvars[letter].get().upper()
            if string:
                # if a letter mapping has been entered, store it in the map
                mapping[letter] = string
                # used to detect duplicates
                reverse_mapping_lists[string].append(self.entries[letter])
            elif letter in input_text:
                # mapping is needed, but is not present
                entry = self.entries[letter]
                entry.configure(background=NEEDED_MAPPING_COLOR)
                tooltip = Tooltip(entry, text="Mapping needed as letter present in input")
                # store tooltip so it can be removed later
                self.tooltips.append(tooltip)

        # mark duplicates
        for letter in ascii_uppercase:
            reverse_mappings = reverse_mapping_lists[letter]
            if len(reverse_mappings) > 1:
                # more than one reverse mapping, mark the duplicate mappings
                for entry in reverse_mappings:
                    entry.configure(background=DUPLICATE_MAPPING_COLOR, foreground="white")
                    tooltip = Tooltip(entry, text="Mapping is not unique!")
                    # store tooltip so it can be removed later
                    self.tooltips.append(tooltip)

        # update the bar chart
        self.update_bar_chart(input_text, mapping)

        return mapping

    def run_cipher(self, text, key):
        """Run the Substitution cipher"""
        return substitution(text, key)

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        tk.Label(frame, text="Mapping", **SUBTITLE_LABEL_OPTIONS).grid(row=0, column=0, columnspan=26)

        # setup label and entry for each letter
        for i, letter in enumerate(ascii_uppercase):
            # setup label for letter
            tk.Label(frame, text=letter).grid(row=1, column=i)
            # setup stringvar for storing mapping
            self.stringvars[letter] = tk.StringVar(self)
            # setup entry for letter mapping
            self.entries[letter] = tk.Entry(frame, validate="key", validatecommand=(frame.register(valid_mapping_entry), "%P"), textvariable=self.stringvars[letter], width=2)
            self.entries[letter].grid(row=2, column=i)
        # setup stringvar callbacks
        self.setup_stringvar_callbacks()

        # store the default colour options
        self.default_colours["foreground"] = self.entries["A"].cget("foreground")
        self.default_colours["background"] = self.entries["A"].cget("background")

        return frame

    def setup_stringvar_callbacks(self):
        """Setup the callbacks so when the mapping is changed the output updates"""
        for stringvar in self.stringvars.values():
            trace_id = stringvar.trace("w", lambda *args: self.update_output())
            stringvar.trace_id = trace_id

    def remove_stringvar_callbacks(self):
        """Remove the callbacks for faster processing of mapping changes"""
        for stringvar in self.stringvars.values():
            stringvar.trace_vdelete("w", stringvar.trace_id)

    def create_widgets(self):
        """Override CipherWindow to add letter frequency bar chart"""
        super(SubstitutionCipher, self).create_widgets()
        self.setup_bar_chart()
        self.setup_option_buttons()

    def setup_option_buttons(self):
        """Additional useful buttons under the Cipher Window back button"""
        frame = tk.Frame(self)
        tk.Button(frame, text="Random Key", command=self.random_key).grid(row=0, column=0)
        tk.Button(frame, text="Swap In/Out", command=self.swap).grid(row=0, column=1)
        # move solve button into option buttons as it is covered by the bar chart
        self.solve_button.destroy()
        self.solve_button = tk.Button(frame, text="Solve", command=self.show_solver, state="disabled")
        self.solve_button.grid(row=0, column=2)
        # under back button
        frame.grid(row=1, column=1)

    def setup_bar_chart(self):
        """Setup the letter frequency bar chart"""
        # make a new matplotlib figure
        figure = Figure(figsize=(2, 4))
        self.freq_subplot = figure.add_subplot(1, 1, 1)
        # graph title
        self.freq_subplot.set_title("Frequency Analysis")
        # setup bar chart with all zero frequencies for all 26 letters
        y_pos = list(range(26))
        frequencies = [0] * len(ascii_uppercase)
        self.freq_bars = self.freq_subplot.barh(y_pos, frequencies, height=0.8)
        # set axis limits
        self.freq_subplot.set_autoscale_on(False)
        self.freq_subplot.set_xlim(0, 100)
        self.freq_subplot.set_ylim(-0.5, 25.5)
        # set positions, contents of labels and y limits
        self.freq_subplot.set_yticks(y_pos)
        self.freq_subplot.set_yticklabels(ascii_uppercase)
        self.freq_subplot.invert_yaxis()
        # set x axis to show % and to show 3 values
        self.freq_subplot.xaxis.set_major_formatter(PercentFormatter())
        self.freq_subplot.xaxis.set_major_locator(LinearLocator(numticks=3))

        def size_callback(event):
            # remove the callback
            self.text_input.unbind("<Configure>", bind_id)
            # on my normal resolution monitor, the text input is 5.5 inches wide.
            # native tkinter widgets scale correctly on high resolution screens.
            # therefore the size of the text_input can be used to calculate
            # an approximation of the screen dpi.
            dpi = self.text_input.winfo_width() / 5.5
            figure.set_dpi(dpi)
            # now that dpi is set, setup canvas to embed inside tkinter window
            self.freq_canvas = FigureCanvasTkAgg(figure, master=self)
            self.freq_canvas.show()
            self.freq_canvas.get_tk_widget().grid(column=1, row=2, rowspan=5, sticky="NSEW")
            # remove some of the extra padding around the graph
            figure.tight_layout(pad=0.2)
        # wait for text_input size to be set, as it's size is used for
        # the dpi calculation
        bind_id = self.text_input.bind("<Configure>", size_callback)

    def update_bar_chart(self, text, mapping):
        """Update the letter frequencies bar chart. text must be uppercase"""
        # find letter frequencies
        frequencies = {letter: 0 for letter in ascii_uppercase}
        total_frequency = 0
        for letter in text:
            if 65 <= ord(letter) <= 90:
                frequencies[letter] += 1
                total_frequency += 1
        # calculate percentages and set max x on graph
        if total_frequency > 0:
            for letter in frequencies:
                frequencies[letter] /= total_frequency
                frequencies[letter] *= 100
            self.freq_subplot.set_xlim(0, max(frequencies.values()))
        else:
            # no data, just set axis limit to 100%
            self.freq_subplot.set_xlim(0, 100)
        # iterate over bars, updating size & colour
        for letter, bar in zip(ascii_uppercase, self.freq_bars):
            bar.set_width(frequencies[letter])

            if letter in mapping:
                # make the bar green if a mapping exists
                bar.set_color("green")
            else:
                bar.set_color("blue")
        # redraw the graph
        self.freq_canvas.show()

    def random_key(self):
        """Creates a random key"""
        # remove the mapping entry widgets callbacks so the output does
        # not get updated every time one of the entries is changed
        self.remove_stringvar_callbacks()

        letters = list(ascii_uppercase)
        random.shuffle(letters)
        input_text = self.get_input_text().upper()
        for letter in ascii_uppercase:
            if letter in input_text:
                self.stringvars[letter].set(letters.pop())
            else:
                self.stringvars[letter].set("")

        # setup the mapping entry widgets callbacks again so the output
        # updates if the mapping is changed
        self.setup_stringvar_callbacks()
        self.update_output()

    def swap(self):
        """Swaps the input text with the output text and reverses the mapping"""
        # remove the mapping entry widgets callbacks so the output does
        # not get updated every time one of the entries is changed
        self.remove_stringvar_callbacks()

        # store the old output text
        text_out = self.output_text.get(1.0, tk.END)
        self.text_input.delete(1.0, tk.END)
        # reverse the mapping
        mapping = self.get_key()
        reverse_mapping = {b: a for a, b in mapping.items()}
        for letter in ascii_uppercase:
            self.stringvars[letter].set(reverse_mapping.get(letter, ""))
        # set the input text to be the old mapping text
        self.text_input.insert(1.0, text_out)

        # setup the mapping entry widgets callbacks again so the output
        # updates if the mapping is changed
        self.setup_stringvar_callbacks()
        self.update_output()

    def get_solver(self):
        # Has to be imported here so the solver file can import the entire cipher file
        from solvers.substitution import SubstitutionSolver
        return SubstitutionSolver()
