from board import Cell


class Piece:
    
    
    def __init__(self, cell: Cell, player) -> None:
        self.cell = cell
        self.is_king = False
            
    
    # toDo
    @property
    def successor_cells(self) -> list[Cell]:
        
        if self.is_king:
            pass
        pass
    