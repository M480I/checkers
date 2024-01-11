from consts import INF


class Move:
    
    
    def __init__(self, from_cell, to_cell, game) -> None:
        self.from_cell = from_cell
        self.to_cell = to_cell
        self.game = game

        self.board = game.board
        self.piece = self.from_cell.piece
        self.player = self.piece.player
        self.opponent = \
            game.up_player if self.player.is_down else game.down_player
        self.diff = \
            [to_cell.coordinates[i] - from_cell.coordinates[i] for i in range(2)]
        
        self.is_valid = None
        self.is_kill = None
        self.killed_piece = None
        self.kill_king = None
        self.get_king = None
        self.destination = None
        
        self.check_move()
        self.score = self.calculate_score()
    
    # fills is_valid, is_kill, get_king, kill_king, destination of the move
    def check_move(self):
        # no pieces in the to_cell, valid move, not a kill move
        if self.to_cell.piece is None:
            self.is_valid = True
            self.is_kill = False
            self.kill_king = False
            self.destination = self.to_cell
            if not self.piece.is_king:
                self.get_king = \
                    self.destination.row == (0 if self.player.is_down else 7)
            else:
                self.get_king = False
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
        self.killed_piece = self.to_cell.piece
        self.kill_king = self.to_cell.piece.is_king
        self.destination = next_cell
        if not self.piece.is_king:
            self.get_king = \
                self.destination.row == (0 if self.player.is_down else 7)
        else:
            self.get_king = False
        
        
    def calculate_score(self):
        
        if not self.is_valid:
            return -INF
        
        res = 0
        # kill +2, kill_king +4
        # get_king +3
        # good dest +1
        res += 2 * (self.is_kill)
        res += 2 * (self.kill_king)
        res += 3 * (self.get_king)
        x, y = self.destination.coordinates
        res += (x in [0, 7] and y in [0, 7])
        return res
                
        
    def do_move(self):
        if not self.is_valid:
            return
        
        self.piece.move(self.destination)
        if self.get_king:
            self.piece.is_king = True
        if self.is_kill:
            self.opponent.remove_piece(piece=self.killed_piece)
    
    
    def undo_move(self):
        if not self.is_valid:
            return
        
        self.piece.move(self.from_cell)
        if self.get_king:
            self.piece.is_king = False
        if self.is_kill:
            self.opponent.add_removed_piece(piece=self.killed_piece,
                                            cell=self.to_cell)
        
        
    def __str__(self) -> str:
        res = f"{self.from_cell}to{self.to_cell}\n"
        res += f"{self.is_valid=}\n"
        res += f"{self.is_kill=}\n"
        res += f"{self.kill_king=}\n"
        res += f"{self.killed_piece=}\n"
        res += f"{self.get_king=}\n"
        res += f"{self.destination=}\n"
        return res
    
    
    def __repr__(self) -> str:
        return self.__str__()