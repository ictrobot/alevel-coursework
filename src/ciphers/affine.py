from utilities import mod_inverse


def affine(text, a, b):
    """This function preforms the affine cipher on the input text and returns the output. Any characters which are not letters are left unchanged."""
    output = ""
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            output += letter
            continue
        index = chr_code - offset
        index *= a
        index += b
        chr_code = offset + (index % 26)
        output += chr(chr_code)
    return output


def reverse_affine(text, a, b):
    """ Reverse the affine function"""
    a_mod_inverse = mod_inverse(a, 26)
    if a_mod_inverse is None:
        # no mod inverse, so cannot be reversed
        raise ValueError("Cannot decrypt affine as A and 26 are not co-prime")

    output = ""
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            output += letter
            continue
        index = chr_code - offset
        index -= b
        index *= a_mod_inverse
        chr_code = offset + (index % 26)
        output += chr(chr_code)
    return output
