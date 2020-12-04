import os

import config
from ai import AiPlayer
from grid import Grid
from player import Player


class Game:
    def __init__(self):
        self.grid = Grid()
        self.turns = 0
        self.player_1 = Player(config.MARK_PLAYER_1, self.grid)
        self.player_2 = AiPlayer(config.MARK_PLAYER_2, self.grid)
        self.player_with_turn = self.player_1

    def play(self):
        print "NEW GAME\n"
        self.grid.print_grid()
        while True:
            self.player_with_turn.move()
            clear_console()
            self.grid.print_grid()
            if self.turns + 1 >= config.GRID_SIZE * 2 - 1 and self.grid.has_full_row():
                print "GAME OVER!\n"
                print "\tWinner: " + self.player_with_turn.mark
                break
            if self.grid.is_full():
                print "GAME OVER!\n"
                print "Draw"
                break
            self.change_turn()

    def change_turn(self):
        self.turns += 1
        if self.player_with_turn == self.player_1:
            self.player_with_turn = self.player_2
        else:
            self.player_with_turn = self.player_1


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
    print "\033[H\033[J"


game = Game()
game.play()
