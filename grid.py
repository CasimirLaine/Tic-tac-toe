import config


class Grid:
    def __init__(self):
        self.grid_array = [config.MARK_EMPTY] * config.GRID_SIZE ** 2

    def __len__(self):
        return len(self.grid_array)

    def print_grid(self):
        index = 0
        print config.MARK_BORDER_HORIZONTAL * (2 * config.GRID_SIZE + 1)
        while index < len(self.grid_array):
            row = self.grid_array[index:index + config.GRID_SIZE]
            print config.MARK_BORDER_VERTICAL + config.MARK_BORDER_VERTICAL.join(row) + config.MARK_BORDER_VERTICAL
            if index != len(self.grid_array) - config.GRID_SIZE:
                print (
                              config.MARK_BORDER_HORIZONTAL + config.MARK_BORDER_CORNER
                      ) * config.GRID_SIZE + config.MARK_BORDER_HORIZONTAL
            index += config.GRID_SIZE
        print config.MARK_BORDER_HORIZONTAL * (2 * config.GRID_SIZE + 1)

    def has_full_row(self):
        return (self.check_straight_lines(True, 0) is not None
                or self.check_straight_lines(False, 0) is not None
                or self.check_diagonal_line(True, 0) is not None
                or self.check_diagonal_line(False, 0) is not None)

    def check_straight_lines(self, vertical, expect_empty_count):
        line_list = []
        axis_1 = 0
        while axis_1 < config.GRID_SIZE:
            axis_2 = 0
            first_value = config.MARK_EMPTY
            full_row = True
            empty_count = 0
            cells = []
            while axis_2 < config.GRID_SIZE:
                x = axis_1 if vertical else axis_2
                y = axis_2 if vertical else axis_1
                value = self.get(x, y)
                cells.append(Cell(x, y, value))
                if first_value == config.MARK_EMPTY:
                    first_value = value
                if value == config.MARK_EMPTY:
                    empty_count += 1
                if empty_count > expect_empty_count or (value != config.MARK_EMPTY and value != first_value):
                    full_row = False
                    break
                axis_2 += 1
            if full_row and empty_count == expect_empty_count:
                line_list.append(Line(first_value, cells))
            axis_1 += 1
        return line_list if line_list else None

    def check_diagonal_line(self, top, expect_empty_count):
        check_x = 0
        check_y = 0 if top else config.GRID_SIZE - 1
        first_value = config.MARK_EMPTY
        empty_count = 0
        cells = []
        while check_x < config.GRID_SIZE and check_y < config.GRID_SIZE:
            value = self.get(check_x, check_y)
            cells.append(Cell(check_x, check_y, value))
            if first_value == config.MARK_EMPTY:
                first_value = value
            if value == config.MARK_EMPTY:
                empty_count += 1
            if empty_count > expect_empty_count or (value != config.MARK_EMPTY and value != first_value):
                return None
            check_x += 1
            check_y += 1 if top else -1
        if empty_count == expect_empty_count:
            return Line(first_value, cells)
        else:
            return None

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
    def __init__(self, mark, cells):
        self.mark = mark
        self.cells = cells


class Cell:
    def __init__(self, x, y, mark):
        self.x = x
        self.y = y
        self.mark = mark
