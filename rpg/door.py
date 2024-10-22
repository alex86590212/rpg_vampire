from abc import ABC, abstractmethod

from rpg.jsonseri import JsonSerializable


class Inspectable(ABC):
    """
    Abstract base class for objects that can be inspected.
    """

    @abstractmethod
    def inspect(self) -> str:
        """
        Return a string description of the object.
        """
        pass


class Interactable(ABC):
    """
    Abstract base class for objects that can interact with the player.
    """

    @abstractmethod
    def interact(self, player) -> None:
        """
        Interact with the player, modifying their state or environment.

        Args:
            player: The player object to interact with.
        """
        pass


class Door(Inspectable, Interactable, JsonSerializable):
    """
    A class representing a door that can be inspected and interacted with.

    Attributes:
        description (str): The description of the door.
        connected_room: The room connected to this door.
        opposite_room: The room opposite to this door.
    """

    def __init__(
                self,
                description: str,
                connected_room,
                opposite_room
                ) -> None:
        """
        Initialize a Door object.

        Args:
            description (str): The description of the door.
            connected_room: The room connected to this door.
            opposite_room: The room opposite to this door.
        """
        self.description = description
        self.connected_room = connected_room
        self.opposite_room = opposite_room

    def inspect(self) -> str:
        """
        Return a string description of the door.

        Returns:
            str: The description of the door.
        """
        return self.description

    def interact(self, player) -> None:
        """
        Interact with the player, changing their current room.

        Args:
            player: The player object to interact with.
        """
        if player.current_room == self.opposite_room:
            print(
                f"You go through the {self.description} and return to the "
                "previous room."
            )
            player.change_room(self.connected_room)
        else:
            print(f"You go through the {self.description}.")
            player.change_room(self.opposite_room)

    def toJSON(self):
        """
        Serialize the Door object by storing room as room IDs instead Room
        to avoid circular references.

        Returns:
            dict: A dictionary representation of the Door object.
        """
        return {
            "description": self.description,
            "connected_room_id": id(self.connected_room),
            "opposite_room_id": id(self.opposite_room),
        }

    @classmethod
    def fromJSON(cls, json_data, room_dict):
        """
        Deserialize a Door object by looking up rooms by their ID in room_dict.

        Args:
            json_data (dict): A dictionary representation of the Door object.
            room_dict (dict): A dictionary mapping room IDs to Room objects.

        Returns:
            Door: A deserialized Door object.
        """
        connected_room = room_dict.get(json_data["connected_room_id"])
        opposite_room = room_dict.get(json_data["opposite_room_id"])
        return cls(
            description=json_data["description"],
            connected_room=connected_room,
            opposite_room=opposite_room,
        )
