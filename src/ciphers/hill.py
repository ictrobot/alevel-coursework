import tkinter as tk
from string import ascii_uppercase

import numpy

from cipher_window import CipherWindow
from utilities import mod_inverse
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
        # setup matrixentry for the actual matrix
        self.matrix_input = MatrixEntry(frame, self.current_order, self.current_order, callback=self.update_output)
        self.matrix_input.grid(row=0, column=1, sticky="NE")

        return frame


class HillEncrypt(HillCipher):
    """Hill Encryption Cipher Window"""

    def __init__(self, application):
        super(HillEncrypt, self).__init__(application, "Encrypt")

    def run_cipher(self, text, matrix):
        return hill(text, matrix)


class HillDecrypt(HillCipher):
    """Hill Decryption Cipher Window"""

    def __init__(self, application):
        super(HillDecrypt, self).__init__(application, "Decrypt")

    def run_cipher(self, text, matrix):
        return reverse_hill(text, matrix)
