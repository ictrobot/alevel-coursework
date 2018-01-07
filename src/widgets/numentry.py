import tkinter as tk


class NumEntry(tk.Frame):
    def __init__(self, master, min=None, max=None, default=None, callback=None, label=None):
        """Create a number entry which only allows numbers between min & max, defaults to default and calls the callback when modified."""
        super(NumEntry, self).__init__(master)
        self.min = min
        self.max = max
        self.callback = callback
        # setup a tkinter StringVar to store the current text in the entry
        self.stringvar = tk.StringVar(master)
        # if a default is provided, set the StringVar to contain it
        if default:
            self.stringvar.set(str(default))
        # if a callback is provided, set the StringVar to call it when changed.
        if callback:
            # on write ('w') call the callback, the lambda is used to gobble the tkinter event
            self.stringvar.trace("w", lambda *args: callback())

        # setup widgets
        if label is not None:
            tk.Label(self, text=label).grid(row=0, column=0)
        tk.Entry(self, width=5, textvariable=self.stringvar, validate="key", validatecommand=(master.register(self.valid_input), "%P")).grid(row=0, column=1)
        tk.Button(self, text="▲", command=self.increment).grid(row=0, column=2)
        tk.Button(self, text="▼", command=self.decrement).grid(row=0, column=3)

    def valid_input(self, text):
        """Callback from tkinter to validate if the new text is valid"""
        # allow empty
        if not text:
            return True

        try:
            i = int(text)
        except ValueError:
            # if its not an int, do not allow
            return False
        # if its not in range, do not allow
        if self.min is not None and i < self.min:
            return False
        if self.max is not None and i > self.max:
            return False
        # allow as it must be an int in range
        return True

    def set_max(self, max):
        """Update the maximum number"""
        self.max = max
        if max is not None and self.get_num() is not None and self.get_num() > max:
            # the current number is greater than the new maximum, so update the stored number
            self.stringvar.set(str(max))
            if self.callback:
                self.callback()

    def set_min(self, min):
        """Update the minimum number"""
        self.min = min
        if min is not None and self.get_num() is not None and self.get_num() < min:
            # the current number is smaller than the new minimum, so update the stored number
            self.stringvar.set(str(min))
            if self.callback:
                self.callback()

    def get_num(self, empty=None):
        """Get the number entered"""
        text = self.stringvar.get()
        # if the text is empty, return the empty parameter
        if not text:
            return empty
        # otherwise the text must be a valid int as it is validated each time it is modified.
        return int(text)

    def increment(self):
        """Increments the stored number"""
        # get the number, use 0 if the box is empty, and add one
        i = self.get_num(0) + 1
        # if this is above the max, set the new number to the maximum
        if self.max is not None and i > self.max:
            i = self.max
        # update the StringVar & call the callback
        self.stringvar.set(str(i))
        if self.callback:
            self.callback()
        return i

    def decrement(self):
        """Decrements the stored number"""
        # get the number, use 0 if the box is empty, and subtract one
        i = self.get_num(0) - 1
        # if this is below the minimum, set the new number to the minimum
        if self.min is not None and i < self.min:
            i = self.min
        # update the StringVar & call the callback
        self.stringvar.set(str(i))
        if self.callback:
            self.callback()
        return i
