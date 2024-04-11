import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.ui.VScrollFrame import VScrollFrame

from src.ui.ConfigVar import ConfigVar

import re

FRAME_TITLE = "Network"

class FrameNetwork(VScrollFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        frm_face = ttk.Labelframe(self.interior, text="Live Link Face")
        frm_face.pack(fill=X, expand=YES, padx=12, pady=12)
        frm_face.grid_columnconfigure(1, weight=6)

        vIP   = (self.register(self.validate_IP))
        vPort = (self.register(self.validate_digit))

        var_face_send = ConfigVar(bool, ('LiveLinkFace', 'send'), fallback=True)
        var_face_ip   = ConfigVar(str, ('LiveLinkFace', 'ip'), fallback="127.0.0.1")
        var_face_port = ConfigVar(str, ('LiveLinkFace', 'port'), fallback="11111")

        chk_face_on = ttk.Checkbutton(frm_face, text="Output Live Link Face", variable=var_face_send.tk_var)
        chk_face_on.grid(column=0, row=0, padx=6, pady=6, columnspan=2)

        lbl1 = ttk.Label(frm_face, text= 'IP:')
        lbl1.grid(column=0, row=1, padx=6, pady=6,sticky="nesw")
        txt1 = ttk.Entry(frm_face, textvariable= var_face_ip.tk_var, 
                              validate='all',
                              validatecommand=(vIP, '%P'))
        txt1.grid(column=1, row=1, padx=6, pady=6,sticky="nesw")

        lbl2 = ttk.Label(frm_face, text="Port:")
        lbl2.grid(column=0, row=2, padx=6, pady=6,sticky="nesw")
        txt2 = ttk.Entry(frm_face, textvariable= var_face_port.tk_var,
                              validate='all',
                              validatecommand=(vPort, '%P'))
        txt2.grid(column=1, row=2, padx=6, pady=6,sticky="nesw")
        
        master.add(self, text=FRAME_TITLE)
    
    def validate_digit(self, P):
        return True if (str.isdigit(P) or P == "") else False
    
    def validate_IP(self, P):
        return True if (re.match('[0-9.]+$', P) or P == "") else False
        # return True if (str.isdigit(P) or P == "" or P == ".") else False