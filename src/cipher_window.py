import tkinter as tk

from utilities import TITLE_LABEL_OPTIONS, SUBTITLE_LABEL_OPTIONS


class CipherWindow(tk.Frame):

    def __init__(self, application, cipher):
        super(CipherWindow, self).__init__(application)
        self.application = application
        self.cipher = cipher

        self.create_widgets()

    def create_widgets(self):
        """ Setup the widgets for the cipher window """
        tk.Label(self, text=self.cipher.name, **TITLE_LABEL_OPTIONS).grid(row=0, column=0)

        tk.Label(self, text="Input", **SUBTITLE_LABEL_OPTIONS).grid(row=1, column=0)
        # setup input text box so the output is updated every time the input changes.
        self.text_input = tk.Text(self, height=7, width=80, wrap=tk.WORD)
        self.text_input.grid(row=2, column=0, sticky="NSEW")
        self.text_input.bind("<<Modified>>", self.input_modified)

        # get key input from cipher
        self.cipher.tk_options_frame(self).grid(row=3, column=0)

        tk.Label(self, text="Output", **SUBTITLE_LABEL_OPTIONS).grid(row=4, column=0)
        # setup output text box which cannot be edited.
        self.output_text = tk.Text(self, height=7, width=80, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=5, column=0, sticky="NSEW")

        # back button
        tk.Button(self, text="Back", command=lambda: self.application.show_main_menu()).grid(row=0, column=1, sticky="NE")

        # when expanding the height of the window, expand the size of the text boxes.
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)
        # when expanding the width of the window, expand the main column
        self.grid_columnconfigure(0, weight=1)

    def input_modified(self, event):
        """Callback for when the input text box is modified"""
        if self.text_input.edit_modified():
            self.update_output()
        self.text_input.edit_modified(False)

    def update_output(self):
        """Runs the cipher on the text in the input box and puts the result in the output box"""
        text_in = self.text_input.get(1.0, tk.END).strip()
        text_out = self.cipher.run(text_in)

        # to set text you must first set it so it is editable, then delete all the old text, insert the new text and then disable editing again.
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text_out)
        self.output_text.configure(state=tk.DISABLED)
