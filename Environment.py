import numpy as np
import Moves

class environment():
    action_space = ["w","a","s","d"]
    observation_space = np.zeros(16)
    
    def __init__ (self, board = np.zeros((4,4))):
        self.observation_space = board.flatten()

    def _seed ():
        pass

    def _step(move):
        if Moves.is_valid(move,game_board):
            if move == "w":
                game_board, score = Moves.up(game_board,score)
            elif move == "a":
                game_board, score = Moves.left(game_board,score)
            elif move == "s":
                game_board, score = Moves.down(game_board,score)
            elif move == "d":
                game_board, score = Moves.right(game_board,score)

    def _reset():
        return Moves.make_board()
