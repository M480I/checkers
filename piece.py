class Piece:
    
    
    def __init__(self, cell, player) -> None:
        self.cell = cell
        self.player = player
        
        self.is_king = False
        cell.piece = self
                
    
    @property
    def emoji(self):
        if not self.is_king:
            return"⚫" if self.player.is_down else "⚪"
        return "⬛" if self.player.is_down else "⬜"
    

    @property
    def next_cells(self):
        cells = []
        
        if self.is_king or not self.player.is_down:
            cells.extend(self.cell.adjacent_cells["down"])
        if self.is_king or self.player.is_down:
            cells.extend(self.cell.adjacent_cells["up"])
        
        return cells
    
    # move piece to new_cell
    def move(self, new_cell):
        
        if new_cell.piece is self:
            return
        
        if new_cell.piece is not None:
            raise RuntimeError
        
        self.cell.piece = None
        new_cell.piece = self
        self.cell = new_cell
    
    
    def __str__(self) -> str:
        return f"{self.emoji} at {self.cell}"
    
    
    def __repr__(self) -> str:
        return self.__str__()
