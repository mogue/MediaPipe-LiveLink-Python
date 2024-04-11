import numpy as np
from src.config import config

from src.anim.AutoBlink import AutoBlink

class FaceAnimator:
    def __init__(self):

        self.fps = 60
        self.frame_number = 0
        self.ratio = self.fps / config["Camera"].getint('fps')

        self.np_zero        = np.zeros(61, dtype='>f')
        self.np_neutral     = np.zeros(61, dtype='>f')
        self.np_freeze      = np.empty(61, dtype='>f')
        self.np_freeze[:]   = np.nan

        # Thread: Camera
        self.np_delta       = np.zeros(61, dtype='>f')
        self.np_target      = np.zeros(61, dtype='>f')
        self.np_scale       = np.ones( 61, dtype='>F')
        self.np_delta_cache = np.zeros([120,61], dtype='>f')
        self.np_value_cache = np.zeros([12, 61], dtype='>f')

        # Thread: Network
        self.np_current     = np.zeros(61, dtype='>f')
        self.np_out         = np.zeros(61, dtype='>f')

        self.np_max         = np.ones( 61, dtype='>f')
        if config["Calibration"].getboolean('use_elastic_max'):
            self.init_elastic_max()

        self.auto_blink = AutoBlink()
        
    def _calc_delta(self, np_new):
        ## Camera ##

        # Update Value Buffer
        self.np_value_cache = np.delete(self.np_value_cache, (0), axis=0)
        self.np_value_cache = np.r_[self.np_value_cache, [np_new]]

        # Elastic Scaling
        if (config["Calibration"].getboolean('use_elastic_max')):
            self.np_max = np.max([self.np_max, np.min(self.np_value_cache, axis=0)], axis=0)
        self.np_scale = 1. / (self.np_max - self.np_neutral) 
        np_new = np_new * self.np_scale

        # Calculate the initial Delta
        self.np_delta = (np_new - self.np_current)
        self.np_delta_cache = np.delete(np.abs(self.np_delta_cache), (0), axis=0)
        self.np_delta_cache = np.r_[self.np_delta_cache,[self.np_delta]]

        # Noise gates (ignore under the threshohlds)
        if config["CameraFilters"].getboolean("jitter_removal_on"):
            amt = config['CameraFilters'].getfloat('jitter_removal_threshold')
            noise_gates = (np.abs(self.np_delta) < np.median(self.np_delta_cache, axis=0) * amt)
            self.np_delta = np.ma.array(self.np_delta, mask=noise_gates).filled(0)
            self.np_target = np.ma.array(np_new, mask=noise_gates).filled(self.np_current)
        else:
            self.np_target = np_new

        # Smoothing
        if config["CameraFilters"].getboolean("frame_smoothing_on"):
            self.np_delta = (self.np_delta / (config["CameraFilters"].getfloat("frame_smoothing_amount") * self.ratio))
    
    def _recover_delta(self):
        ## Camera ##
        self.np_delta = (self.np_neutral - self.np_current)
        self.np_delta = (self.np_delta / (config["Animation"].getfloat("recovery_time") * self.fps))
        self.np_target = self.np_neutral

    def _calc_overrides(self):
        ## Network ##

        # Freeze
        self.np_out = np.ma.array(self.np_freeze,mask=np.isnan(self.np_freeze)).filled(self.np_out)

        # Breathy
        # self.np_out[:52] *= ((math.sin(self.frame_number / 10.) * 0.1) + 1)

        if config['Animation'].getboolean('auto_blink_on'):
            self.np_out = self.auto_blink.step(self.np_out)

        # Clamp
        self.np_out[:52] = np.clip(self.np_out[:52], 0.0, 1.0, out=self.np_out[:52])
        self.np_out[52:] = np.clip(self.np_out[52:], -1.0, 1.0, out=self.np_out[52:])

    def set_neutral_face(self, event):
        # self.np_neutral = np.copy(self.np_current)
        self.np_neutral = np.mean(self.np_value_cache, axis=0)

    def clear_neutral_face(self, event):
        self.np_neutral = np.zeros(61, dtype='>f')

    def clear_elastic_max(self):
        self.np_max = np.ones(61, dtype='>f')

    def init_elastic_max(self):
        self.np_max = np.zeros(61, dtype='>f')
        self.np_max += 0.1
        self.np_max[52:] = 1.0

    def update_frame_out(self):
        ## Network ##
        self.frame_number += 1
        if (abs(self.np_target - self.np_current) <= abs(self.np_delta)).all():
            # Have we arrived?
            # If smoothing is off
            # If Camera frame drops 
            # If thread desync
            # print(str(self.frame_number)  + ": Hit Target")
            # self.np_delta = self.np_zero
            self.np_current = self.np_target
        else:
            # Step
            self.np_current += self.np_delta

        self.np_out = np.copy(self.np_current) - self.np_neutral
        self._calc_overrides()
        return self.np_out

    def update_frame_in(self, new_np_blendshapes, face_found):
        ## Camera ##
        if face_found:
            """
            self.np_max_blends = np.max([self.np_max_blends, new_np_blendshapes], axis=0)
            np_scale = 1. / (self.np_max_blends * 0.95)
            new_np_blendshapes *= np_scale
            """
            # Smoothing (calculate the delta step)
            self._calc_delta(new_np_blendshapes)

        else: # Face not found
            if config["Animation"].getboolean("recovery_on"):
                self._recover_delta()
            else:
                # Freeze (set delta to zeros)
                self.np_delta = self.np_zero

face_animator = FaceAnimator()