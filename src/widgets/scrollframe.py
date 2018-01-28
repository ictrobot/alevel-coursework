import tkinter as tk


class ScrollFrame(tk.Frame):
    """ A frame which can be scrolled vertically and adapts it's width to the inner frame's width """

    def __init__(self, master, *args, **kwargs):
        super(ScrollFrame, self).__init__(master, *args, **kwargs)
        # create scrollbar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="NS")
        # create a canvas, setting the scroll command to be the scrollbar
        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(column=0, row=0, sticky="NSEW")
        self.columnconfigure(0, weight=1)
        # set the scrollbar to scroll the canvas
        self.scrollbar.config(command=self.canvas.yview)
        # setup the inner frame
        self.inner_frame = tk.Frame(self.canvas, bd=2, relief=tk.SUNKEN)
        # setup the frame rendering to the canvas
        self.canvas.create_window(0, 0, window=self.inner_frame, anchor="nw")
        # when the inside window updates or the parent window updates, update the scroll view
        self.canvas.bind("<Configure>", self.update_canvas)
        self.inner_frame.bind("<Configure>", self.update_canvas)

    def update_canvas(self, event=None):
        """ Update the scroll region and width of the canvas"""
        # update the scroll bounding box
        bbox = self.canvas.bbox('all')
        self.canvas.config(scrollregion=bbox)
        # set the width of the canvas to be the width of the inner window
        self.canvas["width"] = bbox[2] - bbox[0]
