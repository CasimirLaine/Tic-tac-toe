import math
import random

from . import config
from .grid import Cell
from .player import Player


class AiPlayer(Player):

    def __init__(self, mark):
        super(AiPlayer, self).__init__(mark)

    def move(self):
        if self.grid.is_full():
            return
        moves = self.__find_all_possible_moves()
        random.shuffle(moves)
        all_lines = self.grid.get_all_lines()
        moves.sort(key=lambda move: self.__sort_moves(move, all_lines))
        move = None
        if moves:
            move = moves[0]
        if move is not None:
            self.grid.set(move.x, move.y, self.mark)

    def __find_all_possible_moves(self):
        cells = []
        for x in range(config.GRID_SIZE):
            for y in range(config.GRID_SIZE):
                mark = self.grid.get(x, y)
                if mark == config.MARK_EMPTY:
                    cells.append(Cell(x, y, mark))
        return cells

    def __sort_moves(self, move, lines):
        best_value = self.__get_intrinsic_value(move)
        for line in lines:
            if move in line.cells:
                empty_count = line.count_marks(config.MARK_EMPTY)
                most_common_mark = line.get_most_common_mark()
                value = best_value
                if empty_count <= 0:
                    continue
                elif empty_count == 1:
                    if most_common_mark == self.mark:
                        value = 1
                    elif most_common_mark != config.MARK_EMPTY and most_common_mark is not None:
                        value = 2
                if best_value is None or value < best_value:
                    best_value = value
        return best_value if best_value is not None else 0

    def __get_intrinsic_value(self, move):
        if self.__is_center(move):
            return 5
        elif self.__is_corner(move):
            return 7
        else:
            return 8

    def __is_center(self, move):
        return move.x == move.y == math.floor(config.GRID_SIZE * 0.5)

    def __is_corner(self, move):
        return (move.x == 0 and (move.y == 0 or move.y == config.GRID_SIZE - 1)) \
               or (move.x == config.GRID_SIZE - 1 and (move.y == 0 or move.y == config.GRID_SIZE - 1))

    def __is_side(self, move):
        return not self.__is_center(move) and not self.__is_corner(move)
