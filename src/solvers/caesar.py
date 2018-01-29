from solvers.solver_process import SolverProcess
from ciphers.caesar import *


class CaesarSolver(SolverProcess):
    """ Automatic key finder for the Caesar Cipher"""

    def __init__(self):
        super(CaesarSolver, self).__init__("Caesar Cipher")

    def run(self, text):
        """ Run the automatic key finding """
        # simply brute force the 26 possibilities
        self.set_total_possibilities(26)
        for i in range(26):
            self.possibility(i, caesar(text, -i))
        self.done()
