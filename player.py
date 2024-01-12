from piece import Piece
from move import Move
from consts import INF, BIG_INF


class Player:
    
    
    def __init__(self, game, is_down, max_depth=10) -> None:
        
        self.game = game
        self.board = game.board
        self.max_depth = max_depth
        self.is_down = is_down
        
        self.opponent = None
        
        self.pieces = []
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

                self.pieces.append(Piece(cell=cell, player=self))        
                                                
    # call with cell or/and piece as an argument
    def remove_piece(self, piece=None, cell=None):
        if piece is not None:
            piece.cell.piece = None
            self.pieces.remove(piece)
        elif cell is not None:
            self.pieces.remove(cell.piece)
            cell.piece = None

    
    def add_removed_piece(self, piece, cell):
        cell.piece = piece
        self.pieces.append(piece)
        
    
    @property
    def next_moves(self):
        moves = []
        for piece in self.pieces:
            cell = piece.cell
            for next_cell in piece.next_cells:
                move = Move(cell, next_cell, self.game)
                if move.is_valid:
                    moves.append(move)
        moves.sort(key=lambda move: -move.score)

        if len(moves) < 16:
            moves = moves[:8]
        else:
            n = len(moves)
            moves = moves[:n // 2]

        return moves
    
    # minimax algorithm
    def best_move(self, depth=0, max_depth=None, alpha=-BIG_INF, beta=BIG_INF) -> tuple[int, Move]:
        
        max_depth = self.max_depth if max_depth is None else max_depth
        
        if self.game.is_end() \
            or depth >= max_depth \
            or (depth >= 5 and self.game.total_moves < self.game.endgame):
                return self.game.evaluate_board(), None
        
        # maximize
        if self.is_down:
            max_eval = -BIG_INF
            best_move = None
            for move in self.next_moves:
                move.do_move()
                eval, next_move = self.opponent.best_move(
                                                depth=depth + 1,
                                                max_depth=max_depth, 
                                                alpha=alpha,
                                                beta=beta,
                                                )
                move.undo_move()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
                
         # minimize   
        else:
            min_eval = BIG_INF
            best_move = None
            for move in self.next_moves:
                move.do_move()
                eval, _ = self.opponent.best_move(
                                                depth=depth + 1,
                                                max_depth=max_depth,
                                                alpha=alpha,
                                                beta=beta,
                                                )
                move.undo_move()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    
    def move(self):
        self.game.total_moves += 1
        _, best_move = self.best_move()
        best_move.do_move()
    
    def __str__(self) -> str:
        return f"{'⚫ at down' if self.is_down else '⚪ at up'}"
    