import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# https://stackoverflow.com/questions/68555249/display-tkinter-scale-value-realtime
class ScaleDisplay(ttk.Scale):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.lbl = ttk.Label(parent, textvariable= kwargs["variable"] )
        self.lbl.pack(side='bottom')

        # self.bind('<Configure>', lambda ev: self.after(1, self.update_lbl))

    def update_lbl(self, *args):
        x, _ = self.coords()  # gets handle x position
        y, h = self.winfo_y(), self.winfo_height() # get the widgets y position and height
        self.lbl.place(x=x, y=h+y)
