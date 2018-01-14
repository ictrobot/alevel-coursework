def string_to_shifts(text):
    """Converts a string representing the shifts of a Vigenère cipher into a list
    of the shifts. e.g. ABC -> [1, 2, 3] """
    shifts = []
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            shifts.append(chr_code - 65)
        elif 97 <= chr_code <= 122:
            shifts.append(chr_code - 97)
    return shifts


def vigenere(text, shifts):
    """Performs Vigenère cipher on the input text. shifts must be a list of shifts,
    which can be produced using string_to_shifts(string)"""

    if len(shifts) == 0:
        raise ValueError("Must be at least one shift")

    output = ""
    # the index of the next shift to use
    shift_index = 0
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            # upper case letters
            offset = 65
        elif 97 <= chr_code <= 122:
            # lower case letters
            offset = 97
        else:
            # leave other characters untouched
            output += letter
            continue
        index = chr_code - offset
        index += shifts[shift_index]
        chr_code = offset + (index % 26)
        output += chr(chr_code)
        # update the shift for the next letter
        shift_index = (shift_index + 1) % len(shifts)
    return output


def reverse_vigenere(text, shifts):
    """Reverses the Vigenère cipher by making all the shifts negative."""
    return vigenere(text, [-shift for shift in shifts])
