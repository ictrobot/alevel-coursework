import tkinter as tk
from tkinter import ttk
import time


class ProgressBar(tk.Frame):
    """ ProgressBar which has progress and eta labels as well as useful methods."""

    def __init__(self, master):
        super(ProgressBar, self).__init__(master)
        # progress label
        self.progress_label = tk.Label(self, text="")
        self.progress_label.grid(column=0, row=0, sticky="SW")
        # eta label
        self.eta_label = tk.Label(self, text="")
        self.eta_label.grid(column=2, row=0, sticky="SE")
        # setup the actual progress bar from ttk
        self.progressbar_var = tk.DoubleVar(self)
        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', variable=self.progressbar_var)
        self.progressbar.grid(column=0, row=1, columnspan=3, sticky="SEW")
        # expand the middle column without either label in
        self.columnconfigure(1, weight=1)

        # state variables
        self.is_indeterminate = False
        self.num_progress = 0
        self.num_total = 1
        self.start_time = time.time()

    def update_labels(self):
        """ Updates the text in the Progress & ETA Labels """
        if self.is_indeterminate:
            # Task progress is unknown
            self.progress_label["text"] = ""
            self.eta_label["text"] = ""
        else:
            # Update the actual progress bar
            self.progressbar_var.set((self.num_progress / self.num_total) * 100)
            # Update the progress label
            self.progress_label["text"] = "{} out of {}".format(self.num_progress, self.num_total)
            # Update the eta label
            if self.num_progress >= self.num_total:
                # already complete
                self.eta_label["text"] = "Done"
            elif self.num_progress > 0:
                # calculate the remaining time
                items_remaining = self.num_total - self.num_progress
                delta_time = time.time() - self.start_time
                time_per_item = delta_time / self.num_progress
                time_remaining = time_per_item * items_remaining
                seconds_remaining = int(round(time_remaining))
                self.eta_label["text"] = "{} seconds remaining".format(seconds_remaining)
            else:
                # cannot display eta until at least one item completes
                self.eta_label["text"] = ""

    def set_total(self, n):
        """ Set the total for the progress bar """
        self.num_total = n
        if self.is_indeterminate:
            # change mode if the progress bar was indeterminate
            self.is_indeterminate = False
            self.progressbar.configure(mode="determinate")
            self.progressbar.stop()
        # update the labels
        self.update_labels()

    def increment_progress(self, n=1):
        """ Increment the progress bar by n (default 1) """
        self.num_progress += n
        # update the labels
        self.update_labels()

    def done(self):
        """ Mark the progress bar as done """
        if self.num_progress <= 0:
            # if zero items have been completed, set to 1 completed to avoid
            # dividing by zero
            self.num_progress = 1
        # update the labels
        self.set_total(self.num_progress)

    def indeterminate(self):
        """ Mark the progress bar as having an indeterminate total """
        if not self.is_indeterminate:
            # change mode to indeterminate
            self.is_indeterminate = True
            self.progressbar.configure(mode="indeterminate")
            self.progressbar.start()
            self.update_labels()


