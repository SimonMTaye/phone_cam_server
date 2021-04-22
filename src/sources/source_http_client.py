from threading import Thread
from time import sleep
from typing import Any, Dict, Optional
from PIL import UnidentifiedImageError

from requests import get, exceptions

from sources.source_abstract_que import AbstractQueSource
from sources.factory import FactoryMixin, ParamInfo
from sources.image_utils import get_image_resolution, get_image_object


class HttpClientSource(AbstractQueSource, FactoryMixin):
    def __init__(self) -> None:
        super().__init__()
        self.url: Optional[str] = None
        self.port: Optional[int] = None
        self.endpoint: Optional[str] = None
        self.sleep_duration: Optional[float] = None
        self._client_thread = Thread(target=self.get_images_from_server, daemon=True)

    def set_url_and_port(self, url: str, port: int, endpoint: Optional[str]):
        self.url = url
        self.port = port
        self.endpoint = endpoint

    def handle_image(self, data: Any):
        if not self.ready:
            try:
                img = get_image_object(data)
            except UnidentifiedImageError:
                return
            res = get_image_resolution(img)
            self._height = res[1]
            self._width = res[0]
            self.init_que()
        self._image_que.queue(data)

    def get_images_from_server(self):
        while True:
            url = f"{self.url}:{self.port}"
            if self.endpoint:
                url += self.endpoint
            try:
                r = get(url)
                self.handle_image(r.content)
            except exceptions.ConnectionError as e:
                print("Connection to device failed")
                print(e)
            assert self.sleep_duration is not None
            sleep(self.sleep_duration)

    def run_http_client(self):
        self._client_thread.start()

    @staticmethod
    def create(
        *,
        url,
        port: int = 80,
        endpoint: Optional[str] = None,
        sleep_duration: float = 1 / 24,
    ) -> "HttpClientSource":
        source = HttpClientSource()
        source.set_url_and_port(url, port, endpoint)
        source.sleep_duration = sleep_duration
        source.run_http_client()
        return source

    @staticmethod
    def parameters() -> Dict[str, ParamInfo]:
        return {
            "url": ParamInfo(str, "Url for image server", True),
            "sleep_duration": ParamInfo(
                float, "Delay between querying the server for images", False
            ),
            "port": ParamInfo(int, "Image server port", False),
            "endpoint": ParamInfo(str, "Endpoint for image server", False),
        }
