import numpy as np
import Moves

class environment():
    action_space = ["w","a","s","d"]
    game_board = Moves.make_board()
    score = 0
    num_actions = 4
    
    def __init__ (self, board = Moves.make_board()):
        self.game_board = board
        moves = []
        for move in ["w","a","s","d"]:
            if Moves.is_valid(move,self.game_board):
                moves.append(move)
        self.action_space = moves
        self.num_actions = len(self.action_space)

    def _seed ():
        pass

    def step(self,move_int):
        move = self.action_space[move_int]
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
            
            # update valid moves:
            moves = []
            for move in ["w","a","s","d"]:
                if Moves.is_valid(move,self.game_board):
                    moves.append(move)
            self.action_space = moves
            self.num_actions = len(self.action_space)
            # print("act",self.action_space)

            if not Moves.game_over(self.game_board):
                return self.game_board.flatten(), self.score-cur_score, False
            else:
                return self.game_board.flatten(), self.score-cur_score, True
        else:
            raise Exception(f"invalid move {move} in board state:\n {self.game_board}")

    def reset(self):
        self.action_space = ["w","a","s","d"]
        self.game_board = Moves.make_board()
        self.score = 0
        self.num_actions = 4
        return self.game_board.flatten()
    
    def get_actions(self):
        # debug output
        # print("get_actions",self.action_space,self.num_actions,"\n", self.game_board)
        return self.num_actions

def create_environment():
    return environment()