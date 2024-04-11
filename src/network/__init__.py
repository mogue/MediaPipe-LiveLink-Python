import threading, time

from src.anim.FaceAnimator import face_animator

class NetworkThread(threading.Thread):
    def __init__(self, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        # self.queue = queue
        self.daemon = True
        # self.receive_messages = args[0]
        self.frame_seconds = (1. / 60.)
        self.running = False

        self.update_delegates = []

    def run(self):
        while True:
            if self.running:
                face_animator.update_frame_out()
                for protocol in self.update_delegates:
                    protocol.run()
            # Sleeps for 1 frame + processing time.
            # This causes a frame drop over time.
            # I considered accounting for the processing time
            # but I think it's not worth it for now.
            # Note: time.sleep also has 10-15ms. granularity.
            time.sleep(self.frame_seconds)

    def toggle(self):
        self.running = not self.running

network_bg_thread = NetworkThread()

from src.network.LiveLinkFace import live_link_face_protocol
live_link_face_protocol.connect()
network_bg_thread.update_delegates.append(live_link_face_protocol)

network_bg_thread.start()