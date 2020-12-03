EMPTY_MARK = " "
BORDER_SIDE = "|"
BORDER_TOP_BOTTOM = "-"
CELL_CORNER = "+"
PLAYER_1_MARK = "X"
PLAYER_2_MARK = "O"
GRID_SIZE = 3
REWRITE_ALLOWED = False


def print_grid():
    index = 0
    print BORDER_TOP_BOTTOM * (2 * GRID_SIZE + 1)
    while index < len(grid):
        row = grid[index:index + GRID_SIZE]
        print BORDER_SIDE + BORDER_SIDE.join(row) + BORDER_SIDE
        if index != len(grid) - GRID_SIZE:
            print (BORDER_TOP_BOTTOM + CELL_CORNER) * GRID_SIZE + BORDER_TOP_BOTTOM
        index += GRID_SIZE
    print BORDER_TOP_BOTTOM * (2 * GRID_SIZE + 1)


def grid_get(x, y):
    index = y * GRID_SIZE + x
    return grid[index]


def grid_set(x, y):
    index = y * GRID_SIZE + x
    if index < 0 or index >= len(grid):
        return False
    value = grid[index]
    if value is EMPTY_MARK or REWRITE_ALLOWED:
        grid[index] = player_with_turn
        return True
    return False


def collect_input():
    print "Player: [" + player_with_turn + "]"
    col = collect_integer("\tCol: ")
    row = collect_integer("\tRow: ")
    return col, row


def collect_integer(text):
    value = None
    while type(value) is not int:
        try:
            value = int(raw_input(text))
        except ValueError:
            print "Please enter an integer!"
            pass
    return value


def change_turn():
    global player_with_turn
    if player_with_turn == PLAYER_1_MARK:
        player_with_turn = PLAYER_2_MARK
    else:
        player_with_turn = PLAYER_1_MARK


def check_grid():
    if check_straight(True):
        return True
    if check_straight(False):
        return True
    if check_diagonal(True):
        return True
    if check_diagonal(False):
        return True
    return False


def check_straight(vertical):
    axis_1 = 0
    while axis_1 < GRID_SIZE:
        axis_2 = 0
        first_value = None
        full_row = True
        while axis_2 < GRID_SIZE:
            value = grid_get(axis_1 if vertical else axis_2, axis_2 if vertical else axis_1)
            if first_value is None:
                if value == PLAYER_1_MARK or value == PLAYER_2_MARK:
                    first_value = value
                else:
                    full_row = False
                    break
            if value != first_value:
                full_row = False
                break
            axis_2 += 1
        if full_row:
            return True
        axis_1 += 1
    return False


def check_diagonal(top):
    full_row = True
    check_x = 0
    check_y = 0 if top else GRID_SIZE - 1
    first_value = None
    while check_x < GRID_SIZE and check_y < GRID_SIZE:
        value = grid_get(check_x, check_y)
        if first_value is None:
            if value == PLAYER_1_MARK or value == PLAYER_2_MARK:
                first_value = value
            else:
                full_row = False
                break
        if value != first_value:
            full_row = False
            break
        check_x += 1
        check_y += 1 if top else -1
    return full_row


grid = [EMPTY_MARK] * GRID_SIZE ** 2
player_with_turn = PLAYER_1_MARK
print_grid()
while True:
    col, row = collect_input()
    result = grid_set(col, row)
    if not result:
        print "Invalid input!"
        continue
    print_grid()
    if check_grid():
        print "GAME OVER!"
        print "\tWinner: " + player_with_turn
        break
    if EMPTY_MARK not in grid:
        print "GAME OVER!"
        print "Draw"
        break
    change_turn()
