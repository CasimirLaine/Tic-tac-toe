import os

from tictactoe import config
from tictactoe.ai import AiPlayer
from tictactoe.game import Game
from tictactoe.player import Player


def render(text):
    clear_console()
    print(text)


def collect_input(game):
    print("Player: [" + game.get_player_with_turn().mark + "]\n")
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


def start():
    clear_console()
    player_1 = AiPlayer(config.MARK_PLAYER_1)
    player_2 = AiPlayer(config.MARK_PLAYER_2)
    game = Game(player_1, player_2)
    print("NEW GAME\n")
    render(game.grid.get_grid_string())
    while True:
        if game.is_game_over():
            break
        game.play_one_turn()
        render(game.grid.get_grid_string())
    print("GAME OVER!\n")
    if game.get_winner() is not None:
        print("Winner: " + game.get_winner().mark)
    else:
        print("Draw")


start()
