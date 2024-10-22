import random
from abc import ABC, abstractmethod


class Combat(ABC):
    """
    Combat ABC for combat gameplay.

    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """

    health: int
    damage: int

    @abstractmethod
    def get_name(self) -> str:
        """

        Return the name/description of the combatant
        (e.g., Player name or Enemy description).
        """
        pass

    def take_damage(self, damage: int) -> None:
        """
        Reduce health by the given damage
        and print a message.
        """
        self.health -= damage
        print(
            f"{self.get_name()} takes {damage} damage! "
            f"{self.get_name()} has {self.health} health remaining."
        )

    def is_alive(self) -> bool:
        """Return True if the entity is still alive (health > 0)."""
        return self.health > 0

    def attack(self, target: "Combat") -> None:
        """Attack the target and deal random damage."""
        if self.is_alive():
            damage_dealt = random.randint(
                int(self.damage * 0.8), self.damage
            )  # Random damage within range
            print(
                f"{self.get_name()} attacks {target.get_name()} for "
                f"{damage_dealt} damage!"
            )
            target.take_damage(damage_dealt)
