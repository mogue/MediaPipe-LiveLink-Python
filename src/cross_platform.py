import sys, os, subprocess
import cv2

if sys.platform.startswith("win"):    
    from pygrabber.dshow_graph import FilterGraph

# https://stackoverflow.com/questions/52558617/enumerate-over-cameras-in-python
def get_camera_device_names():
    if sys.platform.startswith("win"):    
    # Windows device names: https://stackoverflow.com/questions/70886225/get-camera-device-name-and-port-for-opencv-videostream-python
        return FilterGraph().get_input_devices() 
    elif sys.platform.startswith("linux"):
        # Linux: https://stackoverflow.com/questions/73185493/python-get-all-camera-indexes-and-name
        devs = os.listdir('/dev')
        vid_indices = [int(dev[-1]) for dev in devs 
                    if dev.startswith('video')]
        vid_indices = sorted(vid_indices)
        return [ "Default Camera Device" ]
    else:
        camera_list = []
        for i in range(10): 
            cap = cv2.VideoCapture(i)
            ret, frame = cap.read()
            if ret:
                camera_list.append("Camera " + str(i))
        return camera_list

def get_camera_device_formats(input_source):
    if sys.platform.startswith("win"):
        graph = FilterGraph()
        graph.add_video_input_device(input_source)
        formats = graph.get_input_device().get_formats()
        str_formats = [(
            "["+str(x["index"])+"] " +
            str(x["height"]) + 'p ' + 
            str(int(x["min_framerate"])) + "fps"
            ) for x in formats 
        ]
        print(str_formats)
        return (formats, str_formats)
    elif sys.platform.startswith("linux"):
        fmt_list = [""]
        return fmt_list
    else:
        fmt_list = [""]
        return fmt_list

import ctypes as ct

def dark_title_bar(window):
    if sys.platform.startswith("win"):    
        """
        https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter
        MORE INFO:
        https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                            ct.sizeof(value))