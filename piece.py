class Piece:
    
    
    def __init__(self, cell, player) -> None:
        self.cell = cell
        self.player = player
        self.is_king = False
        
        cell.piece = self
        
        self.emoji = "⚫" if player.is_down else "⚪"      
    
    # toDo
    @property
    def next_cells(self):
        cells = []
        
        if self.is_king:
            cells.extend(self.cell.adjacent_cells["backward"])
        cells.extend(self.cell.adjacent_cells["forward"])
        
        return cells
    
    # move piece to new_cell
    def move(self, new_cell):
        if new_cell.piece is not None:
            return
        self.cell.piece = None
        new_cell.piece = self
        self.cell = new_cell
    
    
    def __str__(self) -> str:
        return f"{self.emoji} at {self.cell}"
    
    
    def __repr__(self) -> str:
        return self.__str__()
