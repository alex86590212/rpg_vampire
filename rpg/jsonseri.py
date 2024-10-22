import json
from abc import ABC, abstractmethod


class JsonSerializable(ABC):
    """

    Class that allows for serilization to JSON
    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """

    @abstractmethod
    def toJSON(self):
        """
        Converts the object's attributes to a dictionary
         that can be serialized into JSON.

        """
        pass

    @abstractmethod
    def fromJSON(cls, json_dict):
        """
        Recreate an instance of the class from a dictionary (parsed from JSON).
        Handles nested JsonSerializable objects recursively.
        """
        pass

    def save(self, filename):
        """
        Saves the object to a JSON file.
        """
        with open(filename, "w") as f:
            json.dump(self.toJSON(), f, indent=4)

    @classmethod
    def load(cls, filename):
        """
        Loads a JSON file and converts it back into an instance of the class.
        """
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.fromJSON(data)
