import tkinter as tk

from cipher_window import CipherWindow
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


class ScytaleCipher(CipherWindow):
    """Base Cipher Window for the Scytale Cipher"""

    def __init__(self,  application, mode):
        super(ScytaleCipher, self).__init__( application, "Scytale - " + mode)
        self.numentry_columns = None

    def get_key(self):
        """Returns the key or None if it is invalid"""
        # update the maximum number of columns
        self.numentry_columns.set_max(max(1, len(self.get_input_text())))
        # return the number of columns or none if the input is empty
        return self.numentry_columns.get_num()

    def run_cipher(self, text, key):
        """Subclasses actually run the scytale cipher"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        self.numentry_columns = NumEntry(frame, label="Columns: ", min=1, default=1, callback=self.update_output)
        self.numentry_columns.grid(row=0, column=0)
        return frame


class ScytaleEncrypt(ScytaleCipher):
    """Scytale Encryption Cipher Window"""

    def __init__(self,  application):
        super(ScytaleEncrypt, self).__init__( application,"Encrypt")

    def run_cipher(self, text, columns):
        return scytale(text, columns)


class ScytaleDecrypt(ScytaleCipher):
    """Scytale Decryption Cipher Window"""

    def __init__(self,  application):
        super(ScytaleDecrypt, self).__init__( application,"Decrypt")

    def run_cipher(self, text, columns):
        return reverse_scytale(text, columns)
