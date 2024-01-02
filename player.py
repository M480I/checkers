from piece import Piece


class Player:
    
    
    def __init__(self, board, is_down) -> None:
        
        self.board = board
        self.pieces = []
        self.is_down = is_down
        
        for x in range(board.row_count):
            for y in range(board.column_count):
                cell = board.cells[x][y]
                if cell.color == "W":
                    continue
                if (x >= 3 and not self.is_down) \
                    or (x <= 2 and self.is_down):
                    self.add_piece(cell)
                    
    
    def add_piece(self, cell):
        piece = Piece(cell=cell, player=self)
        self.pieces.append(piece)