from typing import Optional
import camera_win
from numpy import ndarray, zeros, uint8

from camera.camera_abstract import AbstractCamera


#TODO deal with integer overflow in frame index
class WindowsCamera(AbstractCamera):
    def __init__(self, width: int, height: int, fps: int) -> None:
        super().__init__(width, height, fps=fps)
        self._cam = camera_win
        self._frame_index = 0
        self._previous_frame: Optional[ndarray] = None

    def close(self):
        self._cam.close()

    def send(self, frame: ndarray):
        super().send(frame)
        self._frame_index += 1
        # val is the returned error code from C++ code. Used for debugging. Can be removed
        self._cam.send(
            self._frame_index, self.fps, self.width, self.height, frame
        )
