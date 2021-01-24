from setuptools import depends, setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "camera_win",
        ["src/_camera_win/main.cpp"],
    )
]
NAME = "phone-cam"
AUTHOR = "Simon Taye"
DESCRIPTION = "Send frames to a virtual camera"
EMAIL = "mulat.simon@gmail.com"
PYTHON_VERSION = ">=3.7.0"
VERSION = "0.1.0"
DEPENDENCIES = ["pybind11", "numpy"]

setup(
    name=NAME,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    install_requires=DEPENDENCIES,
    python_requires=PYTHON_VERSION,
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)