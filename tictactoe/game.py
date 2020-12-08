from tictactoe import config
from .grid import Grid


class Game:
    def __init__(self, player1, player2, grid_array=None):
        if grid_array is not None:
            self.turns = len(grid_array) - grid_array.count(config.MARK_EMPTY)
        else:
            self.turns = 0
        self.grid = Grid(grid_array)
        self.player_1 = player1
        self.player_2 = player2
        self.player_1.grid = self.grid
        self.player_2.grid = self.grid
        self.player_with_turn = self.player_1

    def play_one_turn(self):
        if self.is_game_over():
            return
        self.player_with_turn.move()
        if not self.is_game_over() and self.turns < self.grid.count_occupied():
            self.__change_turn()

    def __change_turn(self):
        if self.is_game_over():
            return
        self.turns += 1
        if self.player_with_turn == self.player_1:
            self.player_with_turn = self.player_2
        else:
            self.player_with_turn = self.player_1

    def is_game_over(self):
        return self.grid.has_full_row() or self.grid.is_full()

    def get_winner(self):
        return self.player_with_turn if self.grid.has_full_row() else None
