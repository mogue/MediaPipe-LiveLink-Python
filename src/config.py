import configparser, os

config_filepath = 'WebCam_LiveLink.ini'
config = configparser.ConfigParser()

def save_config():
    with open(config_filepath, 'w') as configfile:
        config.write(configfile)

if os.path.exists(config_filepath):
    # Load the config.ini file.
    config.read(config_filepath)
else:
    # Creata a default config.ini file.
    config["UI"] = {
        "preview_wireframe": "True",
        "preview_camera": "True"
    }

    config["UDP"] = {
        "IP": "127.0.0.1",
        "Port": "11111"
    }

    config["Camera"]  = {
        "input_source": "0",
        "FPS": "30",
        "width": "0",
        "height": "0"
    }
    
    config["MediaPipe"] = {
        "min_face_detection_confidence": "0.5",
        "min_face_presence_confidence": "0.5",
        "min_tracking_confidence": "0.5"
    }

    config["LiveLink"] = {
        "device_id": "WebCam",
        "subject_name": "BasicRole"
    }

    save_config()