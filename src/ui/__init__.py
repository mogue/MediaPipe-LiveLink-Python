# import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Emoji

from src.cross_platform import dark_title_bar
from src.config import config, save_config

from src.ui.EventThread import ui_bg_thread
from src.mpipe import camera_bg_thread
from src.network import network_bg_thread

# root = ttk.Tk()
# style = ttk.Style("darkly")
# style = ttk.Style()
# print( style.theme_names() )
# print( style.theme_use() )
# style.theme_use('xpnative')

app = ttk.Window(
    title=config["Application"].get('name'),
    themename=config["Application"].get('theme'),
    resizable=(False, True)
)#    size=(360, 480),
# app.overrideredirect(True) # turns off title bar, geometry
dark_title_bar(app)
app.geometry("360x480+200+200")

def run_toggle():
    camera_bg_thread.toggle()
network_bg_thread.toggle()

ttk.Style().configure('success.TButton', font="-size 24")
ttk.Style().configure('danger.TButton', font="-size 24")
btn_start = ttk.Button(
    app, text=Emoji.get('black right-pointing triangle'),
    command = run_toggle,
    bootstyle = "success"
)
# btn_start.configure(font=('', 24))
btn_start.pack(fill=X, expand=NO, padx=12, pady=12)
camera_bg_thread.ui_camera_button_delegate = btn_start


lbl_status = ttk.Label(app, text="Press play to start tracking.")
lbl_status.pack()

lbl_padder = ttk.Label(app).pack(fill=X, expand=NO, pady=3)

"""
    Submenu Tabs: Tracker, Puppet, Monitor, Network
"""

tab_control = ttk.Notebook(app, bootstyle="primary")
tab_control.bind('<<NotebookTabChanged>>', lambda event: tab_control.update_idletasks())

from src.ui.FrameTracker import FrameTracker
FrameTracker(tab_control)

from src.ui.FramePuppet import FramePuppet
FramePuppet(tab_control)

from src.ui.FrameMonitor import FrameMonitor
ui_blendshapes = FrameMonitor(tab_control, app)

from src.ui.FrameNetwork import FrameNetwork
FrameNetwork(tab_control)

tab_control.pack(fill=BOTH, expand=YES)

"""
    UI Events
"""

def tick_event_handler(evt):
    if tab_control.index('current') == 2:
        ui_blendshapes.update_blendshapes(app)

ui_bg_thread.root_delegate = app
ui_bg_thread.start()
app.bind("<<TickUpdate>>", tick_event_handler)  # event triggered by background thread

def status_change_event_handler(evt):
    lbl_status.config(text=camera_bg_thread.ui_status_msg)
    if (camera_bg_thread.running):
        btn_start.config(text=Emoji.get('black medium square'), bootstyle="danger")
    else:
        btn_start.config(text=Emoji.get('black right-pointing triangle'), bootstyle="success")

camera_bg_thread.ui_app_delegate = app
camera_bg_thread.start()
app.bind('<<StatusChanged>>', status_change_event_handler)



# Main Thread
app.mainloop()

# Save settings when app is closed
save_config()