from rpg.io_utils import Game, Scanner


def main():
    Scanner.simulated_inputs = [1, 0, 2, 1, 0, 0]

    game = Game()
    game.main_loop()


if __name__ == "__main__":
    main()
