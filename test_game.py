import unittest

from rpg.room import Enemy, Player, Room, Wizard


class TestPlayer(unittest.TestCase):
    """
    Unit tests for the Player class.
    """

    def setUp(self):
        """
        Set up a test player and room for each test.
        """
        self.room = Room(description="Test Room")
        self.player = Player(
                            name="Hero",
                            current_room=self.room,
                            health=100,
                            damage=20
                            )

    def test_player_creation(self):
        """
        Test that a player is created with the correct attributes.
        """
        self.assertEqual(self.player.name, "Hero")
        self.assertEqual(self.player.health, 100)
        self.assertEqual(self.player.damage, 20)

    def test_player_change_room(self):
        """
        Test that a player can change rooms.
        """
        new_room = Room(description="New Room")
        self.player.change_room(new_room)
        self.assertEqual(self.player.current_room, new_room)

    def test_player_take_damage(self):
        """
        Test that a player takes damage correctly.
        """
        self.player.take_damage(10)
        self.assertEqual(self.player.health, 90)


class TestEnemy(unittest.TestCase):
    """
    Unit tests for the Enemy class.
    """

    def setUp(self):
        """
        Set up a test enemy for each test.
        """
        self.enemy = Enemy(description="Goblin", health=50, damage=15)

    def test_enemy_creation(self):
        """
        Test that an enemy is created with the correct attributes.
        """
        self.assertEqual(self.enemy.description, "Goblin")
        self.assertEqual(self.enemy.health, 50)

    def test_enemy_take_damage(self):
        """
        Test that an enemy takes damage correctly.
        """
        self.enemy.take_damage(20)
        self.assertEqual(self.enemy.health, 30)

    def test_enemy_is_alive(self):
        """
        Test that the enemy's alive status is correctly updated.
        """
        self.assertTrue(self.enemy.is_alive())
        self.enemy.take_damage(50)
        self.assertFalse(self.enemy.is_alive())


class TestWizard(unittest.TestCase):
    """
    Unit tests for the Wizard class.
    """

    def setUp(self):
        """
        Set up a test wizard and room for each test.
        """
        self.wizard = Wizard(
            description="Old Wizard", bonus_damage=10, healing_power=20
        )
        self.room = Room(description="Wizard Room")

    def test_wizard_creation(self):
        """
        Test that a wizard is created with the correct attributes.
        """
        self.assertEqual(self.wizard.description, "Old Wizard")
        self.assertEqual(self.wizard.bonus_damage, 10)
        self.assertEqual(self.wizard.healing_power, 20)

    def test_wizard_give_bonus(self):
        """
        Test that a wizard can give a bonus to a player.
        """
        player = Player(name="Hero",
                        current_room=self.room,
                        health=100,
                        damage=20
                        )
        self.wizard.give_bonus(player)
        self.assertEqual(player.health, 120)
        self.assertEqual(player.damage, 30)


class TestGameIntegration(unittest.TestCase):
    """
    Integration tests for the game components.
    """

    def setUp(self):
        """
        Set up test rooms, player, enemy, and wizard for each test.
        """
        self.room1 = Room(description="Room 1")
        self.room2 = Room(description="Room 2")
        self.player = Player(
            name="Hero", current_room=self.room1, health=100, damage=20
        )
        self.enemy = Enemy(description="Goblin", health=50, damage=10)
        self.wizard = Wizard(
            description="Old Wizard", bonus_damage=10, healing_power=30
        )

        self.room1.add_npc(self.enemy)
        self.room2.add_npc(self.wizard)

    def test_player_move_between_rooms(self):
        """
        Test that a player can move between rooms.
        """
        self.player.change_room(self.room2)
        self.assertEqual(self.player.current_room.description, "Room 2")

    def test_combat_with_enemy(self):
        """
        Test that a player can engage in combat with an enemy.
        """
        self.player.attack(self.enemy)
        self.assertLess(self.enemy.health, 50)

    def test_interact_with_wizard(self):
        """
        Test that a player can interact with a wizard.
        """
        self.wizard.give_bonus(self.player)
        self.assertEqual(self.player.health, 130)
        self.assertEqual(self.player.damage, 30)

    def test_combat_with_death(self):
        """
        Test that an enemy can be killed in combat.
        """
        self.enemy.take_damage(50)
        self.assertFalse(self.enemy.is_alive())


class TestGameFunctional(unittest.TestCase):
    """
    Functional tests for the full game flow.
    """

    def test_full_game(self):
        """
        Test a full game scenario with room changes, interactions, and combat.
        """
        room1 = Room(description="Start Room")
        room2 = Room(description="End Room")
        player = Player(name="Hero", current_room=room1, health=100, damage=20)
        enemy = Enemy(description="Dragon", health=100, damage=25)
        wizard = Wizard(description="Helpful Wizard",
                        bonus_damage=10,
                        healing_power=50
                        )

        room1.add_npc(enemy)
        room2.add_npc(wizard)

        player.change_room(room2)
        self.assertEqual(player.current_room, room2)

        wizard.give_bonus(player)
        self.assertEqual(player.health, 150)
        self.assertEqual(player.damage, 30)

        player.change_room(room1)
        while enemy.is_alive() and player.is_alive():
            player.attack(enemy)
            if enemy.is_alive():
                enemy.attack(player)

        self.assertTrue(player.is_alive())
        self.assertFalse(enemy.is_alive())
