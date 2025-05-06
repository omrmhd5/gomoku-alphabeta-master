import piece
import numpy as np
from board import BoardState
from ai import get_best_move

class GameRunner:
    def __init__(self, size=19, difficulty="Medium"):
        self.size = size
        self.difficulty = difficulty
        self.finished = False
        
        if difficulty == "Easy":
            self.depth = 1 
        elif difficulty == "Medium":
            self.depth = 2
        else:  
            self.depth = 3
            
        self.restart()


    def restart(self, player_index=-1):
        self.is_max_state = True if player_index == -1 else False 
        self.state = BoardState(self.size) 
        self.ai_color = -player_index

    def play(self, i, j):
        position = (i, j) 
        if self.state.color != self.ai_color: 
            return False
        if not self.state.is_valid_position(position): 
            return False
        self.state = self.state.next(position)
        self.finished = self.state.is_terminal() 
        return True
    
    def aiplay(self): 
        if self.state.color == self.ai_color:
            return 0.0
        
        try:
            move, value, move_time = get_best_move(self.state, self.depth, self.is_max_state, self.difficulty) 
            
            if not isinstance(move, tuple):
                move = tuple(map(int, move))
            
            if not isinstance(move, tuple) or len(move) != 2 or not self.state.is_valid_position(move):
                legal_moves = self.state.legal_moves()
                if len(legal_moves) > 0:
                    move = legal_moves[np.random.choice(len(legal_moves))]
                else:
                    return 0.0
            
            self.state = self.state.next(move)
            self.finished = self.state.is_terminal()
            return move_time
        except Exception as e:
            print(f"Error in AI move: {e}")
            
            legal_moves = self.state.legal_moves()
            if len(legal_moves) > 0:
                move = legal_moves[np.random.choice(len(legal_moves))]
                self.state = self.state.next(move)
                self.finished = self.state.is_terminal()
                return 0.0
            return 0.0
    
    def get_status(self):
        board = self.state.values
        return {
            'board': board.tolist(), 
            'next': -self.state.color, 
            'finished': self.finished, 
            'winner': self.state.winner, 
        }
