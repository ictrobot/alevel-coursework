import ngrams
import time
import multiprocessing
import tkinter as tk


def start_solver(solver, text):
    """ Start the solver thread """
    process = multiprocessing.Process(target=run_solver, args=(solver, text), name="Solver", daemon=True)
    process.start()
    return process


def run_solver(solver, text):
    """ Entry point for solver thread """
    # store the start time
    start_time = time.time()
    # actually run the solver on the text
    solver.run(text)
    # log the time taken
    time_taken = time.time() - start_time
    print("Took {:.2f} seconds to solve".format(time_taken))


class SolverThread:

    def __init__(self, cipher_name):
        self.cipher_name = cipher_name
        self.outputs = []
        # Queue used to send messages to the solver window
        # Each message should be a tuple of (command_name, command_args)
        # Valid commands names          Valid args
        # total_possibilities           the total number of possibilities (int)
        # indeterminate_possibilities   none
        # increment_progress            none
        # outputs                       [(text, key, score), (text, key, score)...]
        self.solver_queue = multiprocessing.Queue()

    def set_total_possibilities(self, n):
        """ Set the total number of possibilities """
        self.solver_queue.put(("total_possibilities", n))

    def set_indeterminate_possibilities(self):
        """ Set as indeterminate """
        self.solver_queue.put(("indeterminate_possibilities", None))

    def possibility(self, key, output_text):
        """ Each new possibility should be passed to this method. """
        # increment the progress
        self.solver_queue.put(("increment_progress", None))
        # calculate the score using 4Grams if the message is at least 4 long
        # otherwise use ngrams where n is the length of the message
        score = ngrams.rate(output_text, min(4, len(output_text)))
        # if there are less than 10 outputs or the score is better than the
        # worst score stored, update the scores
        if len(self.outputs) < 10 or self.outputs[-1][2] > score:
            # add the new (text, key, score) tuple
            self.outputs.append((output_text, key, score))
            self.outputs.sort(key=lambda x: x[2])
            self.outputs = self.outputs[:10]
            # send it to the solver window
            self.solver_queue.put(("outputs", self.outputs[::]))

    def done(self):
        """ Set as done """
        self.solver_queue.put(("done", None))

    # The below methods are designed to be overridden by solver implementations

    def run(self, text):
        """ Run the solver """
        raise NotImplementedError

    def get_key_widget(self, master):
        """ Called to create a blank key widget for the Solver Window """
        return tk.Label(master)

    def update_key_widget(self, widget, key):
        """ Called to update the key widget to display the provided key """
        widget["text"] = str(key)
