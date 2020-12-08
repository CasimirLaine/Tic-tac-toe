import os

from . import config
from .ai import AiPlayer
from .game import Game
from .player import Player


def render(text):
    clear_console()
    print(text)


def collect_input():
    print("Player: [" + game.player_with_turn.mark + "]\n")
    col = collect_integer("\tCol: ")
    row = collect_integer("\tRow: ")
    return col, row


def collect_integer(text):
    value = None
    while type(value) is not int:
        try:
            value = int(input(text))
        except ValueError:
            print("Please enter an integer!")
            pass
    return value


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[H\033[J")


clear_console()
player_1 = Player(config.MARK_PLAYER_1, collect_input)
player_2 = AiPlayer(config.MARK_PLAYER_2)
game = Game(player_1, player_2, render)
print("NEW GAME\n")
game.play()
print("GAME OVER!\n")
if game.turns + 1 >= config.GRID_SIZE * 2 - 1 and game.grid.has_full_row():
    print("\tWinner: " + game.player_with_turn.mark)
if game.grid.is_full():
    print("Draw")
