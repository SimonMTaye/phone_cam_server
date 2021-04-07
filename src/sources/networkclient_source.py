from threading import Thread
from .source import AbstractSource
from .image_que import ImageQue
from requests import get


class NetworkClientSource(AbstractSource):
    def __init__(self, *, width: int = 0, height: int = 0, fps: int = 24) -> None:
        super().__init__(width=width, height=height, fps=fps)
        self._image_que = ImageQue()
        self._input_thread = Thread(target=self.get_images_from_server, daemon=True)
        self._url = None
        self._port = 15535
        self._endpoint = "/frame"

    def set_url_and_port(self, url: str, *, endpoint: str = "/frame", port: int = 15535):
        self._url = url
        self._port = port
        self._endpoint = endpoint

    def get_images_from_server(self):
        while self._keep_cam_running:
            if self._url and self._port:
                url = f"{self._url}:{self._port}"
                if self._endpoint:
                    url += self._endpoint
                r = get(url)
                self._image_que.queue(r.content)
            self.wait_for_next_frame()

    def get_frame(self):
        return self._image_que.dequeue()

    def start(self):
        self._input_thread.start()
        super().start()