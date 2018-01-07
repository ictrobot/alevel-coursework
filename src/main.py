import tkinter as tk

from cipher_window import CipherWindow
from ciphers.affine import AffineDecrypt, AffineEncrypt
from ciphers.caesar import CaesarDecrypt, CaesarEncrypt
from ciphers.scytale import ScytaleDecrypt, ScytaleEncrypt
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
        self.create_widgets()

    def create_widgets(self):
        """ Setup the widgets for the main menu """

        tk.Label(self, text="Ciphers", **TITLE_LABEL_OPTIONS).grid(row=0, sticky="NW")

        tk.Label(self, text="Simple Substitution Ciphers", **SUBTITLE_LABEL_OPTIONS).grid(row=1, sticky="NW")

        tk.Label(self, text="Caesar Cipher").grid(row=2, sticky="NW")
        tk.Button(self, text="Encrypt", command=lambda: self.application.show(CipherWindow, CaesarEncrypt())).grid(row=2, sticky="NESW", column=1)
        tk.Button(self, text="Decrypt", command=lambda: self.application.show(CipherWindow, CaesarDecrypt())).grid(row=2, sticky="NESW", column=2)

        tk.Label(self, text="Affine Cipher").grid(row=3, sticky="NW")
        tk.Button(self, text="Encrypt", command=lambda: self.application.show(CipherWindow, AffineEncrypt())).grid(row=3, sticky="NESW", column=1)
        tk.Button(self, text="Decrypt", command=lambda: self.application.show(CipherWindow, AffineDecrypt())).grid(row=3, sticky="NESW", column=2)

        tk.Label(self, text="Transposition Ciphers", **SUBTITLE_LABEL_OPTIONS).grid(row=4, sticky="NW")

        tk.Label(self, text="Scytale Cipher").grid(row=5, sticky="NW")
        tk.Button(self, text="Encrypt", command=lambda: self.application.show(CipherWindow, ScytaleEncrypt())).grid(row=5, sticky="NESW", column=1)
        tk.Button(self, text="Decrypt", command=lambda: self.application.show(CipherWindow, ScytaleDecrypt())).grid(row=5, sticky="NESW", column=2)


if __name__ == "__main__":
    # Only start the program when this file is run, not when it is imported.
    Application().mainloop()
