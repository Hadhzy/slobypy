
class Path:
    PATH = []
    def __init__(self, path) -> None:
        self.path = path

    @classmethod
    def add_path(cls, path):
        cls.PATH.append(path)

    def __call__(self, component):
        self.add_path({component: self.path})