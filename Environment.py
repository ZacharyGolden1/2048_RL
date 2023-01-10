import numpy as np
import Moves
import tensorflow as tf
import torch
from Disable_Print import *

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

    # resets the current environment back to a new board
    def reset(self):
        self.game_board = Moves.make_board()
        self.action_space = Moves.get_moves(self.game_board)
        self.score = 0
        self.num_actions = len(self.action_space)
        return self.game_board.flatten()
    
    # returns the current set of possible actions
    def get_action_space(self):
        return self.action_space

    # returns the number of actions available in the current environment
    def get_actions(self):
        # debug output
        # print("get_actions",self.action_space,self.num_actions,"\n", self.game_board)
        return self.num_actions

    # clip_action_probs removes invalid actions from the set of actions that the 
    # model might choose by setting their probability to zero,
    # since if a move is illegal the probability that it is the best move is zero
    def clip_action_probs(self,possible_actions,action_probs):
        action_probs = Moves.normalize(np.array(action_probs))
        if 'd' not in possible_actions:
            action_probs[3] = 0
        if 's' not in possible_actions:
            action_probs[2] = 0
        if 'a' not in possible_actions:
            action_probs[1] = 0
        if 'w' not in possible_actions:
            action_probs[0] = 0
        return Moves.normalize(action_probs)
    
    # state_to_one_hot returns a one hot representation of the current game board 
    # (or passed in game board) which can be passed to the model
    def state_to_one_hot(self):
        return tf.reshape(tf.one_hot(np.log2(self.game_board.flatten(),where=self.game_board.flatten()>0),16),[-1])

def state_to_one_hot(state):
    return tf.reshape(tf.one_hot(np.log2(state.flatten(),where=state.flatten()>0),16),[-1])

def create_environment():
    return environment()