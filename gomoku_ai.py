from enum import Enum

BigInitialValue = 100000000000
SIZE = 9   # change the size of the board here
PATTERN_SIZE = 5
TESTVAL = False

P0 = 0  # User # Piece.X
P1 = 1  # AI # Piece.O

class Piece(Enum):
    EMPTY = 0
    X = 1
    O = 2

def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    best = seq[0]
    best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
    return best

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    global BigInitialValue
    global testing
    testing = TESTVAL # set this to True when testing

    def max_value(state, alpha, beta, depth):
        if testing:
            print("  " * depth, "Max  alpha: ", alpha,
                  " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  " * depth, "Max cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = -BigInitialValue  # beta
        succ = game.successors(state)  # return (move, state) pairs
        if testing:
            print("  "*depth, "maxDepth: ", depth, "Successors: ", len(game.successors(state)))
        for (m, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            if state.to_move == s.to_move:
                v = max(v, max_value(s, alpha, beta, depth+1))
            else:
                v = max(v, min_value(s, alpha, beta, depth+1))
            if testing:
                print("  " * depth, "max best value:", v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if testing:
            print("  "*depth, "Min  alpha: ", alpha,
                  " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  "*depth, "Min cutoff returning ", eval_fn(state) ,"at depth" ,depth)
            return eval_fn(state)
        v = BigInitialValue  # alpha
        succ = game.successors(state)
        if testing:
            print("  "*depth, "minDepth: ", depth, "Successors: ", len(game.successors(state)))
        for (m, s) in succ:  
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            if state.to_move == s.to_move:
                v = min(v, min_value(s, alpha, beta, depth+1))
            else:
                v = min(v, max_value(s, alpha, beta, depth+1))
            if testing:
                print("  "*depth, "min best value:", v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def right_value(s, alpha, beta, depth):
        if s.to_move == state.to_move:
            return max_value(s, -BigInitialValue, BigInitialValue, 0)
        else:
            return min_value(s, -BigInitialValue, BigInitialValue, 0)

    # Body of alphabeta_search starts here:
    # The default test cuts off at  depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or (not game.terminal_test(state) == Piece.EMPTY) ))
    eval_fn = eval_fn or (lambda state: game.utility(state, game.current_player))
    move, state = argmax(game.successors(state), lambda a_s: right_value(a_s[1], -BigInitialValue, BigInitialValue, 0))
    return move     

def generate_pattern(board, made_moves):
    """Generate the list of all existing patterns of length 5 on the current board"""
    def row_pattern():
        nonlocal pattern_list, initial_row, initial_col
        pattern = []
        for col in range(initial_col, initial_col + PATTERN_SIZE):
            if (col == SIZE):
                break
            pattern.append(board[initial_row][col])
        if len(pattern) == PATTERN_SIZE:
            pattern_list.append(pattern)

    def col_pattern():
        nonlocal pattern_list, initial_row, initial_col
        pattern = []
        for row in range(initial_row, initial_row + PATTERN_SIZE):
            if (row == SIZE):
                break
            pattern.append(board[row][initial_col])
        if len(pattern) == PATTERN_SIZE:
            pattern_list.append(pattern)

    def diagonal1():
        nonlocal pattern_list, initial_row, initial_col
        pattern = []
        num = 0
        row = initial_row
        col = initial_col
        while (num < PATTERN_SIZE):
            pattern.append(board[row][col])
            row+=1
            col+=1
            num+=1
            if (row == SIZE or col == SIZE):
                break
        if len(pattern) == PATTERN_SIZE:
            pattern_list.append(pattern)

    def diagonal2():
        nonlocal pattern_list, initial_row, initial_col
        pattern = []
        num = 0
        row = initial_row
        col = initial_col
        while (num < PATTERN_SIZE):
            pattern.append(board[row][col])
            row+=1
            col-=1
            num+=1
            if (row == SIZE or col == -1):
                break
        if len(pattern) == PATTERN_SIZE:
            pattern_list.append(pattern)

    pattern_list = []
    for move in made_moves:
        initial_row = move[0]
        initial_col = move[1]
        # row
        row_pattern()
        # col
        col_pattern()
        # diagonal \
        diagonal1()
        # diagonal /
        diagonal2()   
    return pattern_list

X_PATTERNS = [  # straight5
                ['x', 'x', 'x', 'x', 'x'],  
                # open4, cap4   
                ['x','x','x','x','empty'],     
                ['o', 'x','x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'o'],
                # gap4
                ['x','empty', 'x','x','x'],
                ['x', 'x','empty','x','x'],
                ['x', 'x','x','empty','x'],
                # open3
                ['o', 'empty','x','x','x'],
                ['x','x','x','empty','o'],
                ['x','x','x','empty','empty'],
                # gap3
                ['x', 'empty', 'x','x','empty'],
                ['x', 'x','empty','x','empty'],
                ['x', 'empty', 'x','x','o'],
                ['x', 'x','empty','x','o'],
                # cap 3
                ['o', 'x', 'x','x','empty'],
                ['x', 'x', 'x','o','empty'],
                ['x', 'x', 'x','o','o'],
                # 2
                ['x', 'x', 'empty','empty','empty'],
                ['x', 'empty','x','empty','empty'],
                # 1
                ['x', 'empty','empty','empty','empty']]

O_PATTERNS = [  # straight5
                ['o', 'o', 'o', 'o', 'o'],  
                # open4, cap 4
                ['o','o','o','o','empty'],     
                ['x', 'o','o', 'o', 'o'],
                ['o', 'o', 'o', 'o', 'x'],
                # gap4
                ['o','empty', 'o','o','o'],
                ['o', 'o','empty','o','o'],
                ['o', 'o','o','empty','o'],
                # open3
                ['x', 'empty','o','o','o'],
                ['o','o','o','empty','x'],
                ['o','o','o','empty','empty'],
                # gap3
                ['o', 'empty', 'o','o','empty'],
                ['o', 'o','empty','o','empty'],
                ['o', 'empty', 'o','o','x'],
                ['o', 'o','empty','o','x'],
                # cap 3
                ['x', 'o', 'o','o','empty'],
                ['o', 'o', 'o','x','empty'],
                ['o', 'o', 'o','x','x'],
                # 2
                ['o', 'o', 'empty','empty','empty'],
                ['o', 'empty','x','empty','empty'],
                # 1
                ['o', 'empty','empty','empty','empty']]

SCORES = [
            # straight5
            1000000000,
            # open4, cap4 
            90000,50000,50000,
            # gap4
            100000, 100000, 100000,
            # open3
            10000, 10000, 15000,
            # gap3
            5000, 5000,1500, 1500,
            # cap 3
            1000, 1000, 500,
            # 2
            200, 200,
            # 1
            10]

def process_pattern_list(pattern_list):
    """Convert the list of Piece to list of string representing a pattern"""
    string_list = []
    string_sublist = []
    for sublist in pattern_list:
        string_sublist = []
        for piece in sublist:
            if piece == Piece.X:
                string_sublist.append('x')
            elif piece == Piece.O:
                string_sublist.append('o')
            else:
                string_sublist.append('empty')
        string_list.append(string_sublist)
    return string_list

def evaluate_list(string_list):
    """Compute the evaluation score for X player and O player based on the current board"""
    score = {'x': 0, 'o': 0}
    for sublist in string_list:
        for i in range(len(X_PATTERNS)):
            if sublist == X_PATTERNS[i]:
                score['x'] += SCORES[i]
            if sublist == O_PATTERNS[i]:
                score['o'] += SCORES[i]
    return score



