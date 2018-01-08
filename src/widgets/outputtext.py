import tkinter as tk


class OutputText(tk.Text):
    """ An output text box which disallows editing but allows copying """

    def __init__(self, master, *args, **kwargs):
        super(OutputText, self).__init__(master, *args, **kwargs, state=tk.DISABLED)
        self.bind("<1>", self.force_focus_set)

    def force_focus_set(self, event):
        """Fixes copying from disabled text box on Ubuntu"""
        self.focus_set()

    def set_text(self, text):
        """Helper method to set the text"""
        # to set text you must first set it so it is editable,
        # then delete all the old text, insert the new text
        # and then disable editing again.
        self.configure(state=tk.NORMAL)
        self.delete(1.0, tk.END)
        self.insert(tk.END, text)
        self.configure(state=tk.DISABLED)
