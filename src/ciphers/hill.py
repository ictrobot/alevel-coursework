import tkinter as tk
from tkinter import messagebox
from string import ascii_uppercase

import numpy

from cipher_window import CipherWindow
from utilities import mod_inverse, greatest_common_divisor
from widgets.numentry import NumEntry
from widgets.matrixentry import MatrixEntry


def hill(text, key, pad="Z"):
    """This function performs the hill cipher on the input text and returns the output. Any characters which are not letters are removed and the message may be padded."""
    
    # check the key matrix is square
    key_rows, key_columns = key.shape
    if key_rows != key_columns:
        raise ValueError("Key must be a square matrix")
    # strip all non letter characters
    message = ""
    for letter in text.upper():
        if 65 <= ord(letter) <= 90:
            message += letter
    # check if pad is an uppercase letter
    if pad not in ascii_uppercase or len(pad) != 1:
        raise ValueError("Pad must be an uppercase letter")
    # pad the message so the length of the message is a multiple of key order
    while len(message) % key_rows != 0:
        message += pad
    
    # actually perform the hill cipher
    output = ""
    for i in range(0, len(message), key_rows):
        # convert the next group of letters into a matrix
        message_matrix_data = []
        for letter in message[i:i+key_rows]:
            letter_num = ord(letter) - 65
            message_matrix_data.append([letter_num])
        message_matrix = numpy.matrix(message_matrix_data)
        # transform the matrix using the key
        transformed_matrix = (key * message_matrix) % 26
        # convert the result back into letters
        for j in range(key_rows):
            letter_num = int(transformed_matrix.item(j))
            output += ascii_uppercase[letter_num]
    return output


def reverse_hill(ciphertext, key):
    """This function reverses the hill cipher and returns the output."""

    # check the key matrix is square
    key_rows, key_columns = key.shape
    if key_rows != key_columns:
        raise ValueError("Key must be a square matrix")
    # check the ciphertext length is a multiple of key order
    if len(ciphertext) % key_rows != 0:
        raise ValueError("Ciphertext length must be a multiple of the order of the key matrix")
    # check the ciphertext only contains letters
    for letter in ciphertext:
        if not 65 <= ord(letter) <= 90:
            raise ValueError("Ciphertext must only contain letters A-Z")
    # calculate the det of the matrix and check the matrix is not singular
    det = int(round(numpy.linalg.det(key)))
    if det == 0:
        raise ValueError("Cannot decrypt as det(key) == 0")
    # Calculate adjugate of the matrix
    # inverse(A) = ( 1 / det(A) ) * adjugate(A)
    # therefore
    # adjugate(A) = inverse(A) * det(A)
    adjugate = numpy.rint(numpy.linalg.inv(key) * det).astype(int)
    # Calculate modular inverse of det(key)
    det_mod_inverse = mod_inverse(det, 26)
    if det_mod_inverse is None:
        raise ValueError("Cannot decrypt as 26 and det(key) need to be co-prime")
    # Calculate modular multiplicative inverse
    inverse_key = (det_mod_inverse * adjugate) % 26

    # perform the hill cipher using the inverse_key
    output = ""
    for i in range(0, len(ciphertext), key_rows):
        # convert the next group of letters into a matrix
        message_matrix_data = []
        for letter in ciphertext[i:i+key_rows]:
            letter_num = ord(letter) - 65
            message_matrix_data.append([letter_num])
        message_matrix = numpy.matrix(message_matrix_data)
        # transform the matrix using the key
        transformed_matrix = (inverse_key * message_matrix) % 26
        # convert the result back into letters
        for j in range(key_rows):
            letter_num = int(transformed_matrix.item(j))
            output += ascii_uppercase[letter_num]
    return output


def check_key_reversible(key):
    """Convenience method to quickly check if the key is reversible without actually doing the full decryption process"""
    det = int(round(numpy.linalg.det(key)))
    if det == 0:
        return False, "Impossible to decrypt as det(key) == 0"
    if greatest_common_divisor(det, 26) != 1:
        return False, "Impossible to decrypt as 26 and det(key) need to be co-prime"
    return True, ""


class HillCipher(CipherWindow):
    """Base Cipher Window for the Hill Cipher"""

    def __init__(self, application, mode):
        self.matrix_input = None
        self.order_input = None
        self.current_order = 2

        super(HillCipher, self).__init__(application, "Hill Cipher - " + mode)

    def get_key(self):
        """Returns the key or None if it is invalid"""
        # resize the matrix first if needed
        order = self.order_input.get_num()
        if order is not None and order != self.current_order:
            self.current_order = order
            self.matrix_input.resize(order, order)
        # get numpy matrix representing the matrix input
        return self.matrix_input.get_numpy_matrix()

    def run_cipher(self, text, key):
        """Subclasses actually run the hill cipher"""
        raise NotImplementedError()

    def tk_key_frame(self):
        """Get the key input"""
        frame = tk.Frame(self)
        # setup numentry for matrix order
        self.order_input = NumEntry(frame, label="Order: ", min=2, default=self.current_order, callback=self.update_output)
        self.order_input.grid(row=0, column=0, sticky="NW")

        # add option buttons
        self.option_buttons_frame(frame).grid(row=1, column=0, sticky="NW")
        # set the bottom empty row to expand so the option buttons don't move
        frame.grid_rowconfigure(2, weight=1)

        # set the middle empty column to expand to fill the free space
        frame.grid_columnconfigure(1, weight=1)

        # setup matrixentry for the actual matrix
        self.matrix_input = MatrixEntry(frame, self.current_order, self.current_order, callback=self.update_output)
        self.matrix_input.grid(row=0, column=2, rowspan=3, sticky="NE")

        return frame

    def option_buttons_frame(self, key_frame):
        """Additional useful buttons"""
        frame = tk.Frame(key_frame)
        tk.Button(frame, text="Copy Matrix", command=self.copy_matrix).grid(sticky="EW")
        tk.Button(frame, text="Paste Matrix", command=self.paste_matrix).grid(sticky="EW")
        tk.Button(frame, text="Random Matrix", command=self.random_matrix).grid(sticky="EW")
        return frame

    def copy_matrix(self):
        """Copy the key matrix to the clipboard"""
        matrix = self.matrix_input.get_numpy_matrix()
        # convert the matrix to text
        rows = []
        for i in range(self.current_order):
            row = []
            for j in range(self.current_order):
                row.append(str(matrix.item(i, j)))
            rows.append("\t".join(row))
        text = "\n".join(rows)
        # tries to set the clipboard to the text
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
        except tk.TclError:
            messagebox.showerror("Error", "Failed to write to clipboard")

    def paste_matrix(self):
        """Paste the key matrix from the clipboard"""
        # tries to read the contents of the clipboard
        try:
            contents = self.clipboard_get()
        except tk.TclError:
            messagebox.showerror("Error", "Failed to read from clipboard")
            return
        try:
            # try to parse the contents
            rows = contents.split("\n")
            matrix_data = [[0 for j in range(len(rows))] for i in range(len(rows))]
            for i in range(len(rows)):
                row = rows[i].split("\t")
                if len(row) != len(rows):
                    raise ValueError
                for j in range(len(rows)):
                    matrix_data[i][j] = int(row[j])
            matrix = numpy.matrix(matrix_data)
            # set the matrix
            self.matrix_input.set_matrix(matrix)
            self.order_input.set_num(len(rows))
            self.current_order = len(rows)
        except ValueError:
            messagebox.showerror("Error", "Failed to parse key from clipboard")

    def random_matrix(self):
        """Generate a random key matrix"""
        # finding a large matrix which is reversible for the hill cipher can take a long time
        # therefore I decided to limit it to matrices less than 15x15.
        if self.current_order > 15:
            messagebox.showerror("Error", "Random matrix generation is only supported with order 15 or less")
            return
        # generate random matrices
        matrix_size = (self.current_order, self.current_order)
        while True:
            random_array = numpy.random.randint(0, 25, size=matrix_size)
            reversible, reason = check_key_reversible(random_array)
            if reversible:
                # if it is reversible set it as the key matrix & return
                matrix = numpy.asmatrix(random_array)
                self.matrix_input.set_matrix(matrix)
                return

    def create_widgets(self):
        super(HillCipher, self).create_widgets()
        # get the key frame and set it to fill available space
        for widget in self.grid_slaves(3, 0): # row and column of grid frame
            widget.grid_forget()
            widget.grid(row=3, column=0, sticky="NESW")


class HillEncrypt(HillCipher):
    """Hill Encryption Cipher Window"""

    def __init__(self, application):
        super(HillEncrypt, self).__init__(application, "Encrypt")

    def run_cipher(self, text, matrix):
        # check if the matrix is reversible, if it not display a warning
        reversible, reason = check_key_reversible(matrix)
        if not reversible:
            self.set_error(reason)
        return hill(text, matrix)


class HillDecrypt(HillCipher):
    """Hill Decryption Cipher Window"""

    def __init__(self, application):
        super(HillDecrypt, self).__init__(application, "Decrypt")

    def run_cipher(self, text, matrix):
        return reverse_hill(text, matrix)
