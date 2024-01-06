from board import Board
from player import Player


class Game:
    
    
    def __init__(self):
        
        self.board = Board()
        self.player_down = Player(self.board, True)
        self.player_up = Player(self.board, False)        
        self.winner = None
      