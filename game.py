from gomoku import *

class gomoku_player:
    """Human player"""
    def __init__(self, name):
        self.name = name

class gomoku_player2:
    """AI player"""
    def __init__(self, name):
        self.name = name

    def calculate_utility(self, boardstate):
        return boardstate.default_utility()

    def alphabeta_parameters(self, boardstate):
        return (2, None, None)

def play_gomoku(game=None, player1=gomoku_player("p1"), player2=gomoku_player2("p2")):
    "Play a 2-person, move-alternating Gomoku game."
    game = Gomoku()
    state = game.initial
    players = (player1, player2)
    game.display(state)
    while True:
        player = players[state.to_move]    
        game.current_player = player
        if (player == player2):
            params = player.alphabeta_parameters(state)
            print("Please be patient, AI is making a move...")  

            # search 1 layer deeper to determine if the next state is a win. If not, using alpha beta search to make optimal move
            terminal_test = False
            successor_list = [(move, game.make_move(move, state)) for move in game.legal_moves(state)]
            for (m,s) in successor_list:
                pattern_list = generate_pattern(s._board, s.made_moves)
                string_list = process_pattern_list(pattern_list)
                for sublist in string_list:
                    if sublist == O_PATTERNS[0] or sublist == X_PATTERNS[0]:
                        move = m
                        terminal_test = True
                    
            if not terminal_test:
                move = alphabeta_search(state, game, params[0], params[1], params[2])  
            state = game.make_move(move, state)
            game.add_made_move(move, state)
            game.generate_search_region(state)
        else:
            print("Enter move in the format: \"row[space]col\"")
            move = get_user_input()
            state = game.make_move(move, state)
            game.add_made_move(move, state)
            game.generate_search_region(state)

        print("Player: ", player.name, "took move ", move, "resulting in state:")
        game.display(state)

        if (not (winner_piece := game.terminal_test(state)) == Piece.EMPTY):
            winner = "X" if winner_piece == Piece.X else "O" 
            print ("player " + winner + " win!" )
            return "Game Over!!"  
            
play_gomoku(None, gomoku_player("User"), gomoku_player2("AI"))

