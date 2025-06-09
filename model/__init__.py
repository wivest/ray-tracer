from .gltf_parser import *
from .material import *
from .setup import *
from .spatial import *
from .sphere import *
from .triangle import *

from typing import TypeAlias

# aliases
vec: TypeAlias = tuple[float, float, float]
basis: TypeAlias = tuple[vec, vec, vec]
