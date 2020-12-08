class Player:

    def __init__(self, mark, input_collector=None):
        self.mark = mark
        self.grid = None
        self.input_collector = input_collector

    def move(self):
        if self.grid is None or self.input_collector is None:
            return
        col, row = self.input_collector()
        self.grid.set(col, row, self.mark)
