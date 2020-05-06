from gomoku_ai import *
import copy

class BoardState:
    """Holds one state of the Gomoku board."""
    global testing
    testing = False 

    def __init__(self, to_move=None, utility=None, board=None, moves=None):
        # assume if to_move is not None, then neither are the rest
        if ((to_move == 0) or (to_move == 1)):
            self.to_move = to_move
            self._utility = utility
            self._board = board
            self._moves = moves
        else:
            self.create_initial_boardstate()

    def getPlayer(self):
        return self.to_move
    
    def create_initial_boardstate(self):
        """Create an initial boardstate with the default start state."""
        self.made_moves = set()
        self.search_region = set()
        self._board = [[Piece.EMPTY for x in range(SIZE)] for y in range(SIZE)]
        self.to_move = P0  # P0 has the first move 
        self._moves = self.calculate_legal_moves()
        self._utility = self.default_utility()
        self.new_move = None

    def check_legal_move(self, move):
        "A legal move must involve an empty position."
        if self._board[move[0]][move[1]] == Piece.EMPTY:
            return True
        else:
            return None
    
    def generate_search_region(self):
        """generate the region to be searched, involves one layer further from all the existing pieces"""
        for move in self.made_moves:  
            row, col = move
            if row > 0:
                self.search_region.add((row - 1, col))
            if col > 0:
                self.search_region.add((row, col - 1))
            if row > 0 and col > 0:
                self.search_region.add((row - 1, col - 1))
            if row > 0 and col < SIZE - 1:
                self.search_region.add((row - 1, col + 1))
            if row < SIZE - 1:
                self.search_region.add((row + 1, col))
            if col < SIZE - 1:
                self.search_region.add((row, col + 1))
            if row < SIZE -1 and col < SIZE - 1:
                self.search_region.add((row + 1, col + 1))
            if row < SIZE - 1 and col > 0:
                self.search_region.add((row + 1, col - 1))

    def legal_moves(self):
        "Return a list of legal moves for player."
        return self._moves

    def calculate_legal_moves(self):
        """Calculate the legal moves in the current BoardState."""
        moves = []
        for move in self.search_region:
            if self.check_legal_move((move[0], move[1])):
                moves.append(move)
        return moves

    def add_made_move(self, move):
        """Add the new move to the made moves list"""
        self.made_moves.add(move)

    def make_move(self, move):
        "Return a new copy of BoardState reflecting move made from given board state."
        newboardstate = copy.deepcopy(self)
        newboardstate.to_move = opponent(self.to_move)
        if self.to_move == P1:
            piece = Piece.O
        else:
            piece = Piece.X
        if move != None:
            newboardstate._board[move[0]][move[1]] = piece
            newboardstate.add_made_move(move)
            newboardstate.generate_search_region()

        newboardstate._moves = newboardstate.calculate_legal_moves()
        return newboardstate

    def default_utility (self):
        """estimates desirability of a move by evaluating the state that is the result of that move"""
        pattern_list = generate_pattern(self._board, self.made_moves)
        string_list = process_pattern_list(pattern_list)
        score = evaluate_list(string_list)
        if self.to_move == P0:
            result = score['x'] - score['o']
        else:
            result = score['o'] - score['x']
        return result

# Helper functions
def get_user_input():
    """get move from user and check if it is valid"""
    input_flag = False
    while not input_flag:
        user_input = input()
        if len(user_input) < 3:
            print("Invalid Input, please enter input of the format:row col")
            continue
        row, col = map(int, user_input.split(' '))
        if row >= SIZE or col >= SIZE:
            print("Invalid input, please enter row and column < ",SIZE)
            continue
        else:
            break
    return (row, col)

def opponent(player):
    """return the opponent of the player"""
    if player == 1:
        return 0
    elif player == 0:
        return 1