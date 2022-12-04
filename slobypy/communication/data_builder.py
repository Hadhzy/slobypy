# pylint: disable=unused-private-member

from __future__ import annotations

# Built-in
import json
from typing import Self

# This project
from slobypy.react import Design


class DataBuilder:
    """
    This class is build the data for the frontend.
    """
    # Todo: Type hint here
    __JSON_DATA: str = ""  # pylint: disable=invalid-name

    def make_scss_data(self) -> Self:
        """
        This method is used to create the scss data.
        """

        for scss_data in Design.USED_CLASSES:
            self.__JSON_DATA += json.dumps(scss_data)  # add the scss data to the json.

        return self

    def make_app_component_data(self, components_data: str) -> Self:
        """
        This method is used to create the app-component data.
        ### Arguments
        components_data: str
        ### Returns
        value: None
        """

        self.__JSON_DATA += json.dumps(
            components_data)  # add the component_data to the json data based on the app render

        return self

    def get_json(self) -> str:
        """
        Send the json data to the frontend
        """

        return self.__JSON_DATA
