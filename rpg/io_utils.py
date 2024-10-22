import json
import os

from rpg.door import Door
from rpg.jsonseri import JsonSerializable
from rpg.room import NPC, Enemy, Player, Room, Wizard


class Scanner:
    """
    A utility class for reading integer input.

    Attributes:
        simulated_inputs (list): A list of simulated inputs.
        current_index (int): The current index in the simulated inputs list.
    """

    simulated_inputs = []
    current_index = 0

    @staticmethod
    def read_int(prompt: str) -> int:
        """
        Read an integer from user input or from
        simulated inputs if EOFError is encountered.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            int: The integer input by the user or from simulated inputs.
        """
        try:
            return int(input(prompt))
        except EOFError:
            if Scanner.current_index < len(Scanner.simulated_inputs):
                simulated_input = Scanner.simulated_inputs[
                    Scanner.current_index
                    ]
                Scanner.current_index += 1
                return simulated_input
        except ValueError:
            return Scanner.read_int(prompt)


class Saver:
    """
    A utility class for saving and loading game state.
    """

    save_dir = "savedgames"
    save_file = "quicksave.json"

    @staticmethod
    def ensure_save_directory():
        """
        Ensure the savedgames directory exists.
        """
        if not os.path.isdir(Saver.save_dir):
            os.makedirs(Saver.save_dir)
            print(f"Directory '{Saver.save_dir}' created.")

    @staticmethod
    def quicksave(game):
        """
        Save the game state to quicksave.json.

        Args:
            game: The game object to save.
        """
        try:
            Saver.ensure_save_directory()
            save_path = os.path.join(Saver.save_dir, Saver.save_file)
            with open(save_path, "w") as save_file:
                json.dump(game.toJSON(), save_file, indent=4)
            print("Game successfully saved!")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

    @staticmethod
    def quickload():
        """
        Load the game state from quicksave.json.

        Returns:
            dict: The loaded game data.
        """
        try:
            save_path = os.path.join(Saver.save_dir, Saver.save_file)
            if not os.path.exists(save_path):
                raise FileNotFoundError("Save file not found.")
            with open(save_path, "r") as load_file:
                game_data = json.load(load_file)
            print("Game successfully loaded!")
            return game_data
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError:
            print("Error: The save file is not in valid JSON format.")
        except Exception as e:
            print(f"An error occurred while loading the game: {e}")
        return None


class Game(JsonSerializable):
    """
    A class representing the game state.

    Attributes:
        rooms (dict): A dictionary of rooms by their room_id.
        player (Player): The player object.
    """

    def __init__(self):
        """
        Initialize the game state.
        """
        self.rooms = {}

        self.initial_room = Room(
            description="A dusty room full of old computers."
            )
        self.second_room = Room(description="A dark room with dark doors.")

        self.rooms[self.initial_room.room_id] = self.initial_room
        self.rooms[self.second_room.room_id] = self.second_room

        self.player = Player(
            name="Matthew",
            current_room=self.initial_room,
            health=100,
            damage=20
        )

        door1 = Door(
            description="A mysterious red door.",
            connected_room=self.second_room,
            opposite_room=self.initial_room,
        )
        door2 = Door(
            description="A black door with a keypad.",
            connected_room=self.second_room,
            opposite_room=self.initial_room,
        )

        self.initial_room.add_door(door1)
        self.initial_room.add_door(door2)
        self.second_room.add_door(door1)
        self.second_room.add_door(door2)

        npc1 = NPC(description="A suspiciously happy looking orc")
        npc2 = Enemy(description="A fierce goblin", health=50, damage=15)
        npc3 = NPC(description="The kerstman")
        npc4 = Enemy(description="A dangerous vampire", health=60, damage=100)
        wizard = Wizard(
            description="A wise old wizard", bonus_damage=10, healing_power=30
        )

        self.initial_room.add_npc(npc1)
        self.initial_room.add_npc(npc2)
        self.second_room.add_npc(npc3)
        self.second_room.add_npc(npc4)
        self.second_room.add_npc(wizard)

    def main_loop(self) -> None:
        """
        The main game loop.
        """
        vampire_defeated = False

        while self.player.is_alive() and not vampire_defeated:
            self.show_main_menu()

            for room in self.rooms.values():
                for npc in room.npcs:
                    if (
                        isinstance(npc, Enemy)
                        and npc.description == "A dangerous vampire"
                        and not npc.is_alive()
                    ):
                        vampire_defeated = True
                        break
                if vampire_defeated:
                    break

        if vampire_defeated:
            print("Congratulations! You won the game!")
        else:
            print("Game Over! You have died.")

    def toJSON(self):
        """
        Serialize the game state to JSON.

        Returns:
            dict: A dictionary representation of the game state.
        """
        return {
            "rooms": {
                room_id: room.toJSON() for room_id,
                room in self.rooms.items()
                },
            "player": self.player.toJSON(),
        }

    @classmethod
    def fromJSON(cls, json_data):
        """
        Deserialize the game state from JSON.

        Args:
            json_data (dict): A dictionary representation of the game state.

        Returns:
            Game: A deserialized Game object.
        """
        game = cls.__new__(cls)
        game.rooms = {}
        for room_data in json_data["rooms"].values():
            room = Room.fromJSON(room_data)
            game.rooms[room.room_id] = room

        for room in game.rooms.values():
            for door in room.doors:
                door.connected_room = game.rooms.get(door.connected_room_id)
                door.opposite_room = game.rooms.get(door.opposite_room_id)

        game.player = Player.fromJSON(json_data["player"])
        return game

    def show_main_menu(self) -> None:
        """
        Display the main menu and handle user input.
        """
        print("\nWhat do you want to do?")
        print("  (0) Look around")
        print("  (1) Look for a way out")
        print("  (2) Look for company")
        print("  (3) QuickSave")
        print("  (4) QuickLoad")

        choice = Scanner.read_int("Enter your choice: ")

        if choice == 0:
            print(f"\nYou see: {self.player.current_room.inspect()}")
        elif choice == 1:
            self.look_for_way_out()
        elif choice == 2:
            self.look_for_company()
        elif choice == 3:
            print("Saving game....")
            Saver.quicksave(self)
        elif choice == 4:
            print("Loading game...")
            loaded_data = Saver.quickload()
            if loaded_data:
                loaded_game = Game.fromJSON(loaded_data)
                self.__dict__.update(loaded_game.__dict__)
                print("Game successfully loaded. Resuming from saved state.")
        else:
            print("Invalid choice. Please try again.")

    def look_for_way_out(self) -> None:
        """
        Look for a way out by inspecting doors in the current room.
        """
        doors = self.player.current_room.doors
        if not doors:
            print("There are no doors in this room.")
            return

        print("\nYou look around for doors. You see:")
        for index, door in enumerate(doors):
            print(f"  ({index}) {door.inspect()}")

        choice = Scanner.read_int(
            "\nWhich door do you take? (-1 : stay here): "
            )

        if 0 <= choice < len(doors):
            doors[choice].interact(self.player)  # Go through the selected door
        elif choice == -1:
            print("You decide to stay in the room.")
        else:
            print("Invalid choice. Returning to the main menu.")

    def look_for_company(self) -> None:
        """
        Look for company by inspecting NPCs in the current room.
        """
        npcs = self.player.current_room.npcs
        if not npcs:
            print("There is no one here.")
            return

        print("\nYou look if there’s someone here. You see:")
        for index, npc in enumerate(npcs):
            print(f"  ({index}) {npc.inspect()}")

        choice = Scanner.read_int("\nInteract with? (-1 : do nothing): ")

        if 0 <= choice < len(npcs):
            if isinstance(npcs[choice], Enemy):
                self.combat(npcs[choice])
            elif isinstance(npcs[choice], Wizard):
                npcs[choice].give_bonus(self.player)
                npcs[choice].interact(self.player)
        elif choice == -1:
            print("You decide to do nothing.")
        else:
            print("Invalid choice. Returning to the main menu.")

    def combat(self, enemy: Enemy) -> None:
        """
        Engage in combat with an enemy.

        Args:
            enemy (Enemy): The enemy to fight.
        """
        print(f"\nCombat started with {enemy.description}!")
        while self.player.is_alive() and enemy.is_alive():
            print("\nWhat do you want to do?")
            print("  (0) Attack")
            print("  (1) Run away")
            choice = Scanner.read_int("Enter your choice: ")

            if choice == 0:
                self.player.attack(enemy)
                if enemy.is_alive():
                    enemy.attack(self.player)
                else:
                    print(f"{enemy.description} has been defeated!")
                    self.player.current_room.npcs.remove(
                        enemy
                    )  # Remove enemy from NPC list
            elif choice == 1:
                print("You ran away!")
                break
            else:
                print("Invalid choice.")
