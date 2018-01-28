import tkinter as tk
import queue

from solvers.solver_thread import start_solver
from utilities import TITLE_LABEL_OPTIONS, SUBTITLE_LABEL_OPTIONS
from widgets.outputtext import OutputText
from widgets.scrollframe import ScrollFrame
from widgets.progressbar import ProgressBar


class SolverWindow(tk.Frame):
    def __init__(self, application, solver, text, cipher_window):
        super(SolverWindow, self).__init__(application)
        self.application = application
        self.solver = solver
        self.cipher_window = cipher_window
        self.outputs = []
        # setup widgets
        self.create_widgets()
        # start the solver
        self.solver_thread = start_solver(self.solver, text)
        # schedule update
        self.after(1000 // 30, self.update_from_solver)

    def create_widgets(self):
        """ Setup the widgets for the solver window """
        tk.Label(self, text=self.solver.cipher_name + " - Guess Decryption Key", **TITLE_LABEL_OPTIONS).grid(row=0, column=0)
        # back button
        tk.Button(self, text="Back", command=self.go_back).grid(row=0, column=1, sticky="NE")
        # stop button
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_solver)
        self.stop_button.grid(row=3, column=1, sticky="NE")
        # progress bar
        tk.Label(self, text="Progress", **SUBTITLE_LABEL_OPTIONS).grid(row=3, column=0)
        self.progress_bar = ProgressBar(self)
        self.progress_bar.grid(row=4, column=0, sticky="NSEW")
        # set the first column to be expandable
        self.grid_columnconfigure(0, weight=1)

        # setup the output scroll frame
        tk.Label(self, text="Outputs", **SUBTITLE_LABEL_OPTIONS).grid(row=1, column=0)
        self.outputs_scroll_frame = ScrollFrame(self)
        self.outputs_scroll_frame.grid(row=2, column=0, sticky="NSEW")
        self.outputs_inner_frame = self.outputs_scroll_frame.inner_frame
        # setup headings in the output scroll frame
        tk.Label(self.outputs_inner_frame, text="Score").grid(row=0, column=0, padx=10)
        tk.Label(self.outputs_inner_frame, text="Decryption Key").grid(row=0, column=1, padx=10)
        tk.Label(self.outputs_inner_frame, text="Text").grid(row=0, column=2)

    def update_from_solver(self):
        """ Called 30 times a second on the main thread to update progress from solver thread """
        # check if the solver has been stopped
        if self.solver.solver_queue is None:
            return
        # only update the outputs once per set of messages
        outputs = None
        # only mark as done after updating outputs
        done = False
        # loop through and progress each message
        while True:
            # try and get a message
            try:
                command_name, value = self.solver.solver_queue.get_nowait()
            except queue.Empty:
                # break if there aren't any messages in the queue
                break
            # process the messages
            if command_name == "total_possibilities":
                self.progress_bar.set_total(value)
            elif command_name == "indeterminate_possibilities":
                self.progress_bar.indeterminate()
            elif command_name == "increment_progress":
                self.progress_bar.increment_progress()
            elif command_name == "done":
                done = True
            elif command_name == "outputs":
                # not called straight away to avoid updating the gui multiple times a set of messages
                outputs = value
            else:
                # raise an error
                raise ValueError("Invalid command {}".format(command_name))
        # if outputs were received, update the inner scroll window
        if outputs is not None:
            self.set_output(outputs)
        # ensures the outputs are updated before running self.done()
        if done:
            self.done()
        # schedule next update
        self.after(1000 // 30, self.update_from_solver)

    def go_back(self):
        """ Method to go back to the cipher window """
        self.stop_solver()
        self.application.show_existing(self.cipher_window)

    def stop_solver(self):
        """ Stop / wait for the solver to stop """
        if self.solver_thread is not None:
            self.solver_thread.join()
            self.solver_thread = None
            self.done()

    def done(self):
        """ Run when the Solver sends a message saying it is done """
        # mark the progress bar as done
        self.progress_bar.done()

        # hide stop button
        if self.stop_button is not None:
            self.stop_button.destroy()
            self.stop_button = None

        # show full texts in output boxes
        # Whilst the solver is running only the first 500 characters are displayed
        # of the outputs so Tkinter doesn't slow with the rapid updates
        for row, (text, key, score) in enumerate(self.outputs, start=1):
            self.outputs_inner_frame.grid_slaves(row=row, column=2)[0].set_text(text)

    def set_output(self, outputs):
        """ Update the outputs displayed in the inner scroll window """
        # outputs should be in the format:
        #   [(text, key, score), (text, key, score) ... ]
        # and sorted by score

        frame = self.outputs_inner_frame
        for i in range(len(outputs)):
            text, key, score = outputs[i]
            # limit the length of the output to 500 characters to prevent tkinter
            # from slowing down
            if len(text) > 500:
                display_text = text[:500] + "..."
            else:
                display_text = text
            # row to display output on
            row = i + 1
            if i <= len(self.outputs):
                # if this is a new row, create new blank placeholder widgets
                tk.Label(frame, text="").grid(row=row, column=0)
                self.solver.get_key_widget(frame).grid(row=row, column=1)
                OutputText(frame, wrap=tk.WORD, height=3, width=80).grid(row=row, column=2)
                self.outputs.append(None)
            # update the widgets which already exist (or were just created)
            # if the output does not match the current one
            if outputs[i] != self.outputs[i]:
                frame.grid_slaves(row=row, column=0)[0]["text"] = "{0:.3f}".format(score)
                self.solver.update_key_widget(frame.grid_slaves(row=row, column=1)[0], key)
                frame.grid_slaves(row=row, column=2)[0].set_text(display_text)
                self.outputs[i] = outputs[i]
