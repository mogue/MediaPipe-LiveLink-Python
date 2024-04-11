
# Creata a default config.ini file.
default_dict = {
    "Application" : {
        "name": "MogueMotionCapture",
        "config_version" : 2,
        "debug_log": False,
        "theme": "darkly"
    },
    "Camera"  : {
        "input_source": 0,
        "FPS": 30,
        "width": 0,
        "height": 0
    },
    "CameraOptions" : {
        "mirror_camera": False,
        "flip_camera": False,
        "rotate_camera": False,
        "preview_wireframe": True,
        "preview_camera": True
    },
    "CameraFilters" : {
        "jitter_removal_on": True,
        "jitter_removal_threshold": 1.3,
        "frame_smoothing_on": True,
        "frame_smoothing_amount": 2.3
    },
    "MediaPipeFaceLandmarker" : {
        "min_face_detection_confidence": 0.5,
        "min_face_presence_confidence": 0.5,
        "min_tracking_confidence": 0.5
    },

    "Calibration" : {
        "use_elastic_max" : False,
        "use_head_rotation" : True
    },
    "Animation" : {
        "recovery_on" : True,
        "recovery_time" : 0.5,     # seconds?
        "auto_blink_on" : False,
        "auto_blink_rate" : 310    # frames?
    },

    "LiveLinkFace" : {
        "send": True,
        "ip": "127.0.0.1",
        "port": "11111",
        "device_id": "WebCam",
        "subject_name": "BasicRole"
    },
    "VirtualMotionCapture" : {
        "send" : False,
        "ip": "127.0.0.1",
        "port": "39539"
    }
}