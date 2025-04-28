import numpy as np
import piece


class BoardState:
    def __init__(self, size, values=None, evals=None, color=piece.WHITE):
        # initialize the board values
        if np.all(values != None):         
            self.values = np.copy(values) # if exist, copy the exist board
        else:
            self.values = np.full((size, size), piece.EMPTY) # else, create an empty board

        self.size = size # size of board
        self.color = color # current player's color
        self.last_move = None # last move played
        self.winner = 0 

    def value(self, position):
        return self.values[position]

    def is_valid_position(self, position):
        # check if a position is inside the board and is currently empty
        return (is_valid_position(self.size, position)
                and self.values[position] == piece.EMPTY)

    def legal_moves(self):
        # find all valid moves near existing pieces
        prev_move_idxs = self.values != piece.EMPTY
        area_idxs = expand_area(self.size, prev_move_idxs)
        return np.column_stack(np.where(area_idxs == True))

    def next(self, position):
        # create the next board state after playing a move (switch player color, set new move, save last move)
        next_state = BoardState(size=self.size,
                                values=self.values,
                                color=-self.color)
        next_state[position] = next_state.color 
        next_state.last_move = tuple(position)
        return next_state

    def is_terminal(self):
        # check if the game has ended either by win or board full
        is_win, color = self.check_five_in_a_row()
        is_full = self.is_full()
        if is_full:
            return True
        return is_win

    def check_five_in_a_row(self):
        pattern = np.full((5,), 1)

        black_win = self.check_pattern(pattern * piece.BLACK)
        white_win = self.check_pattern(pattern * piece.WHITE)

        if black_win:
            self.winner = piece.BLACK
            return True, piece.BLACK
        if white_win:
            self.winner = piece.WHITE
            return True, piece.WHITE
        return False, piece.EMPTY

    def is_full(self):
        return not np.any(self.values == piece.EMPTY)

    def check_pattern(self, pattern):
        # check how many lines (row, column, diagonal) match a given pattern
        count = 0
        for line in self.get_lines():
            if issub(line, pattern):
                count += 1
        return count

    def get_lines(self):
        # generator to yield all rows, columns, and diagonals
        l = []

        # add all rows and cols
        for i in range(self.size):
            l.append(self.values[i, :])
            l.append(self.values[:, i])

        # add all 2 diagonals
        for i in range(-self.size + 5, self.size - 4):
            l.append(np.diag(self.values, k=i))
            l.append(np.diag(np.fliplr(self.values), k=i))

        # yield each collected line
        for line in l:
            yield line

    def __getitem__(self, position):
        # enable board[i,j] to get a value
        i, j = position
        return self.values[i, j]

    def __setitem__(self, position, value):
        # set a value
        i, j = position
        self.values[i, j] = value

    def __str__(self):
        out = ' ' * 3
        out += '{}\n'.format(''.join(
            '{}{}'.format((i + 1) % 10, i < 10 and ' ' or "'")
            for i in range(self.size)
        ))

        for i in range(self.size):
            out += '{}{} '.format(i + 1 < 10 and ' ' or '', i + 1)
            for j in range(self.size):
                out += piece.symbols[self[i, j]]
                if self.last_move and (i, j) == tuple(self.last_move):
                    out += '*'
                else:
                    out += ' '
            if i == self.size - 1:
                out += ''
            else:
                out += '\n'
        return out

    def __repr__(self):
        return self.__str__()


def issub(l, subl):
    # get lengths of main list and sublist
    l_size = len(l)
    subl_size = len(subl)
    # iterate through the main list, checking slices of size equal to the sublist
    for i in range(l_size - subl_size):
        curr = l[i:min(i + subl_size, l_size - 1)]
        if (curr == subl).all():
            return True
    return False    # no matching slice


def expand_area(size, idxs):
    # create a copy of the input index matrix to modify
    area_idxs = np.copy(idxs)
    # loop through every cell on the board
    for i in range(size):
        for j in range(size):
            if not idxs[i, j]: # if cell is empty, skip
                continue

            # for each direction (horizontal, vertical, and 2 diagonals)
            for direction in ((1, 0), (0, 1), (1, 1), (1, -1)):
                di, dj = direction
                # check both positive and negative directions
                for side in (1, -1):
                    ni = i + di * side
                    nj = j + dj * side
                    if not is_valid_position(size, (ni, nj)): # if new position is invalid, skip
                        continue
                    area_idxs[ni, nj] = True
    # return new cells around existing pieces
    # using xor to remove original occupied cells from the result 
    return np.bitwise_xor(area_idxs, idxs)


def is_valid_position(board_size, position):
    # check if the position is a tuple with exactly two elements (row, column)
    if not isinstance(position, tuple) or len(position) != 2:
        return False
    i, j = position
    # check if both row (i) and column (j) are within board boundaries
    return i >= 0 and i < board_size and j >= 0 and j < board_size
