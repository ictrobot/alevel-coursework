from string import ascii_letters
from collections import defaultdict
from benchmark import benchmark

###############################################################################


def loop_plus(text):
    # simple loop which converts the text to uppercase then adds letter characters to the output string
    letters = ""
    for letter in text.upper():
        if 65 <= ord(letter) <= 90:
            letters += letter
    return letters

###############################################################################


def loop_list_join(text):
    # output is stored as a list then joined together
    letters = []
    for letter in text.upper():
        if 65 <= ord(letter) <= 90:
            letters.append(letter)
    return "".join(letters)

###############################################################################


class MappingClass:

    def __getitem__(self, chr_code):
        if 65 <= chr_code <= 90:
            return chr_code
        if 97 <= chr_code <= 122:
            return chr_code - 32
        return None


mapping_custom = MappingClass()


def string_translate_object(text):
    # uses string.translate on the custom object produced from the above class
    return text.translate(mapping_custom)

###############################################################################


# a dictionary which returns None for unknown keys
mapping_defaultdict = defaultdict(lambda: None)
for l in ascii_letters: # upper and lowercase letters
    mapping_defaultdict[ord(l)] = l.upper()


def string_translate_defaultdict(text):
    # uses string.translate the defaultdict instance
    return text.translate(mapping_defaultdict)

###############################################################################


if __name__ == "__main__":
    # read in the sample text
    with open("sample.txt", "r") as f:
        text = f.read().strip()
    # list of the functions to test
    functions = [loop_plus, loop_list_join, string_translate_object, string_translate_defaultdict]
    # test the functions
    for f in functions:
        if f("Hello World") != "HELLOWORLD" or f("This is a test.") != "THISISATEST":
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
            benchmark(f, args=[test_text])
