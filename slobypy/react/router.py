from __future__ import annotations


#Todo: Add support for multiple /
class SloRouter:
    """Used to define the route"""
    def __init__(self, route: str) -> None:
        self.route = route

    def __truediv__(self, other: str) -> None:

        try:
            if self.route.endswith("/"):
                self.route += other
            else:
                self.route += "/" + other
        except:
            if isinstance(other, SloRouter):
                self.route = other.route

