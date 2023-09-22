import random
import time
import argparse

import Parameters as param

from Visuals import *
from Moves import *

playing = True
score = 0
moves = ["w","a","s","d"]

# initialize board
game_board = make_board()

# game play loop
scores = []

# runs a single instance of a game:
def run_game(playing, game_board, score, moves):
    vBoard = visualBoard()
    while playing:
        vBoard.update(game_board, score)
        # check to see if the game is still playable:
        if param.verbose:
            if game_over(game_board):
                print_board(game_board,score)
                print("gameover, score:", score)
                scores.append(score)
                playing = False
                vBoard.root.quit()
        else:
            if game_over(game_board):
                scores.append(score)
                playing = False

        # get user move:
        if param.gamemode == "player":
            print_board(game_board,score)
            invalid = True
            while invalid:
                move = input("Enter move:")
                if move in moves and is_valid(move,game_board):
                    if move == "w":
                        game_board, score = up(game_board,score)
                    elif move == "a":
                        game_board, score = left(game_board,score)
                    elif move == "s":
                        game_board, score = down(game_board,score)
                    elif move == "d":
                        game_board, score = right(game_board,score)
                    
                    invalid = False
                else:
                    if not is_valid(move,game_board):
                        print("invalid move")
                    else:
                        print("invalid input, please enter 'w' or 'a' or 's' or 'd' and press enter")
                
        elif param.gamemode == "random":
            invalid = True
            moves = ["w","a","s","d"]
            while invalid and moves:
                move = random.choice(moves)
                moves.remove(move)
                if is_valid(move,game_board):
                    if move == "w":
                        game_board, score = up(game_board,score)
                    elif move == "a":
                        game_board, score = left(game_board,score)
                    elif move == "s":
                        game_board, score = down(game_board,score)
                    elif move == "d":
                        game_board, score = right(game_board,score)
                    
                    invalid = False
            
        elif param.gamemode == "down-right-left-up":
            if is_valid("s",game_board) and is_valid("d",game_board):
                move = random.randint(0,1)
                if move == 0:
                    game_board, score = down(game_board,score)
                if move == 1:
                    game_board, score = right(game_board,score)
            
            if is_valid("s",game_board):
                game_board, score = down(game_board,score)
            elif is_valid("d",game_board):
                game_board, score = right(game_board,score)
            elif is_valid("a",game_board):
                game_board, score = left(game_board,score)
            elif is_valid("w",game_board):
                game_board, score = up(game_board,score)

        elif param.gamemode == "ai":
            pass


###### for simulating games #####

t = time.time()
if param.simulation == True: # if simulation in Parameters.py is True then run num_simulations games
    for i in range(param.num_simulations):
        playing = True
        game_board = make_board()
        score = 0
        run_game(playing, game_board, score, moves)
else: # otherwise run a single game
    run_game(playing, game_board, score, moves)

if param.simulation == True:
    print("Time:",time.time() - t,"(s)")
    print("Mean:",sum(scores)/len(scores),"Max:", max(scores))
