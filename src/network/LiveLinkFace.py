import socket
from src.config import config
from src.anim.FaceAnimator import face_animator
from src.network.LiveLinkPacket import LiveLinkPacket

class LiveLinkFace_protocol:
    def __init__(self):
        self.frame_out = LiveLinkPacket()

    def connect(self):
        # self.ip   = config["LiveLinkFace"].get("ip",fallback='127.0.0.1')
        # self.port = config["LiveLinkFace"].getint("port", fallback=11111)
        self.frame_out.VERSION      = LiveLinkPacket.VERSION # 6
        self.frame_out.device_id    = config["LiveLinkFace"].get("device_id", fallback='WebCam') # Ignored
        self.frame_out.subject_name = config["LiveLinkFace"].get("subject_name", fallback='BasicRole') # Ignored
        self.frame_out.frame_time   = {"frame_number":0, "sub_frame":0, "numerator":0, "denominator":0}
        self.frame_out._serialize_header()
        self.frame_out._serialize_timer()

    def run(self):
        if config["LiveLinkFace"].getboolean("send"):
            self.frame_out.np_data = face_animator.np_out
            self.frame_out._serialize()
            MESSAGE = self.frame_out.data
            try:
                sock = socket.socket(socket.AF_INET, 
                                    socket.SOCK_DGRAM) 
                sock.sendto(MESSAGE, (
                    config["LiveLinkFace"].get("ip"), 
                    config["LiveLinkFace"].getint("port")
                ))
            except:
                pass

live_link_face_protocol = LiveLinkFace_protocol()
