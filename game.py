from board import Board
from player import Player
import random
import os
from time import sleep
from consts import INF


class Game:
    
    
    def __init__(
            self, random_first=True,
            visible_board=True, wait_for=2, clean_terminal=True,
            up_depth=10, down_depth=10,
            endgame=8):
        
        self.random_first = random_first
        self.visible_board = visible_board
        self.wait_for=wait_for
        self.clean_terminal=clean_terminal
        self.endgame = endgame
        self.board = Board()
        self.down_player = Player(self, True, max_depth=down_depth)
        self.up_player = Player(self, False, max_depth=up_depth)
        self.down_player.opponent = self.up_player
        self.up_player.opponent = self.down_player  
        self.total_moves = 0
        self.winner = None
    
    
    def start_game(self):
        
        self.players = [
            self.down_player,
            self.up_player, 
        ]
                    
        if self.random_first:
            random.shuffle(self.players)
            
            
        first_player, second_player = self.players
        
        self.show_title()
        
        while not self.is_end():
            
            if self.visible_board:
                self.show_board()
                
            first_player.move()
            
            if self.visible_board:
                self.show_board()
                
            if self.is_end():
                break
            
            second_player.move()
            
            if self.visible_board:
                self.show_board()
        
        self.end()
        self.show_result()
        
    
    def show_title(self):
        self.clean()
        
        title = """
   _____ _               _                 
  / ____| |             | |                
 | |    | |__   ___  ___| | _____ _ __ ___ 
 | |    | '_ \ / _ \/ __| |/ / _ \ '__/ __|
 | |____| | | |  __/ (__|   <  __/ |  \__ \\
  \_____|_| |_|\___|\___|_|\_\___|_|  |___/
                        
                        
                                           
        """
        
        print(title)
        sleep(2)
        print(f"Player {self.players[0]} starts...\n\n")
        sleep(2)
        
    
    def show_board(self):
        self.clean()
        print(self.board)
        sleep(self.wait_for)
        
        
    def show_result(self):
        res = f"Total moves: {self.total_moves}\n"
        res += f"Winner: {self.winner}\n"
        print(res)
        
        
    def clean(self):
        if self.clean_terminal:
            os.system("cls" if os.name == "nt" else "clear")
    
    
    def evaluate_board(self):
        res = 0
        
        # res is how good the board is for down_player
        # +5 for each piece +10 for kings
        # +2 for each piece that can be kings in one move 
        # (are in the row 6 for up_player and row 1 for down_player)
        # +1 for each piece in rows 2 to 5 and columns 2 to 5
        
        winner = self.pick_winner()
        if winner is self.down_player:
            return INF
        if winner is self.up_player:
            return -INF
        
        for piece in self.down_player.pieces:
            x, y = piece.cell.coordinates
            res += 5
            res += 5 * (piece.is_king)
            res += 2 * (x == 1)
            res += (x in range(2, 6)) and (y in range(2, 6))
        
        for piece in self.up_player.pieces:
            x, y = piece.cell.coordinates
            res -= 5
            res -= 5 * (piece.is_king)
            res -= 2 * (x == 6)
            res -= (x in range(2, 6)) and (y in range(2, 6))
            
                    
        return res
        
    
    def end(self):   
        self.winner = self.pick_winner()


    def is_end(self):
        
        if not self.up_player.pieces or not self.up_player.next_moves: 
            return True
        if not self.down_player.pieces or not self.down_player.next_moves:
            return True
        return False
    
    
    def pick_winner(self):
        winner = None
        if not self.up_player.pieces or not self.up_player.next_moves: 
            winner = self.down_player
        elif not self.down_player.pieces or not self.down_player.next_moves:
            winner = self.up_player    
        return winner