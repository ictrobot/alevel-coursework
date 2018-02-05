import multiprocessing
import os
import queue
import random
import sys
from string import ascii_uppercase

from tqdm import tqdm

from solvers.affine import AffineSolver, POSSIBLE_VALUES_A, affine
from solvers.caesar import CaesarSolver, caesar
from solvers.scytale import ScytaleSolver, scytale
from solvers.substitution import SubstitutionSolver, substitution
from solvers.vigenere import VigenereSolver, string_to_shifts, vigenere


class SolverChecker:

    def __init__(self, name, solver_class):
        self.name = name
        self.solver_class = solver_class

    def test(self):
        """ Tests a solver """
        # print a separator
        print()
        print("=" * 80)
        # store the number of found_keys which have been the best key, in the top 10 and different
        best = 0
        top10 = 0
        different = 0
        # pool.imap_unordered(self.test_ebook, texts) runs self.text_ebook() on each text utilizing the process pool
        # this is then wrapped in tqdm to make a progress bar
        for key, ciphertext, outputs in tqdm(pool.imap_unordered(self.test_ebook, texts), total=len(texts)):
            # outputs is a list of tuples containing (output_plaintext, found_key, score)
            # check if it found the best key
            if outputs[0][1] == key:
                best += 1
                continue
            # check if the best key was in the top 10
            for output_plaintext, found_key, score in outputs[1:]:
                if found_key == key:
                    top10 += 1
                    break
            else:
                # otherwise the key was different
                different += 1
        # print the results
        print("\n{}\nBest: {}\nTop 10: {}\nDifferent: {}".format(self.name, best, top10, different))

    def test_ebook(self, text):
        """ Tests an individual book """
        # get a random key and the encrypted cipher text
        key, ciphertext = self.get_ciphertext_key(text)
        # make a new instance of the solver
        solver = self.solver_class()
        # patch the solver queue:
        # normally the solver_queue is a multiprocessing.queue() as it is communicating
        # across processes. As this is not communicating with a parent gui window
        # convert it into a normal queue
        solver.solver_queue = queue.Queue()
        # run the solver on the ciphertext
        solver.run(ciphertext)
        return key, ciphertext, solver.outputs

    def get_ciphertext_key(self, text):
        """ Get ciphertext & random key given input text. Overriden by subclasses"""
        raise NotImplementedError


class CaesarChecker(SolverChecker):
    """ Tests the Caesar Solver"""

    def __init__(self):
        super(CaesarChecker, self).__init__("Caesar", CaesarSolver)

    def get_ciphertext_key(self, text):
        shift = random.randint(0, 25)
        ciphertext = caesar(text, shift)
        return shift, ciphertext


class AffineChecker(SolverChecker):
    """ Tests the Affine Solver"""

    def __init__(self):
        super(AffineChecker, self).__init__("Affine", AffineSolver)

    def get_ciphertext_key(self, text):
        a = random.choice(POSSIBLE_VALUES_A)
        b = random.randint(0, 25)
        ciphertext = affine(text, a, b)
        return (a, b), ciphertext


class ScytaleChecker(SolverChecker):
    """ Tests the Scytale Solver"""

    def __init__(self):
        super(ScytaleChecker, self).__init__("Scytale", ScytaleSolver)

    def get_ciphertext_key(self, text):
        shift = random.randint(2, 20)
        ciphertext = scytale(text, shift)
        return shift, ciphertext


class VigenereChecker(SolverChecker):
    """ Tests the Vigenere Solver"""

    def __init__(self):
        super(VigenereChecker, self).__init__("Vigenere", VigenereSolver)

    def get_ciphertext_key(self, text):
        shift = ""
        for i in range(random.randint(2, 5)):
            shift += random.choice(ascii_uppercase)
        ciphertext = vigenere(text, string_to_shifts(shift))
        return shift, ciphertext


class SubstitutionChecker(SolverChecker):
    """ Tests the Substitution Solver"""

    def __init__(self):
        super(SubstitutionChecker, self).__init__("Substitution", SubstitutionSolver)

    def get_ciphertext_key(self, text):
        letters = list(ascii_uppercase)
        random.shuffle(letters)
        mapping = {k: v for k, v in zip(ascii_uppercase, letters)}
        inverse_mapping = {v: k for k, v in zip(ascii_uppercase, letters)}
        ciphertext = substitution(text, mapping)
        return inverse_mapping, ciphertext


def get_strings(full_path):
    """ loads a file and returns a list of 10000 long strings """
    texts = []
    with open(full_path, "r", encoding="utf-8") as f:
        letters = ""
        for letter in f.read().upper():
            if 65 <= ord(letter) <= 90:
                letters += letter
        for i in range(0, len(letters), 10000):
            string = letters[i:i + 10000]
            if len(string) == 10000:
                texts.append(string)
    return texts


if __name__ == "__main__":
    # start a thread pool
    pool = multiprocessing.Pool(processes=8)
    # directory containing the texts to test is the first command line argument
    input_dir = sys.argv[1]
    # list to store the texts
    texts = []
    # get the filenames and full paths of the files in the input_dir
    filenames = os.listdir(input_dir)
    fullpaths = [os.path.join(input_dir, filename) for filename in filenames]
    # pool.imap_unordered(get_strings, fullpaths) runs get_strings() on each full path utilizing the process pool
    # this is then wrapped in tqdm to make a progress bar
    for file_texts in tqdm(pool.imap_unordered(get_strings, fullpaths), total=len(fullpaths)):
        # add the 10000 long strings from the file into the main list
        texts += file_texts
    # log the number of strings
    print("Loaded {} strings".format(len(texts)))
    # test each solver
    CaesarChecker().test()
    ScytaleChecker().test()
    AffineChecker().test()
    SubstitutionChecker().test()
    VigenereChecker().test()
    # wait for pool to finish
    pool.close()
    pool.join()
