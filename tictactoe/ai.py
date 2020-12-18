import math
import random

from . import config
from .grid import Cell
from .player import Player

_MOVE_VALUE_WIN = 1
_MOVE_VALUE_BLOCK_WIN = 2
_MOVE_VALUE_FORK = 3
_MOVE_VALUE_BLOCK_FORK = 4
_MOVE_VALUE_CENTER = 5
_MOVE_VALUE_OPPOSITE_CORNER = 6
_MOVE_VALUE_CORNER = 7
_MOVE_VALUE_SIDE = 8


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
        best_value = None
        non_blocked_lines = 0
        for line in lines:
            if move not in line.cells:
                continue
            empty_count = line.count_marks(config.MARK_EMPTY)
            most_common_mark = line.get_most_common_mark()
            if empty_count == 1:
                if most_common_mark == self.mark:
                    return _MOVE_VALUE_WIN
                elif self.__is_opponent(most_common_mark):
                    best_value = _MOVE_VALUE_BLOCK_WIN
            if best_value is None or best_value > _MOVE_VALUE_FORK:
                own_marks = line.count_marks(self.mark)
                if own_marks > 0 and empty_count + own_marks == config.GRID_SIZE:
                    non_blocked_lines += 1
                    if non_blocked_lines >= 2:
                        best_value = _MOVE_VALUE_FORK
            if best_value is None and self.__is_opposite_corner(move, line):
                best_value = _MOVE_VALUE_OPPOSITE_CORNER
        intrinsic_value = self.__get_intrinsic_value(move)
        return intrinsic_value if best_value is None or best_value > intrinsic_value else best_value

    def __get_intrinsic_value(self, move):
        if self.__is_center(move):
            return _MOVE_VALUE_CENTER
        elif self.__is_corner(move):
            return _MOVE_VALUE_CORNER
        else:
            return _MOVE_VALUE_SIDE

    def __is_center(self, move):
        return move.x == move.y == math.floor(config.GRID_SIZE * 0.5)

    def __is_opposite_corner(self, move, line):
        if not self.__is_corner(move):
            return False
        if not line.is_diagonal():
            return False
        for cell in line.cells:
            if self.__is_opponent(cell.mark) and self.__is_corner(cell):
                return True
        return False

    def __is_corner(self, move):
        return (move.x == 0 and (move.y == 0 or move.y == config.GRID_SIZE - 1)) \
               or (move.x == config.GRID_SIZE - 1 and (move.y == 0 or move.y == config.GRID_SIZE - 1))

    def __is_side(self, move):
        return not self.__is_center(move) and not self.__is_corner(move)

    def __is_opponent(self, mark):
        return mark != self.mark and mark != config.MARK_EMPTY and mark is not None
