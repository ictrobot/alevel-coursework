from string import ascii_letters

from benchmark import benchmark


###############################################################################

def caesar(text, shift):
    # Normal caesar function
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
        index = (chr_code - offset + shift) % 26
        output += chr(offset + index)
    return output


###############################################################################

def caesar_list(text, shift):
    # Uses a list which is made into a string at the end
    output = []
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            output.append(letter)
            continue
        index = (chr_code - offset + shift) % 26
        output.append(chr(offset + index))
    return "".join(output)


###############################################################################

def caesar_chr_code_list(text, shift):
    # stores characters codes which are converted into a string at the end
    output = []
    for letter in text:
        chr_code = ord(letter)
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            output.append(chr_code)
            continue
        index = (chr_code - offset + shift) % 26
        output.append(offset + index)
    return "".join(map(chr, output))


###############################################################################

def caesar_chr_code_inplace_list(text, shift):
    # converts the input into a list of character codes, which is modified in place and then converted to a string
    chr_code_list = list(map(ord, text))
    for i, chr_code in enumerate(chr_code_list):
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            continue
        index = (chr_code - offset + shift) % 26
        chr_code_list[i] = offset + index
    return "".join(map(chr, chr_code_list))


###############################################################################

def caesar_translate_embedded_class(text, shift):
    # uses the string.translate function
    class Mapping:
        def __getitem__(self, chr_code):
            if 65 <= chr_code <= 90:
                offset = 65
            elif 97 <= chr_code <= 122:
                offset = 97
            else:
                return chr_code
            index = (chr_code - offset + shift) % 26
            return offset + index

    return text.translate(Mapping())


###############################################################################


class IndependentMappingClass:

    def __init__(self, shift):
        self.shift = shift

    def __getitem__(self, chr_code):
        if 65 <= chr_code <= 90:
            offset = 65
        elif 97 <= chr_code <= 122:
            offset = 97
        else:
            return chr_code
        index = (chr_code - offset + self.shift) % 26
        return offset + index


def caesar_translate_independent_class(text, shift):
    # split the class out of the function
    return text.translate(IndependentMappingClass(shift))


###############################################################################

# pre-calculate the translations tables, store as dictionaries
TRANSLATIONS = {shift: {ord(letter): caesar(letter, shift) for letter in ascii_letters} for shift in range(0, 26)}


def caesar_translate_precalculated_dict(text, shift):
    # lookup the translation table
    return text.translate(TRANSLATIONS[shift % 26])

##############################################################################


if __name__ == "__main__":
    # read in the sample text
    with open("sample.txt", "r") as f:
        text = f.read().strip()
    # list of the functions to test
    functions = [caesar, caesar_list, caesar_chr_code_list, caesar_chr_code_inplace_list, caesar_translate_embedded_class, caesar_translate_independent_class, caesar_translate_precalculated_dict]
    # test the functions
    correct = caesar(text[:100], 15)
    for f in functions:
        if f(text[:100], 15) != correct:
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
            benchmark(f, n=1000, args=[test_text, 5])
