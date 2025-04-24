import piece
import numpy as np
from eval_fn import evaluation_state

def get_best_move(state, depth, is_max_state, difficulty="Medium"):
    values = state.values
    best_value = is_max_state and -9999 or 9999
    best_move = (-1, -1)
    pieces = np.count_nonzero(values != piece.EMPTY)  # Fixed: explicit count

    if pieces == 0:
        return first_move(state)
    if pieces == 1:
        return second_move(state)

    # Easy difficulty: make random moves with occasional blunders
    if difficulty == "Easy":
        legal_moves = state.legal_moves()
        if len(legal_moves) > 0:  # Fixed: explicit length check
            # 70% chance to make a completely random move
            if np.random.random() < 0.7:
                best_move = legal_moves[np.random.choice(len(legal_moves))]
                return best_move, 0
            
            # 30% chance to try to make a reasonable move, but with minimal evaluation
            top_moves = get_top_moves(state, 3, is_max_state, difficulty)
            if len(top_moves) > 0:  # Fixed: explicit length check
                # Pick a random move from the top moves but prefer worse ones
                if len(top_moves) > 1:
                    # Avoid the best move
                    move_index = np.random.randint(1, len(top_moves))
                    return top_moves[move_index], 0
                return top_moves[0], 0
            return legal_moves[np.random.choice(len(legal_moves))], 0

    top_moves = get_top_moves(state, 10, is_max_state, difficulty)

    for move_n_value in top_moves:
        move = move_n_value[0]
        value = minimax(state.next(move),
                        -10e5,
                        10e5,
                        depth - 1,
                        not is_max_state,
                        difficulty)

        if ((is_max_state and value > best_value)
                or (not is_max_state and value < best_value)):
            best_value = value
            best_move = move

    if best_move[0] == -1 and best_move[1] == -1:
        return top_moves[0]

    return best_move, best_value
def get_top_moves(state, n, is_max_state, difficulty="Medium"):
    color = state.color
    top_moves = []

    for move in state.legal_moves():
        evaluation = evaluation_state(state.next(move), color, difficulty)
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=is_max_state)[:n]


def minimax(state, alpha, beta, depth, is_max_state, difficulty="Medium"):
    if depth == 0 or state.is_terminal():
        return evaluation_state(state, -state.color, difficulty)

    if is_max_state:
        value = -9999
        for move in state.legal_moves():
            value = max(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, False, difficulty)
            )
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value
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
    x = state.size // 2
    return np.random.choice((x - 1, x, x + 1), 2), 1


def second_move(state):
    i, j = state.last_move
    size = state.size
    i2 = i <= size // 2 and 1 or -1
    j2 = j <= size // 2 and 1 or -1
    return (i + i2, j + j2), 2
