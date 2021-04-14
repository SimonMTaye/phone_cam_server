from typing import Any, Optional, Dict
from threading import Thread

from PIL import UnidentifiedImageError

from flask import Flask, request
from sources.factory import FactoryMixin, ParamInfo

from sources.source_abstract_que import AbstractQueSource
from sources.image_utils import get_image_object, get_image_resolution


class HttpServerSource(AbstractQueSource, FactoryMixin):
    def __init__(self) -> None:
        super().__init__()
        self._server_thread = Thread(target=self.run_server, daemon=True)
        self.url: Optional[str]
        self.endpoint: Optional[str]
        self.port: Optional[int]
        

    def set_url_and_port(self, url: str, port: int, endpoint: str = "/frame"):
        self.url = url
        self.port = port
        self.endpoint = endpoint

    def run_server(self):
        if self.url is None or self.port is None or self.endpoint is None:
            raise AttributeError("Server information must be set before running it")
        app = self.get_app()
        app.run(self.url, self.port, debug=False, load_dotenv=True)

    def recieved_frame(self, data: Any):
        if not self.ready:
            try:
                img = get_image_object(data)
                res = get_image_resolution(img)
                self.__width = res[0]
                self.__height = res[1]
                self.init_que()
            except (UnidentifiedImageError, OSError) as e:
                print(e)
                return
        self.__image_que.queue(data)

    def get_app(self) -> Flask:
        app = Flask(__name__)

        assert self.endpoint is not None

        @app.route(self.endpoint, methods=["GET", "POST"])
        def set_frame():
            if request.method == "POST":
                print("Image Recieved")
                self.recieved_frame(request.data)
                return "SUCCESS"
            else:
                print("Recieved GET request")
                return "USE POST"

        return app

    @staticmethod
    def parameters()-> Dict[str, ParamInfo]:
        return {
            "url": ParamInfo(str, "Server url", True), 
            "port": ParamInfo(int, "Server port", True), 
            "endpoint": ParamInfo(str, "Endpoint for getting images", False)
            }

    @staticmethod
    def create(**kwargs) -> "HttpServerSource":
        try:
            url = kwargs["url"]
            port = kwargs["port"]
            endpoint = kwargs.get("endpoint", "/frame")
            source = HttpServerSource()
            source.set_url_and_port(url, port, endpoint)
            source.run_server()
            return source
        except KeyError:
            raise ValueError("Required function parameters not passed")
