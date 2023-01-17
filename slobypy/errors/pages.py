
class Page404:
    def __init__(self, route="/"):
        self.message = f"{route} is empty"

    def show(self):
        return self.message
