import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.ui.VScrollFrame import VScrollFrame

import re
import numpy as np
from src.anim.FaceAnimator import face_animator
from src.network.ARkit import FACE_BLENDSHAPE_NAMES

FRAME_TITLE = "Monitor"

class FrameMonitor(VScrollFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.pack()

        self.clicked_idx = 0

        self.create_canvas_blendshapes(app)

        master.add(self, text=FRAME_TITLE)

    def create_canvas_blendshapes(self, app):
        self.cvs_monitor = ttk.Canvas(self.interior, height=(len(FACE_BLENDSHAPE_NAMES)*34))
        self.cvs_monitor.bind("<Button>",    self.click_callback)
        self.cvs_monitor.bind("<B1-Motion>", self.drag_callback)
        self.cvs_monitor.pack(fill=X, expand=TRUE)

        self.update()

        #print(self.cvs_monitor.winfo_width())
        self.bar_width = self.cvs_monitor.winfo_width() - (33)
        self.bar_height = 32 # +2 spacing

        self.rects_blendshapes = []
        self.names_blendshapes = []
        self.texts_blendshapes = []

        for i, blendshape in enumerate(FACE_BLENDSHAPE_NAMES):
            name_str = re.sub(r"(\w)([A-Z])", r"\1 \2", blendshape)
            name_str = name_str.title()
            y = (self.bar_height+2)*i
            rect  = self.cvs_monitor.create_rectangle(0, y, self.bar_width, y+self.bar_height, fill='gray')
            self.rects_blendshapes.append(rect)
            name  = self.cvs_monitor.create_text(12, y+(self.bar_height/2), anchor="w", fill="white", text=name_str)
            value = self.cvs_monitor.create_text(self.bar_width-12, y+(self.bar_height/2), anchor="e", fill="white", text="0.0")
            self.names_blendshapes.append(name)
            self.texts_blendshapes.append(value)

    def update_blendshapes(self, window):
        bar_width = self.bar_width
        bar_height = self.bar_height
        halfbar = bar_width / 2.
        for i, val in enumerate(face_animator.np_out):
            y = (bar_height+2)*i

            # Animate bars
            if i < 52:
                self.cvs_monitor.coords(self.rects_blendshapes[i], 0, y, val*bar_width, y+bar_height)
                self.cvs_monitor.itemconfig(self.texts_blendshapes[i], text=str(val))
            elif i >= 52:
                x = min(halfbar, halfbar+(val*halfbar))
                self.cvs_monitor.coords(self.rects_blendshapes[i], x, y, x+ (abs(val)*halfbar), y+bar_height)
                self.cvs_monitor.itemconfig(self.texts_blendshapes[i], text=str(val))

    def click_val(self, x):
        if self.clicked_idx < 52: # (0 to 1)
            return max(0, min(1, x / self.bar_width))
        else: # (-1 to 1)
            return max(-1, min(1, (x / self.bar_width) * 2 - 1 ))

    def click_callback(self, event):
        self.clicked_idx = int(event.y / 34)
        val = self.click_val(event.x)
        if event.num == 1:
            # Blue bar
            self.cvs_monitor.itemconfig(self.rects_blendshapes[self.clicked_idx], fill='#375a7f')
            self.cvs_monitor.itemconfig(self.names_blendshapes[self.clicked_idx], fill='#CCC')
            self.cvs_monitor.itemconfig(self.texts_blendshapes[self.clicked_idx], fill='#CCC')
            face_animator.np_freeze[self.clicked_idx] = val
        else:
            # Gray bar
            self.cvs_monitor.itemconfig(self.rects_blendshapes[self.clicked_idx], fill='gray')
            self.cvs_monitor.itemconfig(self.names_blendshapes[self.clicked_idx], fill='white')
            self.cvs_monitor.itemconfig(self.texts_blendshapes[self.clicked_idx], fill='white')
            face_animator.np_freeze[self.clicked_idx] = np.nan

    def drag_callback(self, event):
        val = self.click_val(event.x)
        face_animator.np_freeze[self.clicked_idx] = val
