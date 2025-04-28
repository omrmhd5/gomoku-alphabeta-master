import piece
import numpy as np
from board import BoardState
from ai import get_best_move

#controls the full logic of running a game (player moves, AI moves, game restarting)
class GameRunner:
    def __init__(self, size=19, difficulty="Medium"):
        self.size = size
        self.difficulty = difficulty
        self.finished = False
        
        #search depth based on difficulty
        if difficulty == "Easy":
            self.depth = 1 
        elif difficulty == "Medium":
            self.depth = 2
        else:  # Hard
            self.depth = 3
            
        self.restart() #Start a new game immediately when the object is created and called.


    #Restarts the game with the player playing
    def restart(self, player_index=-1):
        self.is_max_state = True if player_index == -1 else False #-1 when its AI, tries to maximize
        self.state = BoardState(self.size) #new board
        self.ai_color = -player_index

    def play(self, i, j):
        position = (i, j) # tuple to choose row and column
        if self.state.color != self.ai_color: #if its players turn dont make the ai play and vice versa
            return False
        if not self.state.is_valid_position(position): # check if move empty
            return False
        self.state = self.state.next(position) #apply move
        self.finished = self.state.is_terminal() ##check if game is over
        return True
    
    def aiplay(self): #ai turn
        if self.state.color == self.ai_color:
            return 0.0
        
        # Get AI's move
        try:
            move, value, move_time = get_best_move(self.state, self.depth, self.is_max_state, self.difficulty) #Ask the AI for the best move, expected score, and time taken.
            
            # Convert move to a proper tuple if it's not already
            # This handles cases where move might be a numpy array
            if not isinstance(move, tuple):
                move = tuple(map(int, move))
            
            # Ensure move is valid before applying it check if 2d position
            if not isinstance(move, tuple) or len(move) != 2 or not self.state.is_valid_position(move):
                # If invalid, pick a random valid move as fallback
                legal_moves = self.state.legal_moves()
                if len(legal_moves) > 0:
                    move = legal_moves[np.random.choice(len(legal_moves))]
                else:
                    # No valid moves available
                    return 0.0
            
            # Apply the move and return how long ai took
            self.state = self.state.next(move)
            self.finished = self.state.is_terminal()
            return move_time
        except Exception as e:
            # Fallback in case of any error
            print(f"Error in AI move: {e}")
            
            #Pick a random valid move.
            legal_moves = self.state.legal_moves()
            if len(legal_moves) > 0:
                move = legal_moves[np.random.choice(len(legal_moves))]
                self.state = self.state.next(move)
                self.finished = self.state.is_terminal()
                return 0.0
            return 0.0
    
    def get_status(self):
        board = self.state.values #get curretn board
        return {
            'board': board.tolist(), #Current board (converted to list).
            'next': -self.state.color, #Whose turn is next.
            'finished': self.finished, # game is finished
            'winner': self.state.winner, #who won
            # 'debug_board': self.state.__str__()
        }
