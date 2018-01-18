from string import ascii_uppercase
import numpy

from utilities import mod_inverse


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
