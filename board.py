class Cell:
    

    def __init__(self, row, column, piece = None) -> None:
        self.row = row
        self.column = column
        self.piece = piece
        self.color = "B" if (row % 2) == (column % 2) else "W"
        self.coordinates = self.row, self.column
        self.successor_cells = {
            "forward": [],
            "backward": []
        }

    
    def __str__(self) -> str:
        return f"({self.row}, {self.column})"


class Board:
    moves = {
        "forward": {
            "left": (-1, -1),
            "right": (-1, 1)
        },
        "backward": {
            "left": (1, -1),
            "right": (1, 1)
        }
    }
    
    
    def __init__(self) -> None:
        self.row_count = self.column_count = 8
        
        # make cells for board
        self.cells = []
        
        for x in range(self.row_count):
            row = []
            for y in range(self.column_count):
                row.append(Cell(x, y))
            self.cells.append(row)
        
        # fill successors of each cell
        for row in self.cells:
            for cell in row:
                x, y = cell.coordinates                
                for mode in ["forward", "backward"]:
                    for diff_x, diff_y in Board.moves[mode].values():
                        adj_x, adj_y = x + diff_x, y + diff_y
                        if self.is_valid_cell(adj_x, adj_y):
                            new_cell = self.cells[adj_x][adj_y]
                            cell.successor_cells[mode].append(new_cell)
                
            
            
    def is_valid_cell(self, x, y):
        return x >= 0 and y >= 0 and x < self.row_count and y < self.column_count

    
    def check_move(self, from_cell, to_cell, move: tuple):
        status = {
            "is_valid": None,
            "is_kill": None,
            "destination": None,
        }
        
        # no pieces in the destination cell, valid move, not a kill move
        if to_cell.piece is None:
            status["is_valid"] = True
            status["is_kill"] = False
            status["destination"] = to_cell
            return status
        
        # friendly pieces in the destination cell, not a valid move
        if to_cell.piece.player is from_cell.piece.player:
            status["is_valid"] = False
            return status
        
        # enemy pieces in the destination, so check if the next cell is empty
        diff_x, diff_y = Board.moves[move[0]][move[1]]
        
