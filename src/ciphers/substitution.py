import tkinter as tk
from cipher_window import CipherWindow
from string import ascii_uppercase
from utilities import SUBTITLE_LABEL_OPTIONS


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

        super(SubstitutionCipher, self).__init__(application, "Substitution Cipher")

    def get_key(self):
        """Returns the mapping"""
        # iterate over every letter and store mappings
        mapping = {}
        for letter in ascii_uppercase:
            string = self.stringvars[letter].get().upper()
            if string:
                # if a letter mapping has been entered, store it in the map
                mapping[letter] = string
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
