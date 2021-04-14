from io import BytesIO
from typing import Optional, Any, Tuple

from PIL.Image import Image, open

from numpy import ndarray, asarray_chkfinite, zeros, uint8

def process_image(img: Image, width: Optional[int] = None, height: Optional[int] = None) -> ndarray:
    img = img.convert("RGBA")
    if width and height:
        img = img.resize((width, height))
    return asarray_chkfinite(img)

def valid_frame(frame: Optional[ndarray], height: int, width: int) -> bool:
    if frame is not None:
        return frame.shape[0] == height and frame.shape[1] == width
    else:
        return False

def get_image_object(data: Any) -> Image:
    img_data = BytesIO(data)
    return open(img_data)

def get_image_resolution(img: Image)-> Tuple[int, int]:
    return (img.width, img.height)

def blank_image(width: int, height: int) -> ndarray:
    return zeros((width, height, 4), uint8)


