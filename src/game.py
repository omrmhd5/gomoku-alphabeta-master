import piece
import numpy as np
from board import BoardState
from ai import get_best_move


class GameRunner:
    def __init__(self, size=19, difficulty="Medium"):
        self.size = size
        self.difficulty = difficulty
        self.finished = False
        
        # Set search depth based on difficulty
        if difficulty == "Easy":
            self.depth = 1  # Very shallow search depth for Easy
        elif difficulty == "Medium":
            self.depth = 2
        else:  # Hard
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
            return False, (0, 0)
        
        # For Easy difficulty, occasionally make a suboptimal move
        if self.difficulty == "Easy" and np.random.random() < 0.15:
            # Find a suboptimal move by avoiding center and nearby opponent pieces
            legal_moves = self.state.legal_moves()
            if len(legal_moves) > 0:  # Fixed: explicit length check
                # Try to play in corners or edges rather than center
                edge_moves = []
                for move in legal_moves:
                    i, j = move
                    if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                        edge_moves.append(move)
                
                if len(edge_moves) > 0 and np.random.random() < 0.6:  # Fixed: explicit length check
                    move = edge_moves[np.random.choice(len(edge_moves))]
                else:
                    move = legal_moves[np.random.choice(len(legal_moves))]
                
                self.state = self.state.next(move)
                self.finished = self.state.is_terminal()
                return True, move
        
        # Regular AI play
        move, value = get_best_move(self.state, self.depth, self.is_max_state, self.difficulty)
        self.state = self.state.next(move)
        self.finished = self.state.is_terminal()
        return True, move

    def get_status(self):
        board = self.state.values
        return {
            'board': board.tolist(),
            'next': -self.state.color,
            'finished': self.finished,
            'winner': self.state.winner,
            # 'debug_board': self.state.__str__()
        }
