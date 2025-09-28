import argparse
from argparse import Namespace

SIZE = (1080, 720)
DEFAULT_SAVE = "render.png"

HELP_SAMPLES = "number of samples render lens takes"
HELP_ITERS = "number of iterations (bounces) each ray takes"
HELP_SKY = "hex color of monochrome sky"
HELP_RENDER = "run render and save rendered image"
HELP_WIDTH = "width of window/image"
HELP_HEIGHT = "height of window/image"
HELP_CAMERA = "active camera index (useful when rendering)"
HELP_FILENAME = "path to .gltf or .glb file"


def hex(value: str) -> list[float]:
    value = value.lstrip("#")
    n = len(value)
    return list(int(value[i * n // 3 : (i + 1) * n // 3], 16) / 255 for i in (0, 1, 2))


parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--samples", default=64, type=int, help=HELP_SAMPLES, metavar="N"
)
parser.add_argument("-i", "--iters", default=5, type=int, help=HELP_ITERS, metavar="N")
parser.add_argument(
    "-S", "--sky", default="#FFFFFF", type=hex, help=HELP_SKY, metavar="HEX"
)
parser.add_argument(
    "-r",
    "--render",
    nargs="?",
    const=DEFAULT_SAVE,
    default=None,
    help=HELP_RENDER,
    metavar="SAVEPATH",
)
parser.add_argument(
    "-x", "--width", default=SIZE[0], type=int, help=HELP_WIDTH, metavar="PX"
)
parser.add_argument(
    "-y", "--height", default=SIZE[1], type=int, help=HELP_HEIGHT, metavar="PX"
)
parser.add_argument(
    "-c", "--camera", default=0, type=int, help=HELP_CAMERA, metavar="INDEX"
)
parser.add_argument("filename", help=HELP_FILENAME)


def get_args() -> Namespace:
    return parser.parse_args()
