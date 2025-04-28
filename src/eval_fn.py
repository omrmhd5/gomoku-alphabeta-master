import numpy as np
import piece


def evaluation_state(state, current_color, difficulty="Medium"):
    #Weaken evaluation for easy
    if difficulty == "Easy":
        # Return a very weak evaluation with lots of randomness
        # This will make the AI miss most strategic opportunities
        basic_eval = evaluate_color(state, piece.BLACK, current_color) * 0.2 + \
                    evaluate_color(state, piece.WHITE, current_color) * 0.2
        
        # Add random noise between -50 and 50 to make the Easy AI very unreliable
        random_factor = np.random.random() * 100 - 50  # Random value between -50 and 50
        return basic_eval + random_factor
    
    # For Medium and Hard difficulties, use the normal evaluation 
    if difficulty == "Medium":
        return evaluate_color(state, piece.BLACK, current_color) + \
               evaluate_color(state, piece.WHITE, current_color)
    else:  # Hard
        return (evaluate_color(state, piece.BLACK, current_color) + \
                evaluate_color(state, piece.WHITE, current_color)) * 1.3 #multiply normal evaluation by 1.3 to make decisions more "sharp" and "aggressive".
    
def evaluate_color(state, color, current_color):
    values = state.values
    size = state.size
    current = color == current_color
    evaluation = 0

    # evaluate rows and cols
    for i in range(size):
        evaluation += evaluate_line(values[i, :], color, current)
        evaluation += evaluate_line(values[:, i], color, current)

    # evaluate diagonals
    for i in range(-size + 5, size - 4):
        evaluation += evaluate_line(np.diag(values, k=i),
                                    color,
                                    current)
        evaluation += evaluate_line(np.diag(np.fliplr(values), k=i),
                                    color,
                                    current)

    return evaluation * color #the final score for each color


#Evaluates single row, column, or diagonal (line) for the specified color.
def evaluate_line(line, color, current):
    evaluation = 0
    size = len(line)
    # consecutive peices found
    consec = 0
    block_count = 2 #how many sides are blocked
    empty = False

    for i in range(len(line)):
        value = line[i]

        if value == color:
            # Found one of our pieces — keep building the consecutive count
            consec += 1

        elif value == piece.EMPTY and consec > 0:
            # Empty space after some consecutive pieces
            if not empty and i < size - 1 and line[i + 1] == color:
                # If it's the first empty spot and next piece is still ours, mark that there's a gap
                empty = True
            else:
                # Otherwise, the streak ends here — evaluate what we had
                evaluation += calc(consec, block_count - 1, current, empty)
                # Reset the streak counters
                consec = 0
                block_count = 1
                empty = False

        elif value == piece.EMPTY:
            # Empty space without any ongoing streak — we treat one side as open (not blocked)
            block_count = 1

        elif consec > 0:
            # Hit an opponent's piece after a streak — time to score what we built
            evaluation += calc(consec, block_count, current)
            # Reset streak counters
            consec = 0
            block_count = 2

        else:
            # Just an opponent's piece, no streak to worry about — fully blocked
            block_count = 2

    # After finishing the whole line, if we still have a streak going, score it
    if consec > 0:
        evaluation += calc(consec, block_count, current)

    return evaluation



def calc(consec, block_count, is_current, has_empty_space=False):
    # If both sides are blocked and we don't have 5 in a row, it's pretty much useless
    if block_count == 2 and consec < 5:
        return 0

    # If we have 5 or more consecutive pieces, that's either a win or close to it
    if consec >= 5:
        if has_empty_space:
            # A five-in-a-row with a gap somewhere is still strong, but not perfect
            return 8000
        else:
            # Clean five (or more) in a row with no gaps — massive win
            return 100000

    # Base scores depending on how many in a row we have (1-indexed)
    consec_score = (2, 5, 1000, 10000)
    
    # If one side is blocked, these penalties apply
    block_count_score = (0.5, 0.6, 0.01, 0.25)

    # If it's not our turn (evaluating opponent's potential), we lower the score
    not_current_score = (1, 1, 0.2, 0.15)

    # If there's a gap inside the sequence, slightly adjust the score
    empty_space_score = (1, 1.2, 0.9, 0.4)

    # Pick the right index based on how many pieces we have
    consec_idx = consec - 1
    value = consec_score[consec_idx]

    # If the sequence is only blocked on one side, adjust the score
    if block_count == 1:
        value *= block_count_score[consec_idx]

    # If we're evaluating an opponent's pieces, reduce the importance
    if not is_current:
        value *= not_current_score[consec_idx]

    # If there's an empty spot inside the sequence, adjust accordingly
    if has_empty_space:
        value *= empty_space_score[consec_idx]

    return int(value)
