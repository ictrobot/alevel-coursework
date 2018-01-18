import tkinter as tk
import numpy
import itertools


class MatrixEntry(tk.Frame):
    """A Tkinter Matrix Input which can be resized."""

    def __init__(self, master, rows, columns, min_value=None, max_value=None, default_value=0, callback=None):
        super(MatrixEntry, self).__init__(master)
        self.rows = rows
        self.columns = columns
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.callback = callback

        self.stringvars = {}
        self.entries = {}
        self.validate_command = (self.master.register(self.valid_input), "%P")

        # setup each individual entry widget
        for r in range(self.rows):
            for c in range(self.columns):
                # setup the stringvar
                stringvar = tk.StringVar(self)
                if self.default_value is not None:
                    stringvar.set(str(self.default_value))
                if self.callback is not None:
                    stringvar.trace("w", lambda *args: self.callback())
                self.stringvars[r, c] = stringvar
                # setup the entry widget
                self.entries[r, c] = tk.Entry(self, width=3, textvariable=stringvar, validate="key", validatecommand=self.validate_command)
                self.entries[r, c].grid(row=r, column=c)

    def get_numpy_matrix(self):
        """Returns the matrix as a numpy matrix. Any empty widget will be assumed to be 0."""
        matrix_data = []
        for r in range(self.rows):
            row_data = []
            for c in range(self.columns):
                try:
                    value = int(self.stringvars[r, c].get())
                except ValueError:
                    value = 0
                row_data.append(value)
            matrix_data.append(row_data)
        return numpy.matrix(matrix_data)

    def set_matrix(self, numpy_matrix):
        """Sets the contents from a numpy_matrix"""
        # check the size of the matrix and resize if necessary
        m_rows, m_columns = numpy_matrix.shape
        if m_rows != self.rows or m_columns != self.columns:
            self.resize(m_rows, m_columns)
        # loop through and set individual element
        for (r, c), value in numpy.ndenumerate(numpy_matrix):
            if self.valid_input(str(value)):
                self.stringvars[r, c].set(str(value))
            else:
                raise ValueError("set_matrix matrix element is not valid")

    def resize(self, new_rows, new_columns):
        """Resize the entry"""
        new = set(itertools.product(range(new_rows), range(new_columns)))
        old = set(itertools.product(range(self.rows), range(self.columns)))
        # calculate which entries to add and which to remove
        additional = new - old
        remove = old - new
        # remove the entries which are no longer needed
        for r, c in remove:
            self.entries[r, c].destroy()
            del self.entries[r, c]
            del self.stringvars[r, c]
        # setup the new entries
        for r, c in additional:
            # setup the stringvar
            stringvar = tk.StringVar(self.master)
            if self.default_value is not None:
                stringvar.set(str(self.default_value))
            if self.callback is not None:
                stringvar.trace("w", lambda *args: self.callback())
            self.stringvars[r, c] = stringvar
            # setup the entry widget
            self.entries[r, c] = tk.Entry(self, width=3, textvariable=stringvar, validate="key", validatecommand=self.validate_command)
            self.entries[r, c].grid(row=r, column=c)
        # store the new size
        self.rows = new_rows
        self.columns = new_columns
        # call the callback as the matrix has changed
        if self.callback is not None:
            self.callback()

    def valid_input(self, text):
        """Validate one of the individual entry widgets"""
        if not text:
            return True
        try:
            i = int(text)
        except ValueError:
            return False
        if self.min_value is not None and i < self.min_value:
            return False
        if self.max_value is not None and i > self.max_value:
            return False
        return True
