class Cipher:
    """Base class for all ciphers"""

    def __init__(self, name):
        self.name = name

    def tk_options_frame(self, cipher_window):
        """Returns the tkinter frame with the key inputs for the cipher"""
        raise NotImplementedError()

    def run(self, text):
        """Run the cipher on the text and return the output"""
        raise NotImplementedError()
