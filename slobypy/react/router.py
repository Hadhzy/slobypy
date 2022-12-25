from __future__ import annotations
from typing import Generator


#Todo: Add dynamic feature
class SloRouter:
    """Used to define the route"""
    def __init__(self, route: str) -> None:
            self.route = route

    def __truediv__(self, other: str) -> None:

        if self.route.endswith("/"):
            self.route += other
        else:
            self.route += "/" + other

    def __str__(self) -> str:
        return self.route

    def endpoints_count(self) -> int:
        """Used to return the endpoints in an uri"""

        endpoints_count = 0
        endpoints = self._endpoints_as_list()

        for item in endpoints:
            if item != "":
                endpoints_count += 1

        return endpoints_count

    def _endpoints_as_list(self) -> list[str]:
        return self.route.split("/")

    def __iter__(self) -> Generator[int, None, None]:
        start = 0
        stop = self.endpoints_count()
        curr = start
        while curr < stop:
            yield self._endpoints_as_list()[curr]
            curr += 1
