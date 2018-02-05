from string import ascii_uppercase
from benchmark import benchmark

###############################################################################


def substitution(text, mapping):
    # simple loop which loops through each letter in the mapping and uses .replace()
    text = text.upper()
    for k, v in mapping.items():
        text = text.replace(k.upper(), v.lower())
    return text

###############################################################################


class DictionaryMapping:

    def __init__(self, mapping):
        self.mapping = {}
        for chr_code, letter in enumerate(ascii_uppercase, start=65):
            if letter in mapping:
                self.mapping[chr_code] = ord(mapping[letter].lower())
            else:
                self.mapping[chr_code] = ord(letter.upper())

    def __getitem__(self, i):
        if 97 <= i <= 122:
            i -= 32
        return self.mapping[i]


def substitution_translate_class_dict(text, mapping):
    # method which uses a mapping class based off a dictionary and .translate()
    return text.translate(DictionaryMapping(mapping))

###############################################################################


class ListMapping:

    def __init__(self, mapping):
        self.array = []
        for letter in ascii_uppercase:
            if letter in mapping:
                self.array.append(ord(mapping[letter].lower()))
            else:
                self.array.append(ord(letter.upper()))

    def __getitem__(self, i):
        if 65 <= i <= 90:
            return self.array[i - 65]
        if 97 <= i <= 122:
            return self.array[i - 97]
        return i


def substitution_translate_class_list(text, mapping):
    # method which uses a mapping class based off a list and .translate()
    return text.translate(ListMapping(mapping))

###############################################################################


def substitution_translate_dict(text, mapping):
    # method which makes a dictionary to represent the translation of the mapping, and uses .translate()
    x = {}
    for upper, upper_chr, lower_chr in zip(ascii_uppercase, range(65, 91), range(97, 123)):
        try:
            value = mapping[upper].lower()
            x[upper_chr] = value
            x[lower_chr] = value
        except KeyError:
            x[upper_chr] = upper
            x[lower_chr] = upper
    return text.translate(x)

###############################################################################


if __name__ == "__main__":
    # read in the sample text
    with open("sample.txt", "r") as f:
        text = f.read().strip()
    # list of the functions to test
    functions = [substitution, substitution_translate_class_dict, substitution_translate_class_list, substitution_translate_dict]
    # sample mapping to test correctness
    mapping = {'A': 'Q', 'B': 'J', 'C': 'U', 'D': 'X', 'E': 'B', 'F': 'H', 'G': 'O',
               'H': 'C', 'I': 'N', 'J': 'P', 'K': 'A', 'L': 'F', 'M': 'G', 'N': 'M',
               'O': 'T', 'P': 'Z', 'Q': 'E', 'R': 'W', 'S': 'L', 'T': 'D', 'U': 'I',
               'V': 'R', 'W': 'K', 'X': 'Y', 'Y': 'S', 'Z': 'V'}
    # test the functions
    correct = substitution(text[:1000], mapping)
    for f in functions:
        if f(text[:1000], mapping) != correct:
            print("Function {} FAILED".format(f.__name__))
            exit(1)
        else:
            print("Function {} passed".format(f.__name__))
    # benchmark the functions
    for length in (1, 10, 100, 1000, 10000, 100000):
        # get text of the right length and print header
        test_text = text[:length]
        print("\n{:,} long string".format(length))
        for f in functions:
            # benchmark each function
            benchmark(f, args=[test_text, mapping])
