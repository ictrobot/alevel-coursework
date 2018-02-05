from solvers.solver_process import SolverProcess
from ciphers.vigenere import *
from ciphers.caesar import caesar
from ngrams import get_ngram_data
from string import ascii_uppercase
from utilities import letters_only_uppercase
import itertools


# cache the two gram data locally
bigram_data = get_ngram_data(2)
bigram_scores = {}
for letter1 in ascii_uppercase:
    for letter2 in ascii_uppercase:
        # store the key as a tuple to avoid having to concatenate the two letters repeatedly in the solver
        bigram_scores[letter1, letter2] = bigram_data.get_score(letter1 + letter2)


def best_n_long_key(cipher_text, reverse_caesars, key_len):
    """ Finds the best key for the ciphertext which is `key_len` long """

    # array to store the best two keys for each position
    key_possibilities = [[] for _ in range(key_len)]
    # for each position in the key
    for key_index in range(key_len):
        # store the best average score and keys
        best_average = float("inf")
        best_key1 = "A"
        best_key2 = "A"
        for key1, key2 in itertools.product(ascii_uppercase, repeat=2):
            # try every possible pair of keys
            total_score = 0
            count = 0
            # get the corresponding reverse caesar string for two keys
            string_a = reverse_caesars[key1]
            string_b = reverse_caesars[key2]
            for text_idx in range(key_index, len(cipher_text) - 1, key_len):
                # for every position which this key index would apply to the
                # ciphertext, decrypt the letters and rate the result
                letter_a = string_a[text_idx]  # use the pre-calculated reverse caesars
                letter_b = string_b[text_idx + 1]
                # used the cached local ngram data, avoid having to concatenate the letters
                total_score += bigram_scores[letter_a, letter_b]
                count += 1
            # work out the average score using the key1 key2 pair
            average = total_score / count
            if average < best_average:
                # if it is better than the previous, store it
                best_average = average
                best_key1 = key1
                best_key2 = key2
        # after trying every possible pair of keys store the best key
        # letter 1 & 2 in the relevant positions
        key_possibilities[key_index].append((best_key1, best_average))
        # if this is the last key index the second letter is actually the
        # first key index as the key is repeated
        key_index2 = (key_index + 1) % key_len
        key_possibilities[key_index2].append((best_key2, best_average))
    # make a key from the best letter from each position
    key = ""
    for letter_possibilities in key_possibilities:
        # sort the possibility by the average score
        letter_possibilities.sort(key=lambda x: x[1])
        # add the letter from the possibility with the lowest score to the key
        key += letter_possibilities[0][0]
    return key


class VigenereSolver(SolverProcess):
    """ Automatic key finder for the Vigenère Cipher """

    def __init__(self):
        super(VigenereSolver, self).__init__("Vigenère Cipher")

    def run(self, text):
        """ Run the automatic key finding """
        # strip all non letter characters
        letters_only = letters_only_uppercase(text)
        # all the possible lengths to test
        lengths = list(range(2, min(50, len(letters_only))))
        # set the number of possibilities
        self.set_total_possibilities(len(lengths))
        # pre-calculate the entire text decrypted with all the caesar shifts
        reverse_caesars = {}
        for shift, letter in enumerate(ascii_uppercase):
            reverse_caesars[letter] = caesar(letters_only, -shift)
        # store the found keys
        found_keys = set()
        # iterate over each length to check
        for length in lengths:
            # try and find the best key that is `length` long
            key = best_n_long_key(letters_only, reverse_caesars, length)
            shifts = string_to_shifts(key)
            # check if key is double an existing key
            if len(key) % 2 == 0:
                first_half = key[:len(key) // 2]
                second_half = key[len(key) // 2:]
                if first_half == second_half and first_half in found_keys:
                    # this new key is double an existing key, the solver is done
                    self.done()
                    return
            found_keys.add(key)
            self.possibility(key, reverse_vigenere(text, shifts))
        self.done()

