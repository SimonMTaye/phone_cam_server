from abc import ABC, abstractmethod
from threading import Thread

from camera.camera import Camera
from numpy import ndarray


class Source(ABC):
    def __init__(
        self, *, width: int = 1280, height: int = 720, fps: int = 24
    ) -> None:
        super().__init__()
        self._width = width
        self._height = height
        self._fps = fps
        self._keep_cam_running = True

    @property
    def fps(self) -> int:
        return self._fps

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @abstractmethod
    def get_frame(self) -> ndarray:
        pass

    def send_frames(self):
        with Camera(self.width, self.height, self.fps) as cam:
            while self._keep_cam_running:
                frame = self.get_frame()
                cam.send(frame)
                cam.wait_for_next_frame()

    def start(self):
        self._keep_cam_running = True
        self._thread = Thread(
            None, name="Virtual Cam Data thread", target=self.send_frames, daemon=True
        )
        self._thread.start()

    def stop(self):
        self._keep_cam_running = False
        self._thread.join()
