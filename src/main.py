import tkinter as tk

from utilities import TITLE_LABEL_OPTIONS, SUBTITLE_LABEL_OPTIONS


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        """ Setup the widgets for the main menu """

        tk.Label(self, text="Ciphers", **TITLE_LABEL_OPTIONS).grid(row=0, sticky="NW")

        tk.Label(self, text="Simple Substitution Ciphers", **SUBTITLE_LABEL_OPTIONS).grid(row=1, sticky="NW")

        tk.Label(self, text="Caesar Cipher").grid(row=2, sticky="NW")
        tk.Button(self, text="Encrypt", command=lambda: None).grid(row=2, sticky="NESW", column=1)
        tk.Button(self, text="Decrypt", command=lambda: None).grid(row=2, sticky="NESW", column=2)


if __name__ == "__main__":
    # Only start the program when this file is run, not when it is imported.
    root = tk.Tk()
    MainMenu(root).pack()
    root.mainloop()
