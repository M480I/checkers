from piece import Piece
from move import Transition, Move
from consts import BIG_INF, SMALL_INF


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
                                                

    def remove_piece(self, piece):
        piece.cell.piece = None
        self.pieces.remove(piece)

    
    def revive_piece(self, piece):
        piece.cell.piece = piece
        self.pieces.append(piece)
     
     
    def is_end_row(self, row):
        if self.is_down:
            return row == 0
        return row == 7
        
    # Todo
    # alter moves minimum and maximum length
    @property
    def next_moves(self):
        moves = []
        for piece in self.pieces:
            cell = piece.cell
            for next_cell in piece.next_cells:
                transition = Transition(cell, next_cell, self.game)
                moves.extend(transition.moves)

        moves.sort(key=lambda move: -move.score)
        
        if moves:
            if moves[0].score >= SMALL_INF:
                tmp_moves = []
                for move in moves:
                    if move.score < SMALL_INF:
                        break
                    tmp_moves.append(move)
                moves = tmp_moves

        if len(moves) < 14:
            moves = moves[:7]
        else:
            n = len(moves)
            moves = moves[:n // 2]

        return moves
    
    # Todo
    # better length at the endgame
    
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
                move.do()
                eval, next_move = self.opponent.best_move(
                                                depth=depth + 1,
                                                max_depth=max_depth, 
                                                alpha=alpha,
                                                beta=beta,
                                                )
                move.undo()
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
                move.do()
                eval, _ = self.opponent.best_move(
                                                depth=depth + 1,
                                                max_depth=max_depth,
                                                alpha=alpha,
                                                beta=beta,
                                                )
                move.undo()
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
        best_move.final_do()
    
    
    def __str__(self) -> str:
        return f"{'⚫ at down' if self.is_down else '⚪ at up'}"
    