from pydantic import BaseModel, Field, PrivateAttr, field_validator

from rpg.attackable import Combat
from rpg.door import Inspectable, Interactable
from rpg.jsonseri import JsonSerializable


class NPC(BaseModel, JsonSerializable, Inspectable, Interactable):
    """
    A class representing a non-player character (NPC).

    Attributes:
        description (str): The description of the NPC.
    """

    description: str = Field(...)

    def toJSON(self):
        """
        Serialize the NPC object to JSON.

        Returns:
            dict: A dictionary representation of the NPC object.
        """
        return {"description": self.description}

    def inspect(self) -> str:
        """
        Return a string description of the NPC.

        Returns:
            str: The description of the NPC.
        """
        return self.description

    def interact(self, player) -> None:
        """
        Interact with the player.

        Args:
            player: The player object to interact with.
        """
        print(f"{self.description} is uninterested in interacting right now.")

    @classmethod
    def fromJSON(cls, json_data):
        """
        Deserialize an NPC object from JSON.

        Args:
            json_data (dict): A dictionary representation of the NPC object.

        Returns:
            NPC: A deserialized NPC object.
        """
        return cls(description=json_data["description"])


class Enemy(NPC, Combat):
    """
    A class representing an enemy NPC.

    Attributes:
        _health (int): The health of the enemy.
        _damage (int): The damage the enemy can inflict.
    """

    _health: int = PrivateAttr(...)
    _damage: int = PrivateAttr(...)

    @field_validator("health")
    def validate_health(cls, value):
        """
        Validate the health value.

        Args:
            value (int): The health value to validate.

        Returns:
            int: The validated health value.

        Raises:
            ValueError: If the health value is less than or equal to 0.
        """
        if value <= 0:
            raise ValueError("Health must be greater than 0.")
        return value

    def toJSON(self):
        """
        Serialize the Enemy object to JSON.

        Returns:
            dict: A dictionary representation of the Enemy object.
        """
        return {
            "description": self.description,
            "health": self.health,
            "damage": self.damage,
        }

    @classmethod
    def fromJSON(cls, json_data):
        """
        Deserialize an Enemy object from JSON.

        Args:
            json_data (dict): A dictionary representation of the Enemy object.

        Returns:
            Enemy: A deserialized Enemy object.
        """
        return cls(
            description=json_data["description"],
            health=json_data["health"],
            damage=json_data["damage"],
        )

    def get_name(self) -> str:
        """
        Return the description of the enemy for combat messages.

        Returns:
            str: The description of the enemy.
        """
        return self.description


class Wizard(NPC):
    """
    A class representing a wizard NPC.

    Attributes:
        bonus_damage (int): The bonus damage the wizard can grant.
        healing_power (int): The healing power of the wizard.
    """

    bonus_damage: int = Field(...)
    healing_power: int = Field(...)

    def toJSON(self):
        """
        Serialize the Wizard object to JSON.

        Returns:
            dict: A dictionary representation of the Wizard object.
        """
        return {
            "description": self.description,
            "bonus_damage": self.bonus_damage,
            "healing_power": self.healing_power,
        }

    @classmethod
    def fromJSON(cls, json_data):
        """
        Deserialize a Wizard object from JSON.

        Args:
            json_data (dict): A dictionary representation of the Wizard object.

        Returns:
            Wizard: A deserialized Wizard object.
        """
        return cls(
            description=json_data["description"],
            bonus_damage=json_data["bonus_damage"],
            healing_power=json_data["healing_power"],
        )

    def give_bonus(self, player) -> None:
        """
        Grant a bonus to the player.

        Args:
            player: The player object to grant the bonus to.
        """
        print(f"{self.description} casts a spell on you!")
        player.health += self.healing_power
        player.damage += self.bonus_damage
        print(
            f"The wizard heals for {self.healing_power} health and grants you "
            f"{self.bonus_damage} bonus damage."
        )


class Room(BaseModel, JsonSerializable, Inspectable):
    """
    A class representing a room in the game.

    Attributes:
        description (str): The description of the room.
        doors (list): A list of doors in the room.
        npcs (list): A list of NPCs in the room.
        room_id (int): The unique identifier for the room.
    """

    description: str = Field(...)
    doors: list = []
    npcs: list = []
    room_id: int = None

    def __init__(self, **data):
        """
        Initialize a Room object.

        Args:
            **data: Arbitrary keyword arguments.
        """
        super().__init__(**data)
        self.room_id = id(self)

    def toJSON(self):
        """
        Serialize the Room object to JSON.

        Returns:
            dict: A dictionary representation of the Room object.
        """
        return {
            "description": self.description,
            "room_id": self.room_id,
            "doors": [door.toJSON() for door in self.doors],
            "npcs": [npc.toJSON() for npc in self.npcs],
        }

    def add_door(self, door):
        """
        Add a door to the room.

        Args:
            door: The door object to add.
        """
        self.doors.append(door)

    def add_npc(self, npc):
        """
        Add an NPC to the room.

        Args:
            npc: The NPC object to add.
        """
        self.npcs.append(npc)

    @classmethod
    def fromJSON(cls, json_data):
        """
        Deserialize a Room object from JSON.

        Args:
            json_data (dict): A dictionary representation of the Room object.

        Returns:
            Room: A deserialized Room object.
        """
        room = cls(description=json_data["description"])
        room.room_id = json_data["room_id"]  # Set room ID for lookup
        room.doors = []
        room.npcs = [NPC.fromJSON(npc) for npc in json_data["npcs"]]
        return room

    def inspect(self) -> str:
        """
        Return a string description of the room.

        Returns:
            str: The description of the room.
        """
        door_count = len(self.doors)
        npc_count = len(self.npcs)
        return (
            f"{self.description}. The room has {door_count} doors and "
            f"{npc_count} NPCs."
        )


class Player(BaseModel, JsonSerializable, Combat):
    """
    A class representing the player.

    Attributes:
        name (str): The name of the player.
        current_room (Room): The current room the player is in.
        health (int): The health of the player.
        damage (int): The damage the player can inflict.
    """

    name: str = Field(...)
    current_room: Room
    health: int = Field(default=100)
    damage: int = Field(default=20)

    def toJSON(self):
        """
        Serialize the Player object to JSON.

        Returns:
            dict: A dictionary representation of the Player object.
        """
        return {
            "name": self.name,
            "current_room": self.current_room.toJSON(),
            "health": self.health,
            "damage": self.damage,
        }

    @classmethod
    def fromJSON(cls, json_data):
        """
        Deserialize a Player object from JSON.

        Args:
            json_data (dict): A dictionary representation of the Player object.

        Returns:
            Player: A deserialized Player object.
        """
        return cls(
            name=json_data["name"],
            current_room=Room.fromJSON(json_data["current_room"]),
            health=json_data["health"],
            damage=json_data["damage"],
        )

    def change_room(self, new_room: Room) -> None:
        """
        Change the player's current room.

        Args:
            new_room (Room): The new room to move the player to.
        """
        self.current_room = new_room
        print(f"You are now in: {self.current_room.inspect()}")

    def get_name(self) -> str:
        """
        Return the name of the player for combat messages.

        Returns:
            str: The name of the player.
        """
        return self.name
