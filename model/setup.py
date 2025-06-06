from camera.transform import Transform

# aliases
vec = tuple[float, float, float]
basis = tuple[vec, vec, vec]


class Setup:
    @staticmethod
    def get_camera_transform(path: str) -> Transform:
        with open(path) as file:
            lines = file.readlines()

        camera_pos: vec = (0.0, 0.0, 0.0)
        camera_bx: vec = (1.0, 0.0, 0.0)
        camera_by: vec = (0.0, 1.0, 0.0)
        camera_bz: vec = (0.0, 0.0, 1.0)

        for line in lines:
            tokens = line.split()
            key = tokens[0]

            if key == "cp":
                camera_pos = Setup.__parse_vec(tokens[1:])

            elif key == "bx":
                camera_bx = Setup.__parse_vec(tokens[1:])
            elif key == "by":
                camera_by = Setup.__parse_vec(tokens[1:])
            elif key == "bz":
                camera_bz = Setup.__parse_vec(tokens[1:])

        return Transform(camera_pos, (camera_bx, camera_by, camera_bz))

    @staticmethod
    def get_light(path: str):
        pass

    @staticmethod
    def __parse_vec(tokens: list[str]) -> vec:
        x = float(tokens[0])
        y = float(tokens[1])
        z = float(tokens[2])
        return (x, y, z)
