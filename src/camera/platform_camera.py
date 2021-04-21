import platform
from camera.camera_abstract import AbstractCamera

from typing import Callable
from camera.camera_win import WindowsCamera

if platform.system() == "Windows":
    Camera: Callable[[int, int, int], AbstractCamera] = WindowsCamera
else:
    raise NotImplementedError("Only Windows is Supported")
