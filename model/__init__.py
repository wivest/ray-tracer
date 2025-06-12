from typing import TypeAlias

from .gltf_parser import get_camera_data
from .material import Material
from .setup import Setup
from .spatial import Spatial
from .triangle import Triangle

# aliases
vec: TypeAlias = tuple[float, float, float]
basis: TypeAlias = tuple[vec, vec, vec]
