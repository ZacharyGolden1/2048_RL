import numpy as np
import Moves

class environment():
    action_space = ["w","a","s","d"]
    game_board = Moves.make_board()
    score = 0
    
    def __init__ (self, board = np.zeros((4,4),dtype=int),actions = ["w","a","s","d"]):
        self.game_board = board
        self.action_space = actions

    def _seed ():
        pass

    def step(self,move):
        if Moves.is_valid(move,self.game_board):
            cur_score = self.score
            if move == "w":
                self.game_board, self.score = Moves.up(self.game_board,self.score)
            elif move == "a":
                self.game_board, self.score = Moves.left(self.game_board,self.score)
            elif move == "s":
                self.game_board, self.score = Moves.down(self.game_board,self.score)
            elif move == "d":
                self.game_board, self.score = Moves.right(self.game_board,self.score)
            
            if not Moves.game_over(self.game_board):
                return self.game_board, self.score-cur_score, False
            else:
                return self.game_board, self.score-cur_score, True
        else:
            raise Exception("invalid move")

    def reset(self):
        return environment()

def create_environment():
    return environment()
