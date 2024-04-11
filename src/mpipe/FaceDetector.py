import pkgutil
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
VisionRunningMode = mp.tasks.vision.RunningMode

# Drawing
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

from src.config import config
from src.anim.FaceAnimator import face_animator

# Formatting
from scipy.spatial.transform import Rotation   
from src.network.ARkit import FACE_BLENDSHAPE_NAMES

def blendshapes_as_numpy_array(mp_arkit_blendshapes):
    arr = np.zeros(shape=[61], dtype='>f')
    mp_arkit_blendshapes.pop(0) # remove _neutral
    for blend in mp_arkit_blendshapes:
        i = FACE_BLENDSHAPE_NAMES.index(blend.category_name)
        arr[i] += blend.score
    return arr

def transform_to_euler(mp_transform):
    # Convert transformation matrix to Euler angles
    r = mp_transform[0][0:3, 0:3]
    r = Rotation.from_matrix(r)
    # return angles = ( Roll, Yaw, Pitch )
    return r.as_euler("zyx", degrees=False)
    """
    headRoll  = -angles[0]
    headYaw   = -angles[1]
    headPitch = -angles[2] 
    """

class FaceDetector:
    def __init__(self):
        self.detector = None
        self.detection_result = None

    def prepare(self):
        # STEP 2: Create an FaceLandmarker object.
        base_options = python.BaseOptions(
            # model_asset_path=os.path.join('src','face_landmarker_v2_with_blendshapes.task'),
            model_asset_buffer=pkgutil.get_data( 'data', 'face_landmarker_v2_with_blendshapes.task' )
        )
        options = vision.FaceLandmarkerOptions(base_options=base_options,
                                            running_mode=VisionRunningMode.IMAGE,  # VisionRunningMode.LIVE_STREAM,
                                            # result_callback=print_result,
                                            output_face_blendshapes=True,
                                            output_facial_transformation_matrixes=True,
                                            num_faces=1,
                                            min_face_detection_confidence= config["MediaPipeFaceLandmarker"].getfloat("min_face_detection_confidence"),
                                            min_face_presence_confidence= config["MediaPipeFaceLandmarker"].getfloat("min_face_presence_confidence"),
                                            min_tracking_confidence= config["MediaPipeFaceLandmarker"].getfloat("min_tracking_confidence"))
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, mp_image):
        use_head_rotation = config["Calibration"].getboolean('use_head_rotation', fallback=True)
        # STEP 4: Detect face landmarks from the input image.
        # detection_result = detector.detect_async(mp_image, round(time.time()*1000))
        latest_results = self.detector.detect(mp_image)
        blendshapes = np.zeros(shape=61, dtype='>f')
        if len(latest_results.face_blendshapes):
            blendshapes = blendshapes_as_numpy_array(latest_results.face_blendshapes[0])
        if len(latest_results.facial_transformation_matrixes) and use_head_rotation:
            angles = transform_to_euler(latest_results.facial_transformation_matrixes)
            blendshapes[54] -= angles[0] # Roll
            blendshapes[52] -= angles[1] # Yaw
            blendshapes[53] -= angles[2] # Pitch
        face_animator.update_frame_in(blendshapes, not (len(latest_results.face_blendshapes) == 0))
        return latest_results

    def draw(self, rgb_image, detection_result):
        face_landmarks_list = detection_result.face_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected faces to visualize.
        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            # Draw the face landmarks.
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
            ])

            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_tesselation_style())
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_contours_style())
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_iris_connections_style())

        return annotated_image
