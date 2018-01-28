import tkinter as tk

from solver_window import SolverWindow
from utilities import SUBTITLE_LABEL_OPTIONS, TITLE_LABEL_OPTIONS
from widgets.outputtext import OutputText


class CipherWindow(tk.Frame):

    def __init__(self, application, name):
        super(CipherWindow, self).__init__(application)
        self.application = application
        self.name = name

        self.create_widgets()

    def create_widgets(self):
        """ Setup the widgets for the cipher window """
        tk.Label(self, text=self.name, **TITLE_LABEL_OPTIONS).grid(row=0, column=0)

        tk.Label(self, text="Input", **SUBTITLE_LABEL_OPTIONS).grid(row=1, column=0)
        # setup input text box so the output is updated every time the input changes.
        self.text_input = tk.Text(self, height=7, width=80, wrap=tk.WORD)
        self.text_input.grid(row=2, column=0, sticky="NSEW")
        self.text_input.bind("<<Modified>>", self.input_modified)

        # get key input from cipher
        self.tk_key_frame().grid(row=3, column=0)

        # error label
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.grid(row=4, column=0)

        tk.Label(self, text="Output", **SUBTITLE_LABEL_OPTIONS).grid(row=5, column=0)
        # setup output text box which cannot be edited.
        self.output_text = OutputText(self, height=7, width=80, wrap=tk.WORD)
        self.output_text.grid(row=6, column=0, sticky="NSEW")

        # back button
        tk.Button(self, text="Back", command=lambda: self.application.show_main_menu()).grid(row=0, column=1, sticky="NE")

        # solve button
        if self.get_solver() is not None:
            self.solve_button = tk.Button(self, text="Solve", command=self.show_solver, state="disabled")
            self.solve_button.grid(row=3, column=1, sticky="NE")
        else:
            self.solve_button = None

        # when expanding the height of the window, expand the size of the text boxes.
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=1)
        # when expanding the width of the window, expand the main column
        self.grid_columnconfigure(0, weight=1)

    def input_modified(self, event):
        """Callback for when the input text box is modified"""
        if self.text_input.edit_modified():
            self.update_output()
        self.text_input.edit_modified(False)

    def update_output(self):
        """Runs the cipher on the text in the input box and puts the result in the output box"""
        # first set the error label to be empty
        self.set_error("")
        # get the input text and key
        input_text = self.get_input_text()

        if self.solve_button is not None:
            # if the input is at least 4 long, enable the solve button
            self.solve_button["state"] = "normal" if len(input_text) >= 4 else "disabled"

        key = self.get_key()
        if key is None:
            # if the key is invalid
            output_text = ""
        else:
            # try and run the cipher on the input text
            try:
                output_text = self.run_cipher(input_text, key)
            except ValueError as e:
                # an error has happened, display it in the label
                self.set_error(str(e))
                output_text = ""
        # update the output text box with the new output text
        self.output_text.set_text(output_text)

    def set_error(self, text):
        """Sets the error label to the text provided"""
        self.error_label["text"] = text

    def get_input_text(self):
        """Get the input text"""
        return self.text_input.get(1.0, tk.END).strip()

    def show_solver(self):
        self.application.show(SolverWindow, self.get_solver(), self.get_input_text(), self)

    # The below methods are designed to be overridden by cipher implementations
    def get_key(self):
        """Returns the key to be used for the cipher, or none if it is invalid"""
        return None

    def run_cipher(self, text, key):
        """Run the cipher on the text and return the output"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Returns the tkinter frame with the key inputs for the cipher"""
        raise NotImplementedError()

    def get_solver(self):
        """Returns the solver if there is one"""
        return None
