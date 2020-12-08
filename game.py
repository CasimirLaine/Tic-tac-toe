import config
from grid import Grid


class Game:
    def __init__(self, player1, player2, print_function):
        self.grid = Grid()
        self.turns = 0
        self.player_1 = player1
        self.player_2 = player2
        self.player_1.grid = self.grid
        self.player_2.grid = self.grid
        self.player_with_turn = self.player_1
        self.print_function = print_function

    def play(self):
        self.print_function(self.grid.getGridString())
        while True:
            self.player_with_turn.move()
            self.print_function(self.grid.getGridString())
            if self.turns + 1 >= config.GRID_SIZE * 2 - 1 and self.grid.has_full_row():
                break
            if self.grid.is_full():
                break
            self.change_turn()

    def change_turn(self):
        self.turns += 1
        if self.player_with_turn == self.player_1:
            self.player_with_turn = self.player_2
        else:
            self.player_with_turn = self.player_1
