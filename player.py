class Player:

    def __init__(self, mark, input_collector):
        self.mark = mark
        self.grid = None
        self.input_collector = input_collector

    def move(self):
        if self.grid is None:
            return
        col, row = self.input_collector()
        result = self.grid.set(col, row, self.mark)
        if not result:
            self.move()
