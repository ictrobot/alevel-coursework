from solvers.solver_process import SolverProcess
from ciphers.substitution import *
from ngrams import *


def get_starting_mapping(text):
    """ Returns a starting mapping based off letter frequencies. """
    # get letter frequencies from the text
    text_frequencies = {letter: 0 for letter in ascii_uppercase}
    total_frequency = 0
    for letter in text.upper():
        if letter in ascii_uppercase:
            text_frequencies[letter] += 1
            total_frequency += 1
    # convert the frequencies to a list so it can be ordered
    text_frequencies = [(letter, freq) for letter, freq in text_frequencies.items()]
    # sort so most common letters are first
    text_frequencies.sort(key=lambda x: x[1], reverse=True)
    # get the real frequencies and sort most common first
    letter_data = get_ngram_data(n=1)
    real_frequencies = [(letter, letter_data.get_score(letter)) for letter in ascii_uppercase]
    real_frequencies.sort(key=lambda x: x[1])
    # map most common letter in the text to most common letter,
    # 2nd most common letter in the text to 2nd most common letter, etc
    mapping = {}
    for (real_letter, score), (text_letter, freq) in zip(real_frequencies, text_frequencies):
        mapping[text_letter] = real_letter
    # convert to mapping list & return
    return mapping


class SubstitutionSolver(SolverProcess):
    """ Automatic key finder for the Substitution Cipher"""

    def __init__(self):
        super(SubstitutionSolver, self).__init__("Substitution Cipher")

    def try_swapping(self, text, mapping, score):
        """ Tries to improve the mapping by swapping two letters"""
        for letter1 in ascii_uppercase:
            for letter2 in ascii_uppercase:
                # only try to swap with letters after letter1
                if letter2 <= letter1:
                    continue
                # copy the mapping, swapping the values
                new_mapping = mapping.copy()
                new_mapping[letter1], new_mapping[letter2] = new_mapping[letter2], new_mapping[letter1]
                # rate the output using the new mapping
                new_score = rate(substitution(text, new_mapping))
                if new_score < score:
                    # if the new mapping is better, return it
                    return new_mapping, new_score
        # no better mapping found by swapping
        return None, None

    def run(self, text):
        """ Run the automatic key finding """
        # total number of tries needed is unknown
        self.set_indeterminate_possibilities()
        # get a starting mapping based off letter frequencies
        best_mapping = get_starting_mapping(text)
        # rate the starting mapping
        best_score = rate(substitution(text, best_mapping))

        # try up to 10000 times randomly shuffling the key, then swapping letters
        for repeat in range(10000):
            for i in range(5000):
                # try swapping pairs of letters up to 5000 times to improve the mapping
                self.possibility(best_mapping, substitution(text, best_mapping))
                new_mapping, new_score = self.try_swapping(text, best_mapping, best_score)
                if new_mapping is None:
                    # if the mapping could not be improved
                    if best_score < 0.25:
                        # if the mapping scores less than 0.25, assume it is
                        # the answer and stop
                        self.done()
                        return
                    else:
                        # otherwise stop trying to swap this key
                        break
                best_mapping = new_mapping
                best_score = new_score

            # as the key cannot be improved by swapping, try randomly shuffling
            values = list(best_mapping.values())
            random.shuffle(values)
            best_mapping = {key: value for key, value in zip(best_mapping.keys(), values)}
            best_score = rate(substitution(text, best_mapping))

        # no mapping found with score less than 0.25
        self.done()

    def update_key_widget(self, widget, mapping):
        """ Called to update the key widget to display the provided mapping """
        widget["text"] = "".join(mapping[l] for l in ascii_uppercase)
