from boardstate import *

class Gomoku():
    global testing
    testing = TESTVAL

    def __init__(self):
        self.current_state = BoardState()
        self.initial = self.current_state

    def display(self, boardstate):
        "Print out the board in a readable way."
        print("  ",end='')
        for i in range (SIZE):
            print (str(i),"     ",end='')
        print()
        for i in range(SIZE):
            for j in range(SIZE):
                if boardstate._board[i][j] == Piece.EMPTY:
                    print('[   ]',' ',end='')
                else:    
                    piece = 'X' if boardstate._board[i][j] == Piece.X else 'O'
                    print('[',piece,']',' ',end='')
            print(i) 
        print("----------------------------------------------------------------")

    def legal_moves(self, boardstate):
        "Return a list of legal moves for player."
        def check_legal_move(move):
            "A legal move must involve an empty position."
            if boardstate._board[move[0]][move[1]] == Piece.EMPTY:
                return True
            else:
                return None
        moves = []
        for move in boardstate.search_region:
            if check_legal_move((move[0], move[1])):
                moves.append(move)
        return moves

    def add_made_move(self, move, boardstate):
        """Add the new move to the made moves list"""
        boardstate.made_moves.add(move)
        boardstate.new_move = move
    
    def generate_search_region(self, boardstate):
        """generate the region to be searched, involves one layer further from all the existing pieces"""
        for move in boardstate.made_moves:  
            row, col = move
            if row > 0:
                boardstate.search_region.add((row - 1, col))
            if col > 0:
                boardstate.search_region.add((row, col - 1))
            if row > 0 and col > 0:
                boardstate.search_region.add((row - 1, col - 1))
            if row > 0 and col < SIZE - 1:
                boardstate.search_region.add((row - 1, col + 1))
            if row < SIZE - 1:
                boardstate.search_region.add((row + 1, col))
            if col < SIZE - 1:
                boardstate.search_region.add((row, col + 1))
            if row < SIZE -1 and col < SIZE - 1:
                boardstate.search_region.add((row + 1, col + 1))
            if row < SIZE - 1 and col > 0:
                boardstate.search_region.add((row + 1, col - 1))

    def make_move(self, move, boardstate):
        "Return a new BoardState reflecting move made from given board state."
        if (not boardstate._board[move[0]][move[1]] == Piece.EMPTY):
            print("Occupied spot, please choose another position")
            move = get_user_input()
        newBoard = boardstate.make_move(move)
        return newBoard

    def calculate_utility(self, boardstate):
        """Calculate the utility of this state"""
        return boardstate.default_utility()

    def utility(self, boardstate, player):
        "This is where your utility function gets called."
        return player.calculate_utility(boardstate)

    def terminal_test(self, boardstate):
        "Return True if this is a final state for the game, check if anyone has 5 in a row by checking around the latest move"
        initial_row = boardstate.new_move[0]
        initial_col = boardstate.new_move[1]
        board = boardstate._board
        initial_piece = board[initial_row][initial_col]

        # check horizontally
        row = initial_row
        col = initial_col
        count = 0
        # --->
        while (col < SIZE and board[row][col] == initial_piece):
            count+=1
            col+=1
        # <---
        col = initial_col - 1
        while (col >= 0 and board[row][col] == initial_piece):
            count+=1
            col-=1
        
        # check vertically
        row = initial_row
        col = initial_col
        count = 0
        # down
        while (row < SIZE and board[row][col] == initial_piece):
            count+=1
            row+=1
        # up
        row = initial_row - 1
        while (row >= 0 and board[row][col] == initial_piece):
            count+=1
            row-=1
        
        # check diagonally /
        row = initial_row
        col = initial_col
        count = 0
        # --->
        while (row >=0 and col < SIZE and board[row][col] == initial_piece):
            count+=1
            row-=1
            col+=1
        # <---
        row = initial_row + 1
        col = initial_col - 1
        while (col >= 0 and row >= 0 and row < SIZE and board[row][col] == initial_piece):
            count+=1
            row+=1
            col-=1

        # check diagonally \
        row = initial_row
        col = initial_col
        count = 0
        # --->
        while (row < SIZE and col < SIZE and board[row][col] == initial_piece):
            count+=1
            row+=1
            col+=1
        # <---
        row = initial_row - 1
        col = initial_col - 1
        while (col >= 0 and row >= 0 and board[row][col] == initial_piece):
            count+=1
            row-=1
            col-=1

        if count == 5:
            return initial_piece
        else:
            return Piece.EMPTY

    def to_move(self, boardstate):
        "Return the player whose move it is in this state."
        return boardstate.to_move

    def successors(self, boardstate):
        "Return a list of legal (move, boardstate) pairs."
        successor_list = [(move, self.make_move(move, boardstate)) for move in self.legal_moves(boardstate)]
        return successor_list
   