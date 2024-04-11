
import random
from src.config import config

class AutoBlink:
    def __init__(self):
        self.is_blinking = False
        self.current = 0
        self.delta = 0.1

        self.frames_since_last = 0
        
    def _start_blink(self):
        self.is_blinking = True
        self.frames_since_last = 0
        self.delta = random.uniform(0.08, 0.4)

    def _step_blink(self):
        self.current += self.delta

        # Eyes Closed
        if self.current >= 1.0:
            self.current = 1.0
            self.delta = -self.delta

        # Eyes open
        if self.current <= 0.0:
            self.current = 0.0
            self.delta = 0.0
            self.is_blinking = False

    def step(self, np_blendshapes):
        if (self.is_blinking):
            self._step_blink()
            # Right Blink
            np_blendshapes[0] = self.current
            # Left Blink
            np_blendshapes[7] = self.current
        else:
            self.frames_since_last += 1
            if (random.random() * self.frames_since_last > config["Animation"].getfloat('auto_blink_rate')):
                self._start_blink()
        return np_blendshapes