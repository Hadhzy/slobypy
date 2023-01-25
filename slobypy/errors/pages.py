class Page404:
    def __init__(self, route: str = "/") -> None:
        self.message = f"{route} is empty"

    def show(self) -> str:
        return self.message
