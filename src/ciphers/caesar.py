def caesar(text, shift):
    """This function preforms a caesar shift on the input text and returns the output. Any characters which are not letters are left unchanged."""
    output = ""
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
        index += shift
        chr_code = offset + (index % 26)
        output += chr(chr_code)
    return output
