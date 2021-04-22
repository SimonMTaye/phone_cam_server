import platform

from camera.camera_win import WindowsCamera
from camera.camera_abstract import AbstractCamera


def camera_factory(width: int, height: int, fps: int) -> AbstractCamera:
    if platform.system() == "Windows":
        Camera = WindowsCamera 
    else:
        raise NotImplementedError("Only Windows is Supported")
    return Camera(width, height, fps)


