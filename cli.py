import argparse
from argparse import Namespace

SIZE = (1080, 720)
DEFAULT_SAVE = "render.png"


def hex(value: str) -> list[float]:
    value = value.lstrip("#")
    return list(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--samples", default=64, type=int)
parser.add_argument("-i", "--iters", default=5, type=int)
parser.add_argument("-S", "--sky", default="#FFFFFF", type=hex)
parser.add_argument("-r", "--render", nargs="?", const=DEFAULT_SAVE, default=None)
parser.add_argument("-x", "--width", default=SIZE[0], type=int)
parser.add_argument("-y", "--height", default=SIZE[1], type=int)
parser.add_argument("-c", "--camera", default=0, type=int)
parser.add_argument("filename")


def get_args() -> Namespace:
    return parser.parse_args()
