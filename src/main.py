import tkinter as tk

from cipher_window import CipherWindow
from ciphers.caesar import CaesarDecrypt, CaesarEncrypt
from utilities import SUBTITLE_LABEL_OPTIONS, TITLE_LABEL_OPTIONS


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        """ Setup the widgets for the main menu """

        tk.Label(self, text="Ciphers", **TITLE_LABEL_OPTIONS).grid(row=0, sticky="NW")

        tk.Label(self, text="Simple Substitution Ciphers", **SUBTITLE_LABEL_OPTIONS).grid(row=1, sticky="NW")

        tk.Label(self, text="Caesar Cipher").grid(row=2, sticky="NW")
        tk.Button(self, text="Encrypt", command=lambda: self.show_cipher(CaesarEncrypt)).grid(row=2, sticky="NESW", column=1)
        tk.Button(self, text="Decrypt", command=lambda: self.show_cipher(CaesarDecrypt)).grid(row=2, sticky="NESW", column=2)

    def show_cipher(self, cipher_class):
        """Display the cipher window"""
        cipher_instance = cipher_class()
        new_root = tk.Tk()
        CipherWindow(new_root, cipher_instance).pack()
        # destroy main menu
        self.master.destroy()
        # run new window
        new_root.mainloop()


if __name__ == "__main__":
    # Only start the program when this file is run, not when it is imported.
    root = tk.Tk()
    MainMenu(root).pack()
    root.mainloop()
