from typing import Any
from threading import Lock, Thread

from PIL import Image
from numpy import zeros, uint8, ndarray, asarray_chkfinite
from io import BytesIO
from flask import Flask, request

from .image_que import ImageQue
from .source import AbstractSource

# TODO Standardize Image Resolution


class NetworkSource(AbstractSource):
    def __init__(self, *, width: int = 0, height: int = 0, fps: int = 24) -> None:
        super().__init__(width=width, height=height, fps=fps)
        self._server_thread = Thread(
            None, self.run_server, "Get new frame from network source", daemon=True
        )
        self._image_que = ImageQue()

    def run_server(self):
        app = self.get_app()
        app.run("0.0.0.0", 7447, debug=False, load_dotenv=True)

    def get_frame(self) -> ndarray:
        return self._image_que.dequeue()

    def update_frame(self, data: Any):
        self._image_que.queue(data)

    def get_app(self) -> Flask:
        app = Flask(__name__)

        @app.route("/frame", methods=["GET", "POST"])
        def set_frame():
            if request.method == "POST":
                print("Image Recieved")
                self.update_frame(request.data)
                return "SUCCESS"
            else:
                print("Recieved GET request")
                return "USE POST"

        return app

    def start(self):
        super().start()
        self._server_thread.start()

    def stop(self):
        super().stop()