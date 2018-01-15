import tkinter as tk

from ciphers.affine import AffineDecrypt, AffineEncrypt
from ciphers.caesar import CaesarDecrypt, CaesarEncrypt
from ciphers.keyword import KeywordDecrypt, KeywordEncrypt
from ciphers.scytale import ScytaleDecrypt, ScytaleEncrypt
from ciphers.vigenere import VigenereEncrypt, VigenereDecrypt
from ciphers.substitution import SubstitutionCipher
from utilities import SUBTITLE_LABEL_OPTIONS, TITLE_LABEL_OPTIONS


class Application(tk.Tk):
    """Handles swapping between windows"""

    def __init__(self):
        super(Application, self).__init__()
        # set the window title & that it is not resizable.
        self.title("Ciphers")
        self.resizable(0, 0)
        self.frame = None
        # When first opened, display the Main Menu
        self.show_main_menu()

    def show_main_menu(self):
        """ Shows the main menu. Avoids circular imports """
        self.show(MainMenu)

    def show(self, frame_class=None, *args, **kwargs):
        """ Constructs an instance of the class frame_class and shows the resulting frame """
        # remove the old frame if there was one
        if self.frame is not None:
            self.frame.forget()
        # make the new frame and pack it into the window
        self.frame = frame_class(self, *args, **kwargs)
        self.frame.pack()


class MainMenu(tk.Frame):
    def __init__(self, application):
        super().__init__(application)
        self.application = application
        self.next_row = 1
        self.create_widgets()

    def create_subtitle(self, text):
        """Helper function to simplify the creation of subtitles"""
        # make the subtitle
        tk.Label(self, text=text, **SUBTITLE_LABEL_OPTIONS).grid(row=self.next_row, sticky="NW")
        # increment the next_row variable so the next item goes on the next row
        self.next_row += 1

    def create_cipher_entry(self, cipher_name, cipher_encrypt, cipher_decrypt):
        """Helper function to simplify the creation of cipher entries. If there is one shared encrypt and decrypt window, pass None to cipher_decrypt"""
        # add label with the cipher's name
        tk.Label(self, text=cipher_name).grid(row=self.next_row, column=0, sticky="NW")

        if cipher_decrypt is not None:
            # different encrypt and decrypt buttons

            # setup the encrypt button
            def encrypt_command():
                self.application.show(cipher_encrypt)
            encrypt_button = tk.Button(self, text="Encrypt", command=encrypt_command)
            encrypt_button.grid(row=self.next_row, column=1, sticky="NESW")

            # setup the decrypt button
            def decrypt_command():
                self.application.show(cipher_decrypt)
            decrypt_button = tk.Button(self, text="Decrypt", command=decrypt_command)
            decrypt_button.grid(row=self.next_row, column=2, sticky="NESW")
        else:
            # one shared encrypt and decrypt button

            # setup the encrypt/decrypt button
            def shared_command():
                self.application.show(cipher_encrypt)
            encrypt_button = tk.Button(self, text="Encrypt/Decrypt", command=shared_command)
            encrypt_button.grid(row=self.next_row, column=1, columnspan=2, sticky="NESW")

        # increment the next_row variable so the next item goes on the next row
        self.next_row += 1

    def create_widgets(self):
        """ Setup the widgets for the main menu """

        tk.Label(self, text="Ciphers", **TITLE_LABEL_OPTIONS).grid(row=0, sticky="NW")

        self.create_subtitle("Simple Substitution Ciphers")
        self.create_cipher_entry("Caesar Cipher", CaesarEncrypt, CaesarDecrypt)
        self.create_cipher_entry("Affine Cipher", AffineEncrypt, AffineDecrypt)
        self.create_cipher_entry("Keyword Cipher", KeywordEncrypt, KeywordDecrypt)
        self.create_cipher_entry("Substitution Cipher", SubstitutionCipher, None)

        self.create_subtitle("Polyalphabetic Substitution Ciphers")
        self.create_cipher_entry("Vigenère Cipher", VigenereEncrypt, VigenereDecrypt)

        self.create_subtitle("Transposition Ciphers")
        self.create_cipher_entry("Scytale Cipher", ScytaleEncrypt, ScytaleDecrypt)


if __name__ == "__main__":
    # Only start the program when this file is run, not when it is imported.
    Application().mainloop()
