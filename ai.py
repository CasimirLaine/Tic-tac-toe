import random
import config
from player import Player


class Ai(Player):

    def move(self):
        if self.grid.is_full():
            return
        x, y = self.__get_best_move(self.__get_almost_complete_lines())
        if x is None or y is None:
            x, y = self.__move_random()
        if x is not None and y is not None:
            self.grid.set(x, y, self.mark)

    def __move_random(self):
        x = random.randint(0, config.GRID_SIZE - 1)
        y = random.randint(0, config.GRID_SIZE - 1)
        if self.grid.is_occupied(x, y):
            return self.__move_random()
        return x, y

    def __get_almost_complete_lines(self):
        lines = []
        vertical_lines = self.grid.check_straight_lines(True, 1)
        if vertical_lines is not None:
            lines.extend(vertical_lines)
        horizontal_lines = self.grid.check_straight_lines(False, 1)
        if horizontal_lines is not None:
            lines.extend(horizontal_lines)
        top_diagonal_line = self.grid.check_diagonal_line(True, 1)
        if top_diagonal_line is not None:
            lines.append(top_diagonal_line)
        bottom_diagonal_line = self.grid.check_diagonal_line(False, 1)
        if bottom_diagonal_line is not None:
            lines.append(bottom_diagonal_line)
        return lines

    def __get_best_move(self, line_list):
        best_line = None
        for line in line_list:
            if line is None:
                continue
            if line.mark == self.mark:
                best_line = line
                break
            if best_line is None:
                best_line = line
        if best_line is None:
            return None, None
        cells = best_line.cells
        for cell in cells:
            if cell.mark == config.MARK_EMPTY:
                return cell.x, cell.y
        return None, None
