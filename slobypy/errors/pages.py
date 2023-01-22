
class Page404:
    def __init__(self, route="/") -> None:
        self.message = f"{route} is empty"

    def show(self) -> str:
        return self.message
