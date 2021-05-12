from time import sleep, time
from threading import Thread
from typing import Type

from controller.filter import FilterMixin
from sources.source_abstract import AbstractSource
from camera.camera_factory import camera_factory
from camera.camera_abstract import AbstractCamera

# TODO Connector must handle platform filters (eg RGB -> RGBA for windows)
# TODO It should also be responsible for converting Image object to array
# TODO Performace of Image -> ndarray should be considered


class Connector(FilterMixin):

    # TODO If preview will be needed, controller should provide

    def __init__(
        self, source: AbstractSource, camera: AbstractCamera, fps: int
    ) -> None:
        self.source = source
        self.fps = fps
        self._wait_per_frame: float = 1 / fps
        self._bgthread = Thread(target=self.source_to_camera, daemon=True)
        self.camera = camera
        self._run = True

    def source_to_camera(self):
        with self.camera:
            while self._run:
                start = time()
                frame = self.source.get_frame()
                # frame = self.apply_filters(frame)
                self.camera.send(frame)
                now = time()
                sleep(max(self._wait_per_frame - (now - start), 0))

    def start(self):
        self._run = True
        self._bgthread.start()

    def stop(self):
        self._run = False
        self._bgthread.join()

    @classmethod
    def factory(
        cls: Type["Connector"], source: AbstractSource, fps: int = 24
    ) -> "Connector":
        while not source.ready:
            sleep(0.1)
        camera = camera_factory(source.width, source.height, fps)
        return cls(source, camera, fps)
