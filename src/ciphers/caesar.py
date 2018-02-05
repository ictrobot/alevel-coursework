import tkinter as tk

from cipher_window import CipherWindow
from widgets.numentry import NumEntry

from string import ascii_letters


def _caesar_chr(chr_code, shift):
    """This function preforms a caesar shift on a single letter as a character code. Used to pre-calculate the translations"""
    if 65 <= chr_code <= 90:
        # upper case letters
        offset = 65
    elif 97 <= chr_code <= 122:
        # lower case letters
        offset = 97
    else:
        # leave other characters untouched
        return chr_code
    index = chr_code - offset
    index += shift
    return offset + (index % 26)


# pre-calculate the translations for the caesar cipher
CAESAR = {}
for shift in range(26):
    translation = {}
    for letter in ascii_letters:
        chr_code = ord(letter)
        output_chr_code = _caesar_chr(chr_code, shift)
        translation[chr_code] = output_chr_code
    CAESAR[shift] = translation


def caesar(text, shift):
    """This function preforms a caesar shift on the input text and returns the output. Any characters which are not letters are left unchanged."""
    return text.translate(CAESAR[shift % 26])


class CaesarCipher(CipherWindow):
    """Base Cipher Window for the Caesar Cipher"""

    def __init__(self, application, mode):
        self.numentry_shift = None

        super(CaesarCipher, self).__init__(application, "Caesar Cipher - " + mode)

    def get_key(self):
        """Returns the key or None if it is invalid"""
        return self.numentry_shift.get_num()

    def run_cipher(self, text, key):
        """Subclasses actually run the caesar cipher"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        self.numentry_shift = NumEntry(frame, label="Shift: ", min=0, max=26, default=1, callback=self.update_output)
        self.numentry_shift.grid(row=0, column=0)
        return frame


class CaesarEncrypt(CaesarCipher):
    """Caesar Encryption Cipher Window"""

    def __init__(self, application):
        super(CaesarEncrypt, self).__init__(application, "Encrypt")

    def run_cipher(self, text, shift):
        return caesar(text, shift)


class CaesarDecrypt(CaesarCipher):
    """Caesar Decryption Cipher Window"""

    def __init__(self, application):
        super(CaesarDecrypt, self).__init__(application, "Decrypt")

    def run_cipher(self, text, shift):
        # negative shift is the same as decryption
        return caesar(text, -shift)

    def get_solver(self):
        # Has to be imported here so the solver file can import the entire cipher file
        from solvers.caesar import CaesarSolver
        return CaesarSolver()
