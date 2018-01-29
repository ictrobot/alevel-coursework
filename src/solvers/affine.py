from solvers.solver_thread import SolverThread
from ciphers.affine import *

# store all the possible values of A (where a & 26 have a modular inverse)
POSSIBLE_VALUES_A = [i for i in range(1, 25) if mod_inverse(i, 26) is not None]


class AffineSolver(SolverThread):
    """ Automatic key finder for the Affine Cipher"""

    def __init__(self):
        super(AffineSolver, self).__init__("Affine Cipher")

    def run(self, text):
        """ Run the automatic key finding """
        # simply brute force the possibilities
        self.set_total_possibilities(26 * len(POSSIBLE_VALUES_A))
        for a in POSSIBLE_VALUES_A:
            for b in range(26):
                key = (a, b)
                plaintext = reverse_affine(text, a, b)
                self.possibility(key, plaintext)
        self.done()
