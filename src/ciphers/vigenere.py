import tkinter as tk
from cipher_window import CipherWindow


def string_to_shifts(text):
    """Converts a string representing the shifts of a Vigenère cipher into a list
    of the shifts. e.g. ABC -> [1, 2, 3] """
    shifts = []
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            shifts.append(chr_code - 65)
        elif 97 <= chr_code <= 122:
            shifts.append(chr_code - 97)
    return shifts


def vigenere(text, shifts):
    """Performs Vigenère cipher on the input text. shifts must be a list of shifts,
    which can be produced using string_to_shifts(string)"""

    if len(shifts) == 0:
        raise ValueError("Must be at least one shift")

    output = ""
    # the index of the next shift to use
    shift_index = 0
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
        index += shifts[shift_index]
        chr_code = offset + (index % 26)
        output += chr(chr_code)
        # update the shift for the next letter
        shift_index = (shift_index + 1) % len(shifts)
    return output


def reverse_vigenere(text, shifts):
    """Reverses the Vigenère cipher by making all the shifts negative."""
    return vigenere(text, [-shift for shift in shifts])


def valid_key(text):
    """Returns if the text is a valid encryption/decryption key"""
    for letter in text:
        chr_code = ord(letter)
        if not (65 <= chr_code <= 90 or 97 <= chr_code <= 122):
            # if the character is not an uppercase or lowercase letter, invalid key
            return False
    # all uppercase or lowercase letters, so valid key
    return True


class VigenereCipher(CipherWindow):
    """Base Cipher Window for the Vigenère Cipher"""

    def __init__(self, application, mode):
        self.stringvar_entry = None

        super(VigenereCipher, self).__init__(application, "Vigenère Cipher - " + mode)

    def get_key(self):
        """Returns the key or None if it is invalid"""
        key = self.stringvar_entry.get()
        if len(key) > 0 and valid_key(key):
            return key

    def run_cipher(self, text, key):
        """Subclasses actually run the Vigenère cipher"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        tk.Label(frame, text="Key: ").grid(row=0, column=0)
        self.stringvar_entry = tk.StringVar(frame)
        self.stringvar_entry.trace("w", lambda *args: self.update_output())
        tk.Entry(frame, validate="key", validatecommand=(frame.register(valid_key), "%P"), textvariable=self.stringvar_entry).grid(row=0, column=1)
        return frame


class VigenereEncrypt(VigenereCipher):
    """Vigenère Encryption Cipher Window"""

    def __init__(self, application):
        super(VigenereEncrypt, self).__init__(application, "Encrypt")

    def run_cipher(self, text, key):
        shifts = string_to_shifts(key)
        return vigenere(text, shifts)


class VigenereDecrypt(VigenereCipher):
    """Vigenère Decryption Cipher Window"""

    def __init__(self, application):
        super(VigenereDecrypt, self).__init__(application, "Decrypt")

    def run_cipher(self, text, key):
        shifts = string_to_shifts(key)
        return reverse_vigenere(text, shifts)

    def get_solver(self):
        # Has to be imported here so the solver file can import the entire cipher file
        from solvers.vigenere import VigenereSolver
        return VigenereSolver()
