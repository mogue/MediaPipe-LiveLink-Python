import threading, logging
import os, time, pkgutil
import numpy as np
import cv2
import mediapipe as mp

from src.config import config
from src.mpipe.FaceDetector import FaceDetector

COLOR_WHITE = (255,255,255)
TOP_LEFT = (16,48)

class CameraThread(threading.Thread):
    def __init__(self, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        # self.queue = queue
        self.daemon = True
        # self.receive_messages = args[0]
        self.running = False
        self.capture = None

        self.failed = False
        self.ui_status_msg = 'Press play to start tracking.'
        self.ui_app_delegate = None

        self.face_detector = FaceDetector()
        self.face_detector.prepare()

    def fail(self, msg):
        print(msg)
        self.ui_status_msg = msg
        self.running = False
        self.failed = True
        self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")

    def camera_setup(self):
        self.failed = False
        self.frame_ms = int(1000. / config["Camera"].getfloat("FPS", fallback=30))

        self.ui_status_msg = "Connecting to Camera..."
        self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")

        try:
            self.capture = cv2.VideoCapture(config["Camera"].getint("input_source", fallback=0))
        except cv2.error as error:
            print(error.args)
            

        # Test if input device works.
        if self.capture is None or not self.capture.isOpened():
            self.fail("Error: Camera Device Not Found")
            return
        
        """
        success, _frame = self.capture.read()
        if not success:
            self.fail("Error: Camera Device Already In Use")
            return
        """
        self.cam_width  = config["Camera"].getfloat("width", fallback=0)
        self.cam_height = config["Camera"].getfloat("height", fallback=0)
        
        self.ui_status_msg = "Setting Camera Resolution..."
        self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")
        if self.cam_width > 0:
            self.capture.set(3, self.cam_width)    # width
        if self.cam_height > 0:
            self.capture.set(4, self.cam_height)   # height
            
        self.ui_status_msg = "Opening Preview Window..."
        self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")
        cv2.namedWindow("preview")
        self.ui_status_msg = "Running..."
        self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")

    def camera_destroy(self):
        if not self.failed:
            self.ui_status_msg = "Closing Camera..."
            self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")
        if self.capture.isOpened():
            self.capture.release()
        # closing all open windows 
        cv2.destroyAllWindows() 
        self.capture = None
        if not self.failed:
            self.ui_status_msg = "Press play to start tracking."
            self.ui_app_delegate.event_generate("<<StatusChanged>>", when="tail")

    def process_frame(self):
        latest_results = None

        mirror_camera  = config["CameraOptions"].getboolean("mirror_camera", fallback=False)
        flip_camera    = config["CameraOptions"].getboolean("flip_camera", fallback=False)
        rotate_camera  = config["CameraOptions"].getboolean("rotate_camera", fallback=False)
        show_wireframe = config["CameraOptions"].getboolean("preview_wireframe", fallback=True)
        show_webcam    = config["CameraOptions"].getboolean("preview_camera",  fallback=True)

        # with vision.FaceLandmarker.create_from_options(options) as detector:
        if self.capture.isOpened():
            # print( self.capture.getBackendName())
            success, image = self.capture.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                return
            height, width = image.shape[:2]
            if rotate_camera:
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            if mirror_camera:
                image = cv2.flip(image, 1)
            if flip_camera:
                image = cv2.flip(image, 0)
            delta_process_time = time.time()

            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

            latest_results = self.face_detector.detect(mp_image)

            delta_process_time = self.frame_ms - int((time.time() - delta_process_time) * 1000)
            if (delta_process_time <= 0):
                # If processing took longer then a frame
                # Note this seems to happen if no face is found.
                delta_process_time = 1 # ms.

            # STEP 5: Process the detection result. In this case, visualize it.
            # Start of output Image
            if not show_webcam:
                image = np.zeros(shape=[height, width, 3], dtype=np.uint8) # blank image
            
            if show_wireframe:
                image = self.face_detector.draw(image, latest_results)

            if len(latest_results.face_blendshapes) == 0:
                image = cv2.putText(image, "NO FACE DETECTED", TOP_LEFT, cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_WHITE, 2, cv2.LINE_AA)

            cv2.imshow('preview', image)

            # ESC key to stop the process
            if cv2.waitKey(delta_process_time) & 0xFF == 27:
                self.running = False
            
            # Preview window closed, stop the process
            if cv2.getWindowProperty('preview', cv2.WND_PROP_VISIBLE) < 1:
                self.running = False

    # Thread.start() process
    def run(self):
        while True:
            if self.running:
                if not self.capture:
                    self.camera_setup()
                else:
                    self.process_frame()
            else:
                if self.capture:
                    self.camera_destroy()
                time.sleep(0.5)

    def toggle(self):
        self.running = not self.running
