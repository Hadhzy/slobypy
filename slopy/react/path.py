
class Path:
    PATHS = []

    def __init__(self, path) -> None:
        self.path = path

    @classmethod
    def add_path(cls, path):
        cls.PATHS.append(path)

    def __call__(self, component):
        self.add_path({component: self.path})