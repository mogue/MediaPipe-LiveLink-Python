import os, time, pkgutil
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from src.config import config
from src.livelink import LiveLinkUpdate
from src.mediapipe_draw import  draw_landmarks_on_image

VisionRunningMode = mp.tasks.vision.RunningMode

frame_ms = int(1000. / config["Camera"].getfloat("FPS", fallback=30))

show_wireframe = config["UI"].getboolean("preview_wireframe", fallback=False)
show_webcam = config["UI"].getboolean("preview_camera",  fallback=False)

cv2.namedWindow("preview")
cap = cv2.VideoCapture(config["Camera"].getint("input_source", fallback=0))

cam_width = config["Camera"].getfloat("width")
cam_height = config["Camera"].getfloat("height")

if cam_width > 0:
    cap.set(3, cam_width)    # width
if cam_height > 0:
    cap.set(4, cam_height)   # height

latest_results = None

# Create a face detector instance with the live stream mode:
def print_result(result: vision.FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_results
    latest_results = result
    LiveLinkUpdate(result.face_blendshapes[0])
    # print('face detector result: {}'.format(result))

# STEP 2: Create an FaceLandmarker object.
base_options = python.BaseOptions(
    # model_asset_path=os.path.join('src','face_landmarker_v2_with_blendshapes.task'),
    model_asset_buffer=pkgutil.get_data( 'src', 'face_landmarker_v2_with_blendshapes.task' )
    )
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       running_mode=VisionRunningMode.IMAGE,  # VisionRunningMode.LIVE_STREAM,
                                       # result_callback=print_result,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1,
                                       min_face_detection_confidence= config["MediaPipe"].getfloat("min_face_detection_confidence"),
                                       min_face_presence_confidence= config["MediaPipe"].getfloat("min_face_presence_confidence"),
                                       min_tracking_confidence= config["MediaPipe"].getfloat("min_tracking_confidence"))
detector = vision.FaceLandmarker.create_from_options(options)

with vision.FaceLandmarker.create_from_options(options) as detector:
    while cap.isOpened():
        success, image = cap.read()
        height, width = image.shape[:2]
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        delta_process_time = time.time()

        # Convert the frame received from OpenCV to a MediaPipe’s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # STEP 4: Detect face landmarks from the input image.
        # detection_result = detector.detect_async(mp_image, round(time.time()*1000))
        latest_results = detector.detect(mp_image)
        if len(latest_results.face_blendshapes) and len(latest_results.facial_transformation_matrixes):
            LiveLinkUpdate(latest_results.face_blendshapes[0], latest_results.facial_transformation_matrixes)

        delta_process_time = frame_ms - int((time.time() - delta_process_time) * 1000)
        if (delta_process_time <= 0):
            # If processing took longer then a frame
            # Note this seems to happen if no face is found.
            delta_process_time = 1 # ms.

        # Start of output Image
        if not show_webcam:
            image = np.zeros(shape=[height, width, 3], dtype=np.uint8) # blank image

        # STEP 5: Process the detection result. In this case, visualize it.
        if latest_results and show_wireframe:
            annotated_image = draw_landmarks_on_image(image, latest_results)

        if show_webcam or show_wireframe:
            cv2.imshow('preview', annotated_image)

        #  ESC key to stop the process
        if cv2.waitKey(delta_process_time) & 0xFF == 27:
            print("Exiting...")
            break
  
# plot_face_blendshapes_bar_graph(latest_results.face_blendshapes[0])

# closing all open windows 
cv2.destroyAllWindows() 