from string import ascii_uppercase


def keyword_mapping(keyword):
    """Generates the substitution mapping from a keyword"""
    # letters to be used as the keys
    input_letters = list(ascii_uppercase)
    # remaining letters to be mapped
    mapping_letters = list(ascii_uppercase)
    mapping = {}
    for letter in keyword.upper():
        if letter in mapping_letters:
            # if the letter hasn't already been mapped, map the next input
            # letter to it, and remove it from the letters to map
            mapping[input_letters.pop(0)] = letter
            mapping_letters.remove(letter)
    # map the remaining letters
    for letter in mapping_letters:
        mapping[input_letters.pop(0)] = letter
    return mapping
