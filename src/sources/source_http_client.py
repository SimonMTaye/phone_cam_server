from threading import Thread
from time import sleep 
from typing import Any, Dict, Optional

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
            img = get_image_object(data)
            res = get_image_resolution(img)
            self.__height = res[1]
            self.__width = res[0]
            self.init_que()
        self.__image_que.queue(data)

    def get_images_from_server(self):
        while True:
            url = f"{self.url}:{self.port}"
            if self.endpoint:
                url += self.endpoint
            try:
                r = get(url)
                self.__image_que.queue(r.content)
            except exceptions.ConnectionError as e:
                print("Connection to device failed")
                print(e)
            assert self.sleep_duration is not None
            sleep(self.sleep_duration)

    def run_http_client(self):
        self._client_thread.start()

    @staticmethod
    def create(**kwargs) -> "HttpClientSource":
        try:
            url = kwargs["url"]
            sleep_duration = kwargs["sleep_duration"]
            port = kwargs.get("port", 80)
            endpoint = kwargs.get("endpoint", None)
            source = HttpClientSource()
            source.set_url_and_port(url, port, endpoint)
            source.sleep_duration = sleep_duration
            source.run_http_client()
            return source
        except KeyError:
            raise ValueError("Required parameters not passed")

    @staticmethod
    def parameters() -> Dict[str, ParamInfo]:
        return {
            "url": ParamInfo(str, "Url for image server", True),
            "sleep_duration": ParamInfo(
                float, "Delay between querying the server for images", True
            ),
            "port": ParamInfo(int, "Image server port", False),
            "endpoint": ParamInfo(str, "Endpoint for image server", False),
        }
