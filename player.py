class Player:

    def __init__(self, mark, grid):
        self.mark = mark
        self.grid = grid

    def move(self):
        col, row = self._collect_input()
        result = self.grid.set(col, row, self.mark)
        if not result:
            print("Already occupied or out of bounds!")
            self.move()

    def _collect_input(self):
        print("Player: [" + self.mark + "]\n")
        col = collect_integer("\tCol: ")
        row = collect_integer("\tRow: ")
        return col, row


def collect_integer(text):
    value = None
    while type(value) is not int:
        try:
            value = int(input(text))
        except ValueError:
            print("Please enter an integer!")
            pass
    return value
