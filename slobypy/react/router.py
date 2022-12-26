from __future__ import annotations
from typing import Generator, Self


class SloRouter:
    """Used to define the route"""

    def __init__(self, curr_route: str) -> None:
            self.route = curr_route
            self._dynamic_routes: list[dict] = []
            self._check_dynamic_routes()

    def __truediv__(self, other: str) -> Self:
        """Add an endpoint and return a brand new SloRouter"""
        if self.route.endswith("/"):
            self.route += other

            return self.__get_object()

        else:
            self.route += "/" + other

            return self.__get_object()

    def __get_object(self) -> Self:
        """Used to return a SloRouter with the latest route"""
        obj = SloRouter(self.route)
        return obj

    def __str__(self) -> str:
        return self.route

    def _check_dynamic_routes(self):
        endpoints_as_list = self._endpoints_as_list()

        for item in endpoints_as_list:
            if item.startswith(":"):
                self._dynamic_routes.append({item: endpoints_as_list.index(item)})

    def endpoints_count(self) -> int:
        """Used to return the endpoints in an uri"""

        endpoints_count = 0
        endpoints = self._endpoints_as_list()

        for item in endpoints:
            if item != "":
                endpoints_count += 1

        return endpoints_count

    def dynamic_routes_iter(self) -> list:
        return self._dynamic_routes

    def _endpoints_as_list(self) -> list[str]:
        return self.route.split("/")

    def __iter__(self) -> Generator[int, None, None]:
        start = 0
        stop = self.endpoints_count()
        curr = start
        while curr < stop:
            yield self._endpoints_as_list()[curr]
            curr += 1
