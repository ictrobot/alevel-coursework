from solvers.solver_process import SolverProcess
from ciphers.affine import *


class AffineSolver(SolverProcess):
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

    def update_key_widget(self, widget, key):
        """ Called to update the key widget to display the provided key """
        # Format the key display nicely
        widget["text"] = "a={} b={}".format(*key)
