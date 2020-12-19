import math
import random

from . import config
from .grid import Cell
from .player import Player

_MOVE_VALUE_WIN = 1
_MOVE_VALUE_BLOCK_WIN = 2
_MOVE_VALUE_FORK = 3
_MOVE_VALUE_BLOCK_FORK_AND_BUILD = 4
_MOVE_VALUE_BLOCK_FORK = 5
_MOVE_VALUE_TWO_IN_A_ROW = 6
_MOVE_VALUE_CENTER = 7
_MOVE_VALUE_OPPOSITE_CORNER = 8
_MOVE_VALUE_CORNER = 9
_MOVE_VALUE_SIDE = 10


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
            print("Player:", self.mark, "Move value:", move.value)

    def __find_all_possible_moves(self):
        cells = []
        for x in range(config.GRID_SIZE):
            for y in range(config.GRID_SIZE):
                mark = self.grid.get(x, y)
                if mark == config.MARK_EMPTY:
                    cells.append(Cell(x, y, mark))
        return cells

    def __sort_moves(self, move, lines):
        move_value = MoveValue()
        for line in lines:
            if move not in line.cells:
                continue
            empty_count = line.count_marks(config.MARK_EMPTY)
            most_common_mark = line.get_most_common_mark()
            if empty_count == 1:
                if most_common_mark == self.mark:
                    move_value.update(_MOVE_VALUE_WIN)
                elif self.__is_opponent(most_common_mark):
                    move_value.update(_MOVE_VALUE_BLOCK_WIN)
            own_marks = line.count_marks(self.mark)
            if own_marks > 0 and empty_count + own_marks == config.GRID_SIZE:
                move_value.non_blocked_lines += 1
                for cell in line.cells:
                    if cell.mark == config.MARK_EMPTY and not move_value.does_create_opponent_fork:
                        move_value.does_create_opponent_fork = self.__does_create_opponent_fork(move, lines, cell)
            if own_marks == 0 and empty_count < config.GRID_SIZE:
                move_value.non_blocked_lines_opponent += 1
            if own_marks > 0 and empty_count > 1 and empty_count + own_marks == config.GRID_SIZE:
                move_value.update(_MOVE_VALUE_TWO_IN_A_ROW)
            if self.__is_opposite_corner(move, line):
                move_value.update(_MOVE_VALUE_OPPOSITE_CORNER)
        if move_value.non_blocked_lines >= 2:
            move_value.update(_MOVE_VALUE_FORK)
        if move_value.non_blocked_lines_opponent >= 2 and not move_value.does_create_opponent_fork:
            move_value.update(_MOVE_VALUE_BLOCK_FORK)
        if move_value.non_blocked_lines_opponent >= 2 and move_value.non_blocked_lines > 0 and not move_value.does_create_opponent_fork:
            move_value.update(_MOVE_VALUE_BLOCK_FORK_AND_BUILD)
        move_value.update(self.__get_intrinsic_value(move))
        move.value = move_value.value()
        return move_value.value()

    def __does_create_opponent_fork(self, move, lines, empty_cell):
        non_blocked_lines = 0
        for line in lines:
            if empty_cell not in line.cells:
                continue
            empty_count = line.count_marks(config.MARK_EMPTY)
            own_marks = line.count_marks(self.mark)
            for cell in line.cells:
                if cell.x == move.x and cell.y == move.y:
                    own_marks += 1
                    break
            if own_marks == 0 and empty_count < config.GRID_SIZE:
                non_blocked_lines += 1
                if non_blocked_lines >= 2:
                    return True
        return False

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


class MoveValue:

    def __init__(self):
        self.__value = None
        self.does_create_opponent_fork = False
        self.non_blocked_lines = 0
        self.non_blocked_lines_opponent = 0

    def value(self):
        return self.__value

    def update(self, value):
        if self.__value is None or self.__value > value:
            self.__value = value
