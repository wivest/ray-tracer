from imports.aliases import vec, basis

from pygltflib import GLTF2
from scipy.spatial.transform import Rotation

from camera.transform import Transform


FILENAME = "./scene/untitled.gltf"


def get_camera_data(path: str):
    data = GLTF2().load(path)
    if data == None:
        raise Exception()
    scene = data.scenes[data.scene]
    if scene.nodes == None:
        raise Exception()

    t = []
    r = []
    for i in scene.nodes:
        node = data.nodes[i]
        if node.camera != None:
            t = node.translation
            r = node.rotation

    if t == None or r == None:
        raise Exception()

    return __convert_transform(t, r)


def __convert_transform(translation: list[float], rotation: list[float]) -> Transform:
    if len(translation) != 3:
        raise Exception()

    origin = (translation[0], translation[1], translation[2])
    mat = Rotation.from_quat(rotation).as_matrix()
    bas = tuple(tuple(i) for i in mat.tolist())

    return Transform(origin, bas)  # type: ignore


def get_triangles(path: str):
    gltf = GLTF2().load(path)
    if gltf == None:
        raise Exception()

    primitives = gltf.meshes[0].primitives
    # from pypi docs
    accessor = gltf.accessors[primitives[0].attributes.POSITION]  # type: ignore
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    print(data)
