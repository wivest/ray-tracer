import argparse
from argparse import Namespace

SIZE = (1080, 720)
DEFAULT_GLTF = "./scene/untitled.gltf"

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--render", action="store_true")
parser.add_argument("-x", "--width", default=SIZE[0], type=int)
parser.add_argument("-y", "--height", default=SIZE[1], type=int)
parser.add_argument("filename", nargs="?", default=DEFAULT_GLTF)


def get_args() -> Namespace:
    return parser.parse_args()
