import tkinter as tk

from cipher_window import CipherWindow
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


class AffineCipher(CipherWindow):
    """Base Cipher Window for the Affine Cipher"""

    def __init__(self, application, mode):
        self.numentry_a = None
        self.numentry_b = None

        super(AffineCipher, self).__init__(application, "Affine Cipher - " + mode)

    def get_key(self):
        """Returns the key or None if it is invalid"""
        a = self.numentry_a.get_num()
        b = self.numentry_b.get_num()
        if a is None or b is None:
            return None
        return a, b

    def run_cipher(self, text, key):
        """Subclasses actually run the affine cipher"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        self.numentry_a = NumEntry(frame, label="A: ", min=0, max=26, default=1, callback=self.update_output)
        self.numentry_a.grid(row=0, column=0)
        self.numentry_b = NumEntry(frame, label="B: ", min=0, max=26, default=1, callback=self.update_output)
        self.numentry_b.grid(row=0, column=1)
        return frame


class AffineEncrypt(AffineCipher):
    """Affine Encryption Cipher Window"""

    def __init__(self,  application):
        super(AffineEncrypt, self).__init__( application, "Encrypt")

    def run_cipher(self, text, key):
        a, b = key
        if greatest_common_divisor(a, 26) != 1:
            # display a warning that it is impossible to decrypt the cipher text
            self.set_error("Warning: cannot be decrypted as A and 26 are not co-prime")
        return affine(text, a, b)


class AffineDecrypt(AffineCipher):
    """Affine Decryption Cipher Window"""

    def __init__(self,  application):
        super(AffineDecrypt, self).__init__( application,"Decrypt")

    def run_cipher(self, text, key):
        a, b = key
        # negative shift is the same as decryption
        return reverse_affine(text, a, b)

    def get_solver(self):
        # Has to be imported here so the solver file can import the entire cipher file
        from solvers.affine import AffineSolver
        return AffineSolver()
