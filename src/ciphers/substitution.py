import tkinter as tk
from cipher_window import CipherWindow
from string import ascii_uppercase
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
            self.entries[letter].configure(background="SystemWindow", foreground="SystemWindowText")

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
            self.stringvars[letter].trace("w", lambda *args: self.update_output())
            # setup entry for letter mapping
            self.entries[letter] = tk.Entry(frame, validate="key", validatecommand=(frame.register(valid_mapping_entry), "%P"), textvariable=self.stringvars[letter], width=2)
            self.entries[letter].grid(row=2, column=i)

        return frame
