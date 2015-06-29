"""
A simple clone of the popular game TicTacToe.
Implemented in Python 2. Can be run in any
web browser - visit www.codeskulptor.org to 
view, edit, run & play the game as you like.

Flexible board size with a computer opponent
using monte-carlo simulation to decide moves.
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator

NTRIALS = 100         # Number of trials to run. 10 = Easy mode, 100+ = Hard.
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    Run current game to completion using random moves
    """
    while board.check_win() == None:
        next_move = random.choice(board.get_empty_squares())
        board.move(next_move[0],next_move[1],player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    Updates the score table of every cell
    """

    if board.check_win() == provided.DRAW:
        return
    else:
        if board.check_win() == player:
            other_mod = 0
            current_mod = 1
        else:
            other_mod = 1
            current_mod = 0            
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row,col) == board.check_win():
                    scores[row][col] += SCORE_CURRENT*current_mod
                    scores[row][col] += SCORE_OTHER*other_mod
                elif board.square(row,col) != provided.EMPTY:
                    scores[row][col] -= SCORE_CURRENT*other_mod
                    scores[row][col] -= SCORE_OTHER*current_mod
                else:
                    pass
        return

def make_score_grid(size):
    """
    Helper function for testing the score updater.
    Creates a blank size x size score grid.
    """
    return [[0 for dummy_col in range(size)] for dummy_row in range(size)]

def get_best_move(board, scores):
    """
    Uses the score grid to return the 'best' move
    """
    move_list = board.get_empty_squares()
    good_moves = []
    score_list = []
    for move in move_list:
        score_list.append(scores[move[0]][move[1]])
    max_score = max(score_list)
    for score in range(len(score_list)):
        if score_list[score] == max_score:
            good_moves.append(move_list[score])
    return random.choice(good_moves)

def mc_move(board, player, trials):
    """
    Function to implement the best available move
    """
    scores = make_score_grid(board.get_dim())
    for dummy_i in range(trials):
        temp_board = board.clone()
        mc_trial(temp_board,player)
        mc_update_scores(scores, temp_board, player)
    return get_best_move(board,scores)
        
     
poc_ttt_gui.run_gui(4, provided.PLAYERX, mc_move, NTRIALS, False)

