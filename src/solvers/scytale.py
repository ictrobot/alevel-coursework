from solvers.solver_thread import SolverThread
from ciphers.scytale import *


def factors(integer):
    """ Returns a list of factors of an integer """
    results = set()
    # only have to go up to sqrt(integer) as sqrt(integer) ** 2 == integer
    # first + 1 as int rounds down, second to make it include the previous value
    for i in range(1, int(integer ** 0.5) + 2):
        if integer % i == 0:
            results.add(i)
    return list(results)


class ScytaleSolver(SolverThread):
    """ Automatic key finder for the Scytale Cipher"""

    def __init__(self):
        super(ScytaleSolver, self).__init__("Scytale Cipher")

    def run(self, text):
        """ Run the automatic key finding """
        # number of possibilities is the number of factors of the length
        factors_list = factors(len(text))
        self.set_total_possibilities(len(factors_list))
        for factor in factors_list:
            plaintext = reverse_scytale(text, factor)
            self.possibility(factor, plaintext)
        self.done()
