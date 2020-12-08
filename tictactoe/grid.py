from . import config


class Grid:
    def __init__(self, grid_array=None):
        if grid_array is None:
            self.grid_array = [config.MARK_EMPTY] * config.GRID_SIZE ** 2
        else:
            self.grid_array = grid_array

    def __len__(self):
        return len(self.grid_array)

    def get_grid_string(self):
        grid_string = (config.MARK_BORDER_HORIZONTAL * (2 * config.GRID_SIZE + 1)) + "\n"
        index = 0
        while index < len(self.grid_array):
            row = self.grid_array[index:index + config.GRID_SIZE]
            grid_string += config.MARK_BORDER_VERTICAL + config.MARK_BORDER_VERTICAL.join(
                row) + config.MARK_BORDER_VERTICAL + "\n"
            if index != len(self.grid_array) - config.GRID_SIZE:
                grid_string += ((config.MARK_BORDER_HORIZONTAL + config.MARK_BORDER_CORNER) *
                               config.GRID_SIZE + config.MARK_BORDER_HORIZONTAL) + "\n"
            index += config.GRID_SIZE
        grid_string += (config.MARK_BORDER_HORIZONTAL * (2 * config.GRID_SIZE + 1)) + "\n"
        return grid_string

    def get_all_lines(self):
        lines = []
        lines.extend(self.get_all_straight_lines(True))
        lines.extend(self.get_all_straight_lines(False))
        lines.append(self.get_diagonal_line(True))
        lines.append(self.get_diagonal_line(False))
        return lines

    def get_all_straight_lines(self, vertical):
        line_list = []
        axis_1 = 0
        while axis_1 < config.GRID_SIZE:
            axis_2 = 0
            cells = []
            while axis_2 < config.GRID_SIZE:
                x = axis_1 if vertical else axis_2
                y = axis_2 if vertical else axis_1
                value = self.get(x, y)
                cells.append(Cell(x, y, value))
                axis_2 += 1
            line_list.append(Line(cells))
            axis_1 += 1
        return line_list

    def get_diagonal_line(self, top):
        check_x = 0
        check_y = 0 if top else config.GRID_SIZE - 1
        cells = []
        while check_x < config.GRID_SIZE and check_y < config.GRID_SIZE:
            value = self.get(check_x, check_y)
            cells.append(Cell(check_x, check_y, value))
            check_x += 1
            check_y += 1 if top else -1
        return Line(cells)

    def has_full_row(self):
        if self.count_occupied() < config.GRID_SIZE:
            return False
        line_list = self.get_all_lines()
        for line in line_list:
            if line.is_full():
                return True
        return False

    def get(self, x, y):
        index = y * config.GRID_SIZE + x
        return self.grid_array[index]

    def set(self, x, y, mark):
        index = y * config.GRID_SIZE + x
        if index < 0 or index >= len(self.grid_array):
            return False
        value = self.grid_array[index]
        if value is config.MARK_EMPTY or config.CELL_REWRITE_ALLOWED:
            self.grid_array[index] = mark
            return True
        return False

    def is_occupied_index(self, index):
        return self.grid_array[index] != config.MARK_EMPTY

    def is_occupied(self, x, y):
        return self.is_occupied_index(y * config.GRID_SIZE + x)

    def is_full(self):
        return config.MARK_EMPTY not in self.grid_array

    def is_empty(self):
        for item in self.grid_array:
            if item != config.MARK_EMPTY:
                return False
        return True

    def count_occupied(self):
        return len(self.grid_array) - self.grid_array.count(config.MARK_EMPTY)


class Line:
    def __init__(self, cells):
        self.cells = cells

    def get_most_common_mark(self):
        mark_map = {}
        for cell in self.cells:
            count = mark_map.get(cell.mark)
            if count is None:
                count = 0
            count += 1
            mark_map.update({cell.mark: count})
        most_common_mark = None
        most_common_mark_count = 0
        for key, value in mark_map.items():
            if value > most_common_mark_count:
                most_common_mark = key
                most_common_mark_count = value
            elif value == most_common_mark_count:
                most_common_mark = None
        return most_common_mark

    def count_marks(self, mark):
        count = 0
        for cell in self.cells:
            if mark == cell.mark:
                count += 1
        return count

    def is_full(self):
        mark = config.MARK_EMPTY
        for cell in self.cells:
            if cell.mark == config.MARK_EMPTY:
                return False
            elif mark == config.MARK_EMPTY:
                mark = cell.mark
            elif mark != cell.mark:
                return False
        return True


class Cell:
    def __init__(self, x, y, mark):
        self.x = x
        self.y = y
        self.mark = mark

    def __eq__(self, other):
        return isinstance(other, Cell) and other.x == self.x and other.y == self.y and other.mark == self.mark
