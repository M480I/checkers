from piece import Piece


class Player:
    
    
    def __init__(self, board, is_down) -> None:
        
        self.board = board
        self.pieces = []
        self.is_down = is_down
        
        self.add_pieces()
        
        
    def add_pieces(self):
        if self.is_down:
            l = 5
            r = 8
        else:
            l = 0
            r = 3
            
        for x in range(l, r):
            for y in range(self.board.column_count):
                cell = self.board.cells[x][y]
                
                if cell.color == "W":
                    continue

                self.add_piece(cell)
                                            
        
    def add_piece(self, cell):
        piece = Piece(cell=cell, player=self)
        self.pieces.append(piece)
        
        
    def add_removed_piece(self, piece, cell):
        cell.piece = piece
        self.pieces.append(piece)
        
    
    # call with cell or/and piece as an argument
    def remove_piece(self, piece=None, cell=None):
        if piece is not None:
            piece.cell.piece = None
            self.pieces.remove(piece)
        if cell is not None:
            self.pieces.remove(cell.piece)
            cell.piece = None
