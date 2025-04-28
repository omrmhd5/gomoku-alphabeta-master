import piece
import numpy as np
from eval_fn import evaluation_state
import time

def get_best_move(state, depth, is_max_state, difficulty="Medium"):
    start_time = time.time()
    values = state.values
    best_value = is_max_state and -9999 or 9999 # initialize best value with -9999 for max player and 9999 for min player
    best_move = (-1, -1) # initialize best move with an invalid move
    pieces = np.count_nonzero(values != piece.EMPTY) # count number of non-empty pieces on the board

    # check if no pieces on the board, AI picks a random move
    if pieces == 0:
        move, value, _ = first_move(state) 
        return move, value, time.time() - start_time 
    # check if one piece on the board, AI picks a move to respond to the opponent's move
    if pieces == 1:
        move, value, _ = second_move(state) 
        return move, value, time.time() - start_time
                
    legal_moves = state.legal_moves() # get all legal moves
    # check if no legal moves available
    if len(legal_moves) == 0:
        return (-1, -1), 0, 0            
    # check if easy difficulty: no deep thinking, and AI picks random move
    if difficulty == "Easy":
        move_index = np.random.choice(len(legal_moves))
        selected_move = legal_moves[move_index]
        # check if move is not a tuple, convert to tuple
        if not isinstance(selected_move, tuple):
            selected_move = tuple(map(int, selected_move))
        return selected_move, 0, time.time() - start_time

    # medium and hard difficulties, AI uses normal logic, get top 10 moves
    top_moves = get_top_moves(state, min(10, len(legal_moves)), is_max_state, difficulty)    

    # iterate through the top moves to find the best move using Minimax
    for move_n_value in top_moves:
        move = move_n_value[0]
        value = minimax(state.next(move),
                      -10e5,
                      10e5,
                      depth - 1,
                      not is_max_state,
                      difficulty)

        # update best move and value if found a better one     
        if ((is_max_state and value > best_value)
                or (not is_max_state and value < best_value)):
            best_value = value
            best_move = move
    # if not found, set to the first top move
    if best_move[0] == -1 and best_move[1] == -1 and len(top_moves) > 0:
        best_move = top_moves[0][0]
    # ensure the best move format is a tuple
    if not isinstance(best_move, tuple):
        best_move = tuple(map(int, best_move))
    
    return best_move, best_value, time.time() - start_time

def get_top_moves(state, n, is_max_state, difficulty="Medium"):
    color = state.color # get the current player's color
    top_moves = []    # initialize an empty list to store moves and their evaluations

    for move in state.legal_moves():
        # simulate the move and evaluate the resulting state
        evaluation = evaluation_state(state.next(move), color, difficulty)
        # store the move along with its evaluation
        top_moves.append((move, evaluation))

    # sort the moves based on their evaluation score
    # if maximizing, sort from highest to lowest; if minimizing, from lowest to highest
    # return only the top 'n' moves
    return sorted(top_moves, key=lambda x: x[1], reverse=is_max_state)[:n]


def minimax(state, alpha, beta, depth, is_max_state, difficulty="Medium"):
    # base case: if maximum depth reached or game is over
    if depth == 0 or state.is_terminal():
        # return the evaluated value of the current board state
        return evaluation_state(state, -state.color, difficulty)

    # if maximizing player's turn
    if is_max_state:
        value = -9999
        for move in state.legal_moves():
            # recursively call minimax for the next move
            value = max(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, False, difficulty)
            )
            alpha = max(value, alpha)
            # cut off remaining branches by alpha-beta pruning
            if alpha >= beta:
                break
        return value
    # if minimizing player's turn, do the same but start with very high value
    else:
        value = 9999
        for move in state.legal_moves():
            value = min(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, True, difficulty)
            )
            beta = min(value, beta)
            if alpha >= beta:
                break
        return value


def first_move(state):
    x = state.size // 2   # find the center index of the board
    # choose a random move near the center
    move = (np.random.choice((x - 1, x, x + 1)), np.random.choice((x - 1, x, x + 1)))
    # return the chosen move, a dummy value (1), and a dummy time (0)
    return move, 1, 0

def second_move(state):
    # get last move's coordinates
    i, j = state.last_move
    size = state.size # get the board size
    # decide the direction to move:
    # if the last move was on the top half, move down (i2 = 1), else move up (i2 = -1)
    i2 = i <= size // 2 and 1 or -1
    # if the last move was on the left half, move right (j2 = 1), else move left (j2 = -1)
    j2 = j <= size // 2 and 1 or -1
    # calculate the new move position based on the chosen directions
    move = (int(i + i2), int(j + j2))
    # return the new move, a dummy value (2), and a dummy time (0)
    return move, 2, 0