import platform
from camera.camera_base import CameraBase

from typing import Callable
from camera.camera_win import WindowsCamera

if platform.system() == "Windows":
    Camera: Callable[[int, int ,int], CameraBase] = WindowsCamera
else:
    raise NotImplementedError("Only Windows is Supported")