import sys
import random
import config
from grid import Cell
from player import Player


class AiPlayer(Player):

    def move(self):
        if self.grid.is_full():
            return
        moves = self.__find_all_possible_moves()
        random.shuffle(moves)
        moves.sort(key=lambda move: self.__sort_moves(move, self.grid.get_all_lines()))
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
        for line in lines:
            if move in line.cells:
                empty_count = line.count_marks(config.MARK_EMPTY)
                if empty_count <= 0:
                    continue
                value = empty_count * 4
                most_common_mark = line.get_most_common_mark()
                value += self.__sort_marks(most_common_mark)
                if best_value is None or value < best_value:
                    best_value = value
        return best_value if best_value is not None else 0

    def __sort_marks(self, mark):
        if mark == self.mark:
            return 0
        elif mark == config.MARK_EMPTY:
            return 2
        elif mark is None:
            return 3
        else:
            return 1
