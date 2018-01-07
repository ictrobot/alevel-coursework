def scytale(text, columns):
    """ Preforms scytale on the input text as if there were the specified amount of columns"""
    # add padding
    while len(text) % columns != 0:
        text += "_"
    # do scytale
    output = ""
    for i in range(columns):
        output = output + text[i::columns]
    return output


def reverse_scytale(text, columns):
    """ Reverse the scytale function"""
    return scytale(text, len(text) // columns).replace("_", "")
