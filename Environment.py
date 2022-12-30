import numpy as np
import Moves
import tensorflow as tf

class environment():
    game_board = Moves.make_board()
    action_space = Moves.get_moves(game_board)
    score = 0
    num_actions = len(action_space)
    
    def __init__ (self, board = Moves.make_board()):
        self.game_board = board
        self.action_space = Moves.get_moves(self.game_board)
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
            self.action_space = Moves.get_moves(self.game_board)
            self.num_actions = len(self.action_space)
            # print("act",self.action_space)

            if not Moves.game_over(self.game_board):
                return self.game_board.flatten(), self.score-cur_score, False
            else:
                return self.game_board.flatten(), self.score-cur_score, True
        else:
            raise Exception(f"invalid move {move}")

    def reset(self):
        self.game_board = Moves.make_board()
        self.action_space = Moves.get_moves(self.game_board)
        self.score = 0
        self.num_actions = len(self.action_space)
        return self.game_board.flatten()
    
    def get_action_space(self):
        return self.action_space

    def get_actions(self):
        # debug output
        # print("get_actions",self.action_space,self.num_actions,"\n", self.game_board)
        return self.num_actions

    def clip_action_probs(self,possible_actions,action_probs):
        action_probs = np.array(action_probs[0])
        if 'd' not in possible_actions:
            action_probs[3] = 0
        if 's' not in possible_actions:
            action_probs[2] = 0
        if 'a' not in possible_actions:
            action_probs[1] = 0
        if 'w' not in possible_actions:
            action_probs[0] = 0
        action_probs = tf.convert_to_tensor(action_probs)
        return action_probs

def create_environment():
    return environment()