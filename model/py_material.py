from pygltflib import Material, PbrMetallicRoughness


class PyMaterial(dict[str, list[float]]):

    def __init__(self, material: Material | None = None):
        if material == None:
            material = Material()
        if material.pbrMetallicRoughness == None:
            material.pbrMetallicRoughness = PbrMetallicRoughness()
        diffuse = (material.pbrMetallicRoughness.baseColorFactor or [1, 1, 1])[:3]
        self["diffuse"] = diffuse
        spec = 1.0 - (material.pbrMetallicRoughness.roughnessFactor or 1.0)
        self["specular"] = [spec, spec, spec]
        self["emission"] = material.emissiveFactor or [0, 0, 0]
