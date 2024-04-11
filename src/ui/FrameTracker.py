import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.ui.VScrollFrame import VScrollFrame

import re
from src.cross_platform import get_camera_device_names, get_camera_device_formats
import sys

from src.config import config
from src.ui.ConfigVar import ConfigVar

FRAME_TITLE = "Tracker"

DEVICE_NAMES = get_camera_device_names()

# Format Options
DEVICE_NAMES = [ (str(i) + ": " + x) for i, x in enumerate(DEVICE_NAMES)]
DEVICE_NAMES = [ DEVICE_NAMES[0] ] + DEVICE_NAMES

class FrameTracker(VScrollFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=X, expand=NO)

        self.source_input_value = ttk.StringVar(value=config["Camera"].getint("input_source"))
        opt_source = ttk.OptionMenu(self.interior, self.source_input_value, *DEVICE_NAMES, command=self.opt_source_change ) 
        opt_source.pack(fill=X, expand=YES, padx=12, pady=12 )

        """
            Tunrs out this is kind of tricky to make work properly.
            TODO: (idea) make static list with a few common resolutions and the option to add/rem resolutions to the list.
        res = get_camera_device_formats(config["Camera"].getint("input_source"))
        self.RESOLUTIONS_INFO = res[0]
        self.RESOLUTIONS_TEXT = res[1]
        self.source_res_value = ttk.StringVar()
        self.opt_source_res = ttk.OptionMenu(self.interior, self.source_res_value, *self.RESOLUTIONS_TEXT, command=self.opt_source_res_change)
        self.opt_source_res.pack(fill=X, expand=YES, padx=12, pady=12)
        """

        self.create_camera_resolution()
        self.create_frame_camera_options()
        self.create_frame_filters()

        master.add(self, text=FRAME_TITLE)

    def create_camera_resolution(self):
        frm_format = ttk.Labelframe(self.interior, text="Camera Resolution")
        frm_format.pack(fill=X, expand=YES, padx=12, pady=0)
        frm_format.grid_columnconfigure(0, weight=1)
        frm_format.grid_columnconfigure(1, weight=1)
        frm_format.grid_columnconfigure(2, weight=1)

        # on grids: https://www.pythontutorial.net/tkinter/tkinter-grid/

        ttk.Label(frm_format, text="Width:" ).grid(column=0, row=0)
        ttk.Label(frm_format, text="Height:").grid(column=1, row=0)
        ttk.Label(frm_format, text="FPS:"   ).grid(column=2, row=0)

        self.ety_height_value = ConfigVar(str, ("Camera", "height"), fallback="0")
        self.ety_width_value  = ConfigVar(str, ("Camera", "width"),  fallback="0")
        self.ety_fps_value    = ConfigVar(str, ("Camera", "fps"),    fallback="0")

        vcmd = (self.register(self.validate_digit))
        ety_height = ttk.Entry(frm_format, width=8, justify="center", 
                               textvariable=self.ety_height_value.tk_var,
                               validate='all',
                               validatecommand=(vcmd, '%P'))
        ety_height.grid(column=0, row=1, sticky="we", padx=6, pady=6)
        ety_width = ttk.Entry(frm_format, width=8, justify="center", 
                              textvariable=self.ety_width_value.tk_var,
                              validate='all',
                              validatecommand=(vcmd, '%P'))
        ety_width.grid(column=1, row=1, sticky="we")
        ety_fps = ttk.Entry(frm_format, width=8, justify="center", 
                            textvariable=self.ety_fps_value.tk_var, 
                            validate='all',
                            validatecommand=(vcmd, '%P'))
        ety_fps.grid(column=2, row=1, sticky="we", padx=6, pady=6)

    def create_frame_camera_options(self):
        frm_options = ttk.Labelframe(self.interior, text="Camera Options")
        frm_options.pack(fill=X, expand=YES, padx=12, pady=12)

        frm_row1 = ttk.Frame(frm_options)
        frm_row1.pack(fill=X, expand=YES, padx=6, pady=6)

        self.chk_mirror_value = ConfigVar(bool, ("CameraOptions", "mirror_camera"))
        self.chk_flip_value   = ConfigVar(bool, ('CameraOptions', 'flip_camera'))
        self.chk_rotate_value = ConfigVar(bool, ('CameraOptions', 'rotate_camera'))

        chk_mirror = ttk.Checkbutton(frm_row1, text='Mirror', variable=self.chk_mirror_value.tk_var).pack(side=LEFT, expand=YES)
        chk_flip   = ttk.Checkbutton(frm_row1, text='Flip',   variable=self.chk_flip_value.tk_var  ).pack(side=LEFT, expand=YES)
        chk_rotate = ttk.Checkbutton(frm_row1, text='Rotate', variable=self.chk_rotate_value.tk_var).pack(side=LEFT, expand=YES)
        
        frm_row2 = ttk.Frame(frm_options)
        frm_row2.pack(fill=X, expand=YES, padx=6, pady=6)

        self.chk_cam_value  = ConfigVar(bool, ("CameraOptions", "preview_camera"))
        self.chk_wire_value = ConfigVar(bool, ("CameraOptions", "preview_wireframe"))

        chk_cam  = ttk.Checkbutton(frm_row2, text='Show camera',    variable=self.chk_cam_value.tk_var ).pack(side=LEFT, expand=YES)
        chk_wire = ttk.Checkbutton(frm_row2, text='Show wireframe', variable=self.chk_wire_value.tk_var).pack(side=LEFT, expand=YES)

    def create_frame_filters(self):
        frm_filters = ttk.Labelframe(self.interior, text="Filters")
        frm_filters.pack(fill=X, expand=YES, padx=12, pady=0)

        self.chk_noise_bool   = ConfigVar(bool,  ('CameraFilters', 'jitter_removal_on'))
        self.scl_noise_value  = ConfigVar(float, ('CameraFilters', 'jitter_removal_threshold'))
        self.chk_smooth_bool  = ConfigVar(bool,  ('CameraFilters', 'frame_smoothing_on'))
        self.scl_smooth_value = ConfigVar(float, ('CameraFilters', 'frame_smoothing_amount'))

        chk_noise  = ttk.Checkbutton(frm_filters, text="Jitter Removal (threshold)", variable=self.chk_noise_bool.tk_var)
        chk_noise.pack(fill=X, expand=YES, padx=6, pady=6)
        scl_noise  = ttk.Scale(frm_filters, variable=self.scl_noise_value.tk_var, from_=0.5, to=3)
        scl_noise.pack(fill=X, expand=YES, padx=12, pady=6)

        chk_smooth = ttk.Checkbutton(frm_filters, text="Motion Smoothing (time)", variable=self.chk_smooth_bool.tk_var)
        chk_smooth.pack(fill=X, expand=YES, padx=6, pady=0)
        scl_smooth = ttk.Scale(frm_filters, variable=self.scl_smooth_value.tk_var, from_=1, to=8)
        scl_smooth.pack(fill=X, expand=YES, padx=12, pady=6)

    def opt_source_change(self, option_str):
        config["Camera"]["input_source"] = option_str.split(":")[0]
        """
            TODO: probably just remove this
        res = get_camera_device_formats(config["Camera"].getint("input_source"))
        self.RESOLUTIONS_INFO = res[0]
        self.RESOLUTIONS_TEXT = res[1]
        """
    
    def opt_source_res_change(self, option_str):
        # TODO: implement this when I have a good solution
        print(option_str)
        pass

    def validate_digit(self, P):
        return True if (str.isdigit(P) or P == "") else False