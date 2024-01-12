from consts import moves


class Cell:
    

    def __init__(self, row, column, board) -> None:
        self.row = row
        self.column = column
        self.board = board
        
        self.piece = None
        self.color = "B" if (row % 2) != (column % 2) else "W"
        self.coordinates = self.row, self.column
        
        self.adjacent_cells = {
            "up": [],
            "down": []
        }


    def next_diagonally(self, other):
        if (other not in self.adjacent_cells["down"] 
            and other not in self.adjacent_cells["up"]):
            return None
        
        new_x, new_y = 2*other.row - self.row, 2*other.column - self.column
        
        if self.board.is_valid_cell(new_x, new_y):
            return self.board.cells[new_x][new_y]
        
        return None

    
    def __str__(self) -> str:
        return f"({self.row}, {self.column})"
    
    
    def __repr__(self) -> str:
        return self.__str__()
    

class Board:
        
    
    def __init__(self) -> None:
        self.row_count = self.column_count = 8
        
        self.cells = []
        
        self.make_cells()
        self.fill_adjacents()
        
    # make cells for board>
    def make_cells(self):
        for x in range(self.row_count):
            row = []
            for y in range(self.column_count):
                row.append(Cell(x, y, self))
            self.cells.append(row)    
                
    # fill successors of each cell
    def fill_adjacents(self):
        for row in self.cells:
            for cell in row:
                
                x, y = cell.coordinates 
                               
                for diff_mode in ["down", "up"]:
                    for diff_x, diff_y in moves[diff_mode].values():
                        
                        adj_x, adj_y = x + diff_x, y + diff_y
                        
                        if self.is_valid_cell(adj_x, adj_y):
                            adj_cell = self.cells[adj_x][adj_y]
                                
                            cell.adjacent_cells[diff_mode].append(adj_cell)
    
    
    def is_valid_cell(self, x, y):
        return x >= 0 and y >= 0 and x < self.row_count and y < self.column_count
    
    
    def __str__(self) -> str:
        
        res = ""
        sep1 = " +----+----+----+----+----+----+----+----+\n "
        sep2 = "| "
        sep3 = " "
        
        for i in range(self.row_count):
            res += sep1
            for j in range(self.column_count):
                piece = "  "
                if self.cells[i][j].piece is not None:
                    piece = self.cells[i][j].piece.emoji
                res += sep2 + piece + sep3
            res += "|\n"
        res += sep1
        
        return res
    
    
    def __repr__(self) -> str:
        return self.__str__()
