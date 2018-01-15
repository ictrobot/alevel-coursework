import tkinter as tk
from string import ascii_uppercase

from cipher_window import CipherWindow
from ciphers.substitution import substitution


def keyword_mapping(keyword):
    """Generates the substitution mapping from a keyword"""
    # letters to be used as the keys
    input_letters = list(ascii_uppercase)
    # remaining letters to be mapped
    mapping_letters = list(ascii_uppercase)
    mapping = {}
    for letter in keyword.upper():
        if letter in mapping_letters:
            # if the letter hasn't already been mapped, map the next input
            # letter to it, and remove it from the letters to map
            mapping[input_letters.pop(0)] = letter
            mapping_letters.remove(letter)
    # map the remaining letters
    for letter in mapping_letters:
        mapping[input_letters.pop(0)] = letter
    return mapping


def valid_keyword(text):
    """Returns if the text is a valid keyword"""
    for letter in text:
        chr_code = ord(letter)
        if not (65 <= chr_code <= 90 or 97 <= chr_code <= 122):
            # if the character is not an uppercase or lowercase letter, invalid key
            return False
    # all uppercase or lowercase letters, so valid key
    return True


class KeywordCipher(CipherWindow):
    """Base Cipher Window for the Keyword Cipher"""

    def __init__(self, application, mode):
        self.stringvar_entry = None

        super(KeywordCipher, self).__init__(application, "Keyword Cipher - " + mode)

    def get_key(self):
        """Returns the key or None if it is invalid"""
        key = self.stringvar_entry.get()
        if len(key) > 0 and valid_keyword(key):
            return key

    def run_cipher(self, text, key):
        """Subclasses actually run the Keyword cipher"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        tk.Label(frame, text="Keyword: ").grid(row=0, column=0)
        self.stringvar_entry = tk.StringVar(frame)
        self.stringvar_entry.trace("w", lambda *args: self.update_output())
        tk.Entry(frame, validate="key", validatecommand=(frame.register(valid_keyword), "%P"), textvariable=self.stringvar_entry).grid(row=0, column=1)
        return frame


class KeywordEncrypt(KeywordCipher):
    """Keyword Encryption Cipher Window"""

    def __init__(self, application):
        super(KeywordEncrypt, self).__init__(application, "Encrypt")

    def run_cipher(self, text, keyword):
        mapping = keyword_mapping(keyword)
        return substitution(text, mapping)


class KeywordDecrypt(KeywordCipher):
    """Keyword Decryption Cipher Window"""

    def __init__(self, application):
        super(KeywordDecrypt, self).__init__(application, "Decrypt")

    def run_cipher(self, text, keyword):
        mapping = keyword_mapping(keyword)
        reversed_mapping = {b: a for a, b in mapping.items()}
        return substitution(text, reversed_mapping)
