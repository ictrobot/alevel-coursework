import tkinter as tk

from ciphers.cipher import Cipher
from widgets.numentry import NumEntry


def caesar(text, shift):
    """This function preforms a caesar shift on the input text and returns the output. Any characters which are not letters are left unchanged."""
    output = ""
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            # upper case letters
            offset = 65
        elif 97 <= chr_code <= 122:
            # lower case letters
            offset = 97
        else:
            # leave other characters untouched
            output += letter
            continue
        index = chr_code - offset
        index += shift
        chr_code = offset + (index % 26)
        output += chr(chr_code)
    return output


class CaesarCipher(Cipher):
    """Base Cipher implementation for the Caesar Cipher"""

    def __init__(self, mode):
        super(CaesarCipher, self).__init__("Caesar Cipher - " + mode)
        self.numentry_shift = None

    def run(self, text):
        """Run the cipher"""
        shift = self.numentry_shift.get_num()
        # if the number entry is empty, return a blank string
        if shift is None:
            return ""
        return self.shift(text, shift)

    def shift(self, text, shift):
        """Actually perform the caesar cipher, overridden in subclasses"""
        raise NotImplementedError()

    def tk_options_frame(self, cipher_window):
        """Get the key input"""
        frame = tk.Frame(cipher_window)
        self.numentry_shift = NumEntry(frame, label="Shift: ", min=0, max=26, default=1, callback=cipher_window.update_output)
        self.numentry_shift.grid(row=0, column=0)
        return frame


class CaesarEncrypt(CaesarCipher):
    """Caesar Encryption Cipher implementation"""

    def __init__(self):
        super(CaesarEncrypt, self).__init__("Encrypt")

    def shift(self, text, shift):
        return caesar(text, shift)


class CaesarDecrypt(CaesarCipher):
    """Caesar Decryption Cipher implementation"""

    def __init__(self):
        super(CaesarDecrypt, self).__init__("Decrypt")

    def shift(self, text, shift):
        # negative shift is the same as decryption
        return caesar(text, -shift)
