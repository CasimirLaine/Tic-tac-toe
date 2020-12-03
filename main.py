import config
from grid import Grid
from player import Player
from ai import Ai


class Game:
    def __init__(self):
        self.grid = Grid()
        self.turns = 0
        self.player = Player(config.MARK_PLAYER_1, self.grid)
        self.ai = Ai(config.MARK_PLAYER_2, self.grid)
        self.player_with_turn = self.player

    def play(self):
        print "NEW GAME"
        self.grid.print_grid()
        while True:
            self.player_with_turn.move()
            self.grid.print_grid()
            if self.turns + 1 >= config.GRID_SIZE * 2 - 1 and self.grid.has_full_row():
                print "GAME OVER!"
                print "\tWinner: " + self.player_with_turn.mark
                break
            if self.grid.is_full():
                print "GAME OVER!"
                print "Draw"
                break
            self.change_turn()

    def change_turn(self):
        self.turns += 1
        if self.player_with_turn == self.player:
            self.player_with_turn = self.ai
        else:
            self.player_with_turn = self.player


game = Game()
game.play()
