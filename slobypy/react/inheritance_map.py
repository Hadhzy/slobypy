
class SlobyPyInheritanceMap:
    inheritance_map: dict = {}

    def __init__(self) -> None:
       pass

    def add_element(self, tag: str, classNames: list):

        self.inheritance_map[f"{tag}{classNames}"] = f""

    def __str__(self) -> str:
        return f"{self.inheritance_map}"