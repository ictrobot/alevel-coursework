import tkinter as tk


# Adapted from:
# https://github.com/python/cpython/blob/master/Lib/idlelib/tooltip.py
class Tooltip:

    def __init__(self, widget, text, delay=500):
        """Make a new tooltip which displays the text after delay milliseconds"""
        self.widget = widget
        self.text = text
        self.delay = delay

        # Store the IDs returned by bind so the tooltip can be removed later
        self.bindid_enter = self.widget.bind("<Enter>", self.enter)
        self.bindid_leave = self.widget.bind("<Leave>", self.leave)
        # Delay callback ID, used to cancel the callback if the mouse leaves
        # the widget before the callback happens
        self.callback_id = None
        # The actual tooltip window, used to destroy it after it is created
        self.tooltip_window = None

    def enter(self, event):
        """On mouse over this widget, cancel any existing callback and ask for
        a new callback after delay milliseconds """

        self.cancel_callback()
        self.callback_id = self.widget.after(self.delay, self.show_tooltip)

    def leave(self, event):
        """When the mouse leaves the widget, cancel any existing callback and
        destroy the tooltip if it exists"""
        self.cancel_callback()
        self.hide_tooltip()

    def cancel_callback(self):
        """Cancels any existing callbacks"""
        if self.callback_id:
            self.widget.after_cancel(self.callback_id)
        self.callback_id = None

    def show_tooltip(self):
        """Displays the tooltip, called from the callback setup by enter()"""
        # Callback has happened, no need to store callback id anymore
        self.callback_id = None
        if self.tooltip_window:
            return
        # Get the coordinates of the widget on the screen
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        # Make a new window to draw the tooltip in
        self.tooltip_window = tk.Toplevel(self.widget)
        # Stops the window frame including minimize, maximize and exit buttons
        # from being created for the tooltip window
        self.tooltip_window.wm_overrideredirect(True)
        # Set the tooltip position
        self.tooltip_window.wm_geometry("+%d+%d" % (x, y))

        # Add the label to display the text in the tooltip window
        label = tk.Label(self.tooltip_window, text=self.text, justify="left", background="#ffffff", relief="solid", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self):
        """Destroys the tooltip window if it exists"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

    def remove(self):
        """Removes the tooltip from the widget. After calling this, this
        tooltip instance is useless"""

        # unbind methods so they stop getting called
        self.widget.unbind("<Enter>", self.bindid_enter)
        self.widget.unbind("<Leave>", self.bindid_leave)

        self.cancel_callback()  # cancels any existing callbacks
        self.hide_tooltip()  # destroy existing tooltip window if one exists
