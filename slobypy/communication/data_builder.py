from __future__ import annotations
# This project
from slobypy.react import Design
# Built-in
import json
from typing import Self


class DataBuilder:
    """
    This class is build the data for the frontend.
    """
    __JSON_DATA = ""  # Todo: Type hint here

    def make_scss_data(self) -> Self:
        """
        This method is used to create the scss data.
        """

        for scss_group in Design.get_registered_groups():
            self.__JSON_DATA += json.dumps(scss_group)  # add the scss groups to the json data

        for scss_class in Design.get_registered_classes():
            self.__JSON_DATA += json.dumps(scss_class)  # add the scss class to the json data

        return self

    def make_app_component_data(self, components_data: str) -> Self:
        """
        This method is used to create the app-component data.
        ### Arguments
        components_data: str
        ### Returns
        value: None
        """

        self.__JSON_DATA += json.dumps(components_data)  # add the component_data to the json data based on the app render

        return self

    def send(self):
        """
        Send the json data to the frontend
        """

        return self
