import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.ui.VScrollFrame import VScrollFrame

from src.ui.ConfigVar import ConfigVar
from src.ui.ScaleDisplay import ScaleDisplay

from src.config import config
from src.anim.FaceAnimator import face_animator

FRAME_TITLE = "Puppet"

class FramePuppet(VScrollFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.create_calibration()
        self.create_automation()

        master.add(self, text=FRAME_TITLE)

    def create_calibration(self):
        frm_calib = ttk.Labelframe(self.interior, text="Calibration")
        frm_calib.pack(fill=X, expand=YES, padx=12, pady=12)

        btn_neutral_face = ttk.Button(frm_calib, text="Set Neutral Face")
        btn_neutral_face.bind("<Button-1>", face_animator.set_neutral_face)
        btn_neutral_face.bind("<Button-3>", face_animator.clear_neutral_face)
        btn_neutral_face.pack(fill=X, expand=YES, padx=6, pady=6)

        var_elastic  = ConfigVar(bool, ('Calibration', 'use_elastic_max'))
        var_use_head = ConfigVar(bool, ('Calibration', 'use_head_rotation'))

        chk_elastic = ttk.Checkbutton(frm_calib, text="Use Elastic Calibration Scaling (experimental)", variable=var_elastic.tk_var)
        chk_elastic.config(command=self.click_elastic)
        chk_elastic.pack(fill=X, expand=YES, padx=6, pady=0)

        chk_head_rotation = ttk.Checkbutton(frm_calib, text="Use Face Rotation", variable=var_use_head.tk_var)
        chk_head_rotation.pack(fill=X, expand=YES, padx=6, pady=6)

    def create_automation(self):
        frm_auto = ttk.Labelframe(self.interior, text="Animation")
        frm_auto.pack(fill=X, expand=YES, padx=12, pady=12)

        var_recover_on     = ConfigVar(bool,  ('Animation',  'recovery_on'))
        var_recover_time   = ConfigVar(float, ('Animation',  'recovery_time'))
        var_autoblink_on   = ConfigVar(bool,  ('Animation', 'auto_blink_on'))
        var_autoblink_rate = ConfigVar(float, ('Animation', 'auto_blink_rate'))

        chk_recover_on = ttk.Checkbutton(frm_auto, text="Return to Neutral (Time)", variable=var_recover_on.tk_var)
        chk_recover_on.pack(fill=X, expand=YES, padx=6, pady=6)

        scl_recover_time =ttk.Scale(frm_auto, variable=var_recover_time.tk_var, from_=0.1, to=2.0)
        scl_recover_time.pack(fill=X, expand=YES, padx=12, pady=6)

        chk_autoblink_on = ttk.Checkbutton(frm_auto, text="Auto-Blink (rate)", variable=var_autoblink_on.tk_var)
        chk_autoblink_on.pack(fill=X, expand=YES, padx=6, pady=6)

        scl_autoblink_rate = ttk.Scale(frm_auto, variable=var_autoblink_rate.tk_var, from_=30, to=600)
        scl_autoblink_rate.pack(fill=X, expand=YES, padx=12, pady=6)

    def click_elastic(self):
        if config["Calibration"].getboolean('use_elastic_max'):
            face_animator.init_elastic_max()
        else:
            face_animator.clear_elastic_max()