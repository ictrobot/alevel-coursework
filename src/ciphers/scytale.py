import tkinter as tk

from ciphers.cipher import Cipher
from widgets.numentry import NumEntry


def scytale(text, columns):
    """ Preforms scytale on the input text as if there were the specified amount of columns"""
    # add padding
    while len(text) % columns != 0:
        text += "_"
    # do scytale
    output = ""
    for i in range(columns):
        output = output + text[i::columns]
    return output


def reverse_scytale(text, columns):
    """ Reverse the scytale function"""
    return scytale(text, len(text) // columns).replace("_", "")


class ScytaleCipher(Cipher):
    """Base Cipher implementation for the Scytale Cipher"""

    def __init__(self, mode):
        super(ScytaleCipher, self).__init__("Scytale - " + mode)
        self.numentry_columns = None

    def run(self, text):
        """Run the cipher"""
        # update the maximum number of columns
        self.numentry_columns.set_max(len(text))
        # get the current number of columns
        columns = self.numentry_columns.get_num()
        # if the number entry is empty, return a blank string
        if columns is None:
            return ""
        return self.shift(text, columns)

    def shift(self, text, columns):
        """Actually perform the scytale cipher, overridden in subclasses"""
        raise NotImplementedError()

    def tk_options_frame(self, cipher_window):
        """Get the key input"""
        frame = tk.Frame(cipher_window)
        self.numentry_columns = NumEntry(frame, label="Columns: ", min=1, default=1, callback=cipher_window.update_output)
        self.numentry_columns.grid(row=0, column=0)
        return frame


class ScytaleEncrypt(ScytaleCipher):
    """Scytale Encryption Cipher implementation"""

    def __init__(self):
        super(ScytaleEncrypt, self).__init__("Encrypt")

    def shift(self, text, columns):
        return scytale(text, columns)


class ScytaleDecrypt(ScytaleCipher):
    """Scytale Decryption Cipher implementation"""

    def __init__(self):
        super(ScytaleDecrypt, self).__init__("Decrypt")

    def shift(self, text, columns):
        return reverse_scytale(text, columns)
