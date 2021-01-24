import camera_win
from numpy import ndarray, zeros, uint8

from .camera_base import CameraBase


class WindowsCamera(CameraBase):
    def __init__(self, width: int, height: int, fps: int) -> None:
        super().__init__(width, height, fps=fps)
        self._cam = camera_win
        self._frame_index = 0

    def close(self):
        self._cam.close()

    def send(self, frame: ndarray):
        super().send(frame)
        self._frame_index += 1
        # Switch B and R bits since DirectShow filters need it that way
        adjusted_frame = zeros((self.height, self.width, 4), dtype=uint8)
        for y in range(self.height):
            for x in range(self.width):
                adjusted_frame[y][x] = [
                    frame[y][x][2],
                    frame[y][x][1],
                    frame[y][x][0],
                    frame[y][x][3],
                ]
        # val returns code from C++ code. Used for debugging. Can be removed
        val = self._cam.send(
            self._frame_index, self.fps, self.width, self.height, adjusted_frame
        )
