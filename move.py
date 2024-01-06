moves = {
    "up": {
        "left": (-1, -1),
        "right": (-1, 1)
    },
    "down": {
        "left": (1, -1),
        "right": (1, 1)
    }
}


class Move:
    
    
    def __init__(self, from_cell, to_cell, game) -> None:
        self.from_cell = from_cell
        self.to_cell = to_cell

        self.board = game.board
        self.player = self.from_cell.piece.player
        self.opponent = \
            game.player_up if self.player.is_down else game.player_down
        self.diff = \
            tuple([to_cell.coordinates[i] - from_cell.coordinates[i] for i in range(2)])
        
        self.is_valid = None
        self.is_kill = None
        self.kill_king = None
        self.get_king = None
        self.destination = None
        
        self.check_move()
    
    # fills is_valid, is_kill, get_king, kill_king, destination of the move
    def check_move(self):
        # no pieces in the to_cell, valid move, not a kill move
        if self.to_cell.piece is None:
            self.is_valid = True
            self.is_kill = False
            self.kill_king = False
            self.get_king = self.to_cell.row == (0 if self.player.is_down else 7)
            self.destination = self.to_cell
            return
        
        # friendly pieces in the to_cell, not a valid move
        if self.to_cell.piece.player is self.player:
            self.is_valid = False
            return
        
        # enemy pieces in the to_cell, so check if the next cell is empty
        x, y = \
            tuple([self.to_cell.coordinates[i] + self.diff[i] for i in range(2)])
        # next cell is not valid in the board, not a valid move
        if not self.board.is_valid_cell(x, y):
            self.is_valid = False
            return
        
        next_cell = self.board.cells[x][y]
        # next cell is not empty, not a valid move
        if next_cell.piece is not None:
            self.is_valid = False
            return
        
        # next cell is a valid, empty cell, so
        # kill the enemy piece and move to next cell
        self.is_valid = True
        self.is_kill = True
        self.kill_king = self.to_cell.piece.is_king
        self.get_king = self.to_cell.row == (0 if self.player.is_down else 7)
        self.destination = next_cell
        
        
    def do_move(self):
        pass
    
    
    def undo_move(self):
        pass
        
        
    def __str__(self) -> str:
        res = ""
        res += f"{self.is_valid=}\n"
        res += f"{self.is_kill=}\n"
        res += f"{self.kill_king=}\n"
        res += f"{self.get_king=}\n"
        res += f"{self.destination=}\n"
        return res
    
    
    def __repr__(self) -> str:
        return self.__str__()