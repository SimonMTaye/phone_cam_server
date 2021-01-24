from sys import argv
from .image_source import ImageSource
from time import sleep


if __name__ == "__main__":
    if len(argv) > 1:
        img_path = argv[1]
        source = ImageSource.create(img_path)
    else:
        source = ImageSource.create()
    try:
        source.start()
        while True:
            continue
    except BaseException as e:
        source.stop()
        raise e
