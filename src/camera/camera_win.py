import camera_win
from numpy import ndarray

from camera.camera_abstract import AbstractCamera


# FIXME deal with integer overflow in frame index
class WindowsCamera(AbstractCamera):
    def __init__(self, width: int, height: int, fps: int) -> None:
        super().__init__(width, height, fps)
        self._cam = camera_win
        self._frame_index = 0

    def close(self):
        self._cam.close()

    def send(self, frame: ndarray):
        super().send(frame)
        self._frame_index += 1
        # The function returns an error code from C++ code. Used for debugging
        self._cam.send(self._frame_index, self.fps, self.width, self.height, frame)
