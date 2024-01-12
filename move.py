from consts import SMALL_INF

   
class Transition():
    
    
    def __init__(self, from_cell, to_cell, game) -> None:
                
        self.from_cell = from_cell
        self.to_cell = to_cell
        
        self.game = game
        self.board = game.board

        self.piece = self.from_cell.piece
        self.player = self.piece.player
        
        self.moves = []
        
        self.find_moves()

    
    def find_moves(self):
        # no pieces in the to_cell, only one move
        if self.to_cell.piece is None:
            
            get_king = \
                (not self.piece.is_king 
                and self.player.is_end_row(self.to_cell.row))
            
            move = Move(initial_cell=self.from_cell,
                        piece=self.piece,
                        rest_cells=[],
                        dest_cell=self.to_cell,
                        get_king=get_king,
                        killed_pieces=[],
                        game=self.game,
                        )
            self.moves.append(move)
            return
        
        path = []
        killed_pieces = []
        
        def continue_path(cell, to_cell=None):
            
            next_cells = \
                [to_cell] if to_cell is not None else self.piece.next_cells
                
            can_kill = False
            get_king = not self.piece.is_king and self.player.is_end_row(cell.row)
            
            for next_cell in next_cells:
                
                rest_cell = cell.next_diagonally(next_cell)
                
                
                if to_cell is None:
                    if get_king:
                        break
                    
                    if next_cell.piece is None:
                        continue
                    
                    if (next_cell.piece.player is self.player 
                            or next_cell.piece in killed_pieces):
                        continue
                    
                    if rest_cell is None: 
                        continue
                    
                    if rest_cell.piece is not None:
                        continue
                    
                else:
                    if next_cell.piece.player is self.player:
                        return

                    if rest_cell is None:
                        return

                    if rest_cell.piece is not None:
                        continue
                    
                    
                can_kill = True                   
                    
                killed_pieces.append(next_cell.piece)
                path.append(rest_cell)
                self.piece.move(rest_cell)

                continue_path(rest_cell)

                self.piece.move(cell)
                path.pop()
                killed_pieces.pop()
                
            if to_cell is None and (not next_cells 
                    or get_king 
                    or can_kill == False):
                
                move = Move(initial_cell=self.from_cell,
                            piece=self.piece,
                            rest_cells=path[:-1],
                            dest_cell=cell,
                            get_king=get_king,
                            killed_pieces=killed_pieces[:],
                            game=self.game
                            )
                self.moves.append(move)
        
        continue_path(self.from_cell, self.to_cell)
        
        
class Move():
    
    
    def __init__(
            self, initial_cell, piece, rest_cells, dest_cell, get_king, 
            killed_pieces, game) -> None:
        
        self.initial_cell = initial_cell
        self.piece = piece
        self.player = piece.player
        self.game = game
        self.opponent = \
            game.up_player if self.player.is_down else game.down_player        
        self.rest_cells = rest_cells
        self.dest_cell = dest_cell
        self.get_king = get_king
        self.killed_pieces = killed_pieces
        self.visible_board = game.visible_board
        
        self.score = self.calculate_score()
        
        
    def calculate_score(self):
        res = 0
        # has_kill +SMALL_INF (mandatory kill)
        # kill +3, kill_king +5
        # get king +5
        # good dest +1
        
        if self.killed_pieces:
            res += SMALL_INF
        
        for killed_piece in self.killed_pieces:
            if killed_piece.is_king:
                res += 5
            else:
                res += 3
                
        res += 5 * (self.get_king)
        
        x, y = self.dest_cell.coordinates
        res += (x in [0, 7] and y in [0, 7])  
        
        return res
    

    def final_do(self):
        
        if not self.rest_cells:
            self.piece.move(self.dest_cell)
            if self.get_king:
                self.piece.is_king = True
            if self.visible_board:
                self.game.show_board()
            
        else:
            path = self.rest_cells + [self.dest_cell]
            for killed_piece, cell in zip(self.killed_pieces, path):
                self.opponent.remove_piece(piece=killed_piece)
                self.piece.move(cell)
                if self.get_king and self.player.is_end_row(cell.row):
                    self.piece.is_king = True
                if self.visible_board:
                    self.game.show_board()
                    
                    
    def do(self):
        
        if not self.rest_cells:
            self.piece.move(self.dest_cell)
            if self.get_king:
                self.piece.is_king = True
            
        else:
            path = self.rest_cells + [self.dest_cell]
            for killed_piece, cell in zip(self.killed_pieces, path):
                self.opponent.remove_piece(piece=killed_piece)
                self.piece.move(cell)
                if self.get_king and self.player.is_end_row(cell.row):
                    self.piece.is_king = True
                    
                    
    def undo(self):
        
        self.piece.move(self.initial_cell)
        if self.get_king:
            self.piece.is_king = False
        for killed_piece in self.killed_pieces:
            self.opponent.revive_piece(killed_piece)
                
                
    def __str__(self) -> str:
        res = '\n{' + f"{self.piece=}\n"
        res += f"{self.rest_cells=}\n"
        res += f"{self.dest_cell=}\n"
        res += f"{self.get_king=}\n"
        res += f"{self.killed_pieces=}\n"
        res += f"{self.score=}" + '}\n'
        return res
    
    
    def __repr__(self) -> str:
        return self.__str__()