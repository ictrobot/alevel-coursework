import tkinter as tk

from ciphers.cipher import Cipher
from utilities import greatest_common_divisor, mod_inverse
from widgets.numentry import NumEntry


def affine(text, a, b):
    """This function preforms the affine cipher on the input text and returns the output. Any characters which are not letters are left unchanged."""
    output = ""
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            output += letter
            continue
        index = chr_code - offset
        index *= a
        index += b
        chr_code = offset + (index % 26)
        output += chr(chr_code)
    return output


def reverse_affine(text, a, b):
    """ Reverse the affine function"""
    a_mod_inverse = mod_inverse(a, 26)
    if a_mod_inverse is None:
        # no mod inverse, so cannot be reversed
        raise ValueError("Cannot decrypt affine as A and 26 are not co-prime")

    output = ""
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            output += letter
            continue
        index = chr_code - offset
        index -= b
        index *= a_mod_inverse
        chr_code = offset + (index % 26)
        output += chr(chr_code)
    return output


class AffineCipher(Cipher):
    """Base Cipher implementation for the Affine Cipher"""

    def __init__(self, mode):
        super(AffineCipher, self).__init__("Affine Cipher - " + mode)
        self.numentry_a = None
        self.numentry_b = None

    def run(self, text):
        """Run the cipher"""
        a = self.numentry_a.get_num()
        b = self.numentry_b.get_num()
        # if the number entry is empty, return a blank string
        if a is None or b is None:
            return ""
        return self.shift(text, a, b)

    def shift(self, text, a, b):
        """Actually perform the affine cipher, overridden in subclasses"""
        raise NotImplementedError()

    def tk_options_frame(self, cipher_window):
        """Get the key input"""
        frame = tk.Frame(cipher_window)
        self.numentry_a = NumEntry(frame, label="A: ", min=0, max=26, default=1, callback=cipher_window.update_output)
        self.numentry_a.grid(row=0, column=0)
        self.numentry_b = NumEntry(frame, label="B: ", min=0, max=26, default=1, callback=cipher_window.update_output)
        self.numentry_b.grid(row=0, column=1)
        return frame


class AffineEncrypt(AffineCipher):
    """Affine Encryption Cipher implementation"""

    def __init__(self):
        super(AffineEncrypt, self).__init__("Encrypt")

    def tk_options_frame(self, cipher_window):
        # store the cipher window so the error message can be set in the shift function
        self.cipher_window = cipher_window
        # call the super method
        return super(AffineEncrypt, self).tk_options_frame(cipher_window)

    def shift(self, text, a, b):
        if greatest_common_divisor(a, 26) != 1:
            # display a warning that it is impossible to decrypt the cipher text
            self.cipher_window.set_error("Warning: cannot be decrypted as A and 26 are not co-prime")
        return affine(text, a, b)


class AffineDecrypt(AffineCipher):
    """Affine Decryption Cipher implementation"""

    def __init__(self):
        super(AffineDecrypt, self).__init__("Decrypt")

    def shift(self, text, a, b):
        # negative shift is the same as decryption
        return reverse_affine(text, a, b)
