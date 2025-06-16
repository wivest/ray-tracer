from imports.aliases import vec, basis

from pygltflib import GLTF2


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

    print(f"TRANSLATION: {t}")
    print(f"ROTATION: {r}")

    if t == None or r == None:
        raise Exception()

    return __convert_transform(t, r)


def __convert_transform(
    translation: list[float], rotation: list[float]
) -> tuple[vec, basis]:
    if len(translation) != 3:
        raise Exception()

    origin = (translation[0], translation[1], translation[2])

    return origin, basis()
