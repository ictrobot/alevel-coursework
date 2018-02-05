import tkinter as tk

from cipher_window import CipherWindow
from utilities import greatest_common_divisor, mod_inverse
from widgets.numentry import NumEntry
from string import ascii_letters

# store all the possible values of A (where a & 26 have a modular inverse)
POSSIBLE_VALUES_A = [i for i in range(1, 25) if mod_inverse(i, 26) is not None]


def _affine_chr(chr_code, a, b):
    """This function preforms the affine cipher on a single letter as a character code. Used to pre-calculate the translations"""
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
    index *= a
    index += b
    return offset + (index % 26)


def _reverse_affine_chr(chr_code, a, b):
    """ Reverse the affine function on a single letter as a character code"""
    a_mod_inverse = mod_inverse(a, 26)
    if a_mod_inverse is None:
        # no mod inverse, so cannot be reversed
        raise ValueError("Cannot decrypt affine as A and 26 are not co-prime")
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
    index -= b
    index *= a_mod_inverse
    return offset + (index % 26)


# pre-calculate the translations for the affine cipher
ASCII_LETTERS = [ord(l) for l in ascii_letters]
AFFINE = {}
for a in range(0, 26):
    for b in range(0, 26):
        AFFINE[a, b] = {}
        for letter in ascii_letters:
            chr_code = ord(letter)
            AFFINE[a, b][chr_code] = _affine_chr(chr_code, a, b)

REVERSE_AFFINE = {}
for a in POSSIBLE_VALUES_A:
    for b in range(0, 26):
        REVERSE_AFFINE[a, b] = {}
        for letter in ascii_letters:
            chr_code = ord(letter)
            REVERSE_AFFINE[a, b][chr_code] = _reverse_affine_chr(chr_code, a, b)


def affine(text, a, b):
    """This function preforms the affine cipher on the input text and returns the output. Any characters which are not letters are left unchanged."""
    return text.translate(AFFINE[a % 26, b % 26])


def reverse_affine(text, a, b):
    """ Reverses the affine function"""
    if a not in POSSIBLE_VALUES_A:
        raise ValueError("Cannot decrypt affine as A and 26 are not co-prime")
    return text.translate(REVERSE_AFFINE[a, b % 26])


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
