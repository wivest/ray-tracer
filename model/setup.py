# aliases
vec = tuple[float, float, float]
basis = tuple[vec, vec, vec]


class Setup:
    @staticmethod
    def get_camera(path: str) -> tuple[vec, basis]:
        with open(path) as file:
            lines = file.readlines()

        camera_pos: vec = (0.0, 0.0, 0.0)
        camera_basis: basis = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))

        for line in lines:
            tokens = line.split()
            key = tokens[0]

            if key == "cp":
                x = float(tokens[1])
                y = float(tokens[2])
                z = float(tokens[3])
                camera_pos = (x, y, z)

        return camera_pos, camera_basis

    @staticmethod
    def get_light(path: str):
        pass
