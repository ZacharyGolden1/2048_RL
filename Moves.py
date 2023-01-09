import random
import numpy as np
import tensorflow as tf

# create board:
def make_board():
    board = np.zeros((4,4),dtype=int)

    empty_squares = get_empty_squares(board)
    (x,y) = get_random_empty_square(empty_squares)
    board[x,y] = random.choice([2,4])

    empty_squares = get_empty_squares(board)
    (x,y) = get_random_empty_square(empty_squares)
    board[x,y] = random.choice([2,4])
    return board

# get all empty squares:
def get_empty_squares(board):
    empty_squares = []
    for i in range(4):
        for j in range(4):
            if board[i,j] == 0:
                empty_squares.append((i,j))
    return empty_squares

# pick random empty square:
def get_random_empty_square(empty_squares):
    coords = random.choice(empty_squares)
    return coords

# moves
def up(board,score):
    # get rid of all zeroes in the board
    new_board = dict()
    for col in range(4):
        new_board[col] = []
        for row in range(4):
            if board[row,col] != 0:
                new_board[col].append(board[row,col])
                
    # combine like numbers:
    for col in range(4):
        i = 0
        while i < len(new_board[col]) - 1:
            if new_board[col][i] == new_board[col][i+1]:
                new_board[col][i] = 2*new_board[col][i]
                score += new_board[col][i]
                new_board[col].pop(i+1)
            i+=1

    # add back zeroes:
    for col in range(4):
        while len(new_board[col]) < 4:
            new_board[col].append(0)

    # transpose
    final_board = make_board()
    for i in range(4):
        for j in range(4):
            final_board[i,j] = new_board[j][i]

    # at the beginning of each turn pick a random square that does not have a 
    # number in it and set it to either 2 or 4
    empty_squares = get_empty_squares(final_board)
    try:
        (x,y) = get_random_empty_square(empty_squares)
    except:
        pass
    final_board[x,y] = random.choice([2,4])

    return final_board,score

def down(board,score):
    # get rid of all zeros in the board
    new_board = dict()
    for col in range(4):
        new_board[col] = []
        for row in range(4):
            if board[row,col] != 0:
                new_board[col].append(board[row,col])
                
    # combine like numbers:
    for row in range(4):
        i = len(new_board[row]) - 1
        while i > 0:
            if new_board[row][i] == new_board[row][i-1]:
                new_board[row][i] = 2*new_board[row][i]
                score += new_board[row][i]
                new_board[row].pop(i-1)
            i-=1

    # add back zeros:
    for col in range(4):
        while len(new_board[col]) < 4:
            new_board[col].insert(0, 0)

    # transpose
    final_board = make_board()
    for i in range(4):
        for j in range(4):
            final_board[i,j] = new_board[j][i]

    # at the beginning of each turn pick a random square that does not have a 
    # number in it and set it to either 2 or 4
    empty_squares = get_empty_squares(final_board)
    try:
        (x,y) = get_random_empty_square(empty_squares)
    except:
        pass
    final_board[x,y] = random.choice([2,4])

    return final_board, score

def left(board,score):
    # get rid of all zeroes in the board
    new_board = dict()
    for row in range(4):
        new_board[row] = []
        for col in range(4):
            if board[row,col] != 0:
                new_board[row].append(board[row][col])
                
    # combine like numbers:
    for row in range(4):
        i = 0
        while i < len(new_board[row]) - 1:
            if new_board[row][i] == new_board[row][i+1]:
                new_board[row][i] = 2*new_board[row][i]
                score += new_board[row][i]
                new_board[row].pop(i+1)
            i+=1

    # add back zeroes:
    for row in range(4):
        while len(new_board[row]) < 4:
            new_board[row].append(0)
    
    # make into a np.array
    final_board = make_board()
    for i in range(4):
        for j in range(4):
            final_board[i,j] = new_board[i][j]
    
    # at the beginning of each turn pick a random square that does not have a 
    # number in it and set it to either 2 or 4
    empty_squares = get_empty_squares(final_board)
    try:
        (x,y) = get_random_empty_square(empty_squares)
    except:
        pass
    final_board[x,y] = random.choice([2,4])

    return final_board, score

def right(board,score):
    # get rid of all Nones in the board
    new_board = dict()
    for row in range(4):
        new_board[row] = []
        for col in range(4):
            if board[row][col] != 0:
                new_board[row].append(board[row,col])
                
    # combine like numbers:
    for row in range(4):
        i = len(new_board[row]) - 1
        while i > 0:
            if new_board[row][i] == new_board[row][i-1]:
                new_board[row][i] = 2*new_board[row][i]
                score += new_board[row][i]
                new_board[row].pop(i-1)
            i-=1

    # add back Zeroes:
    for row in range(4):
        while len(new_board[row]) < 4:
            new_board[row].insert(0, 0)
    
    # make into a np.array
    final_board = make_board()
    for i in range(4):
        for j in range(4):
            final_board[i,j] = new_board[i][j]
    
    # at the beginning of each turn pick a random square that does not have a 
    # number in it and set it to either 2 or 4
    empty_squares = get_empty_squares(final_board)
    try:
        (x,y) = get_random_empty_square(empty_squares)
    except:
        pass
    final_board[x,y] = random.choice([2,4])

    return final_board, score

# check if a move is valid:
def is_valid(move,board):
    # left
    if move == "a":
        for row in range(4):
            for col in range(3):
                if board[row,col] == board[row,col+1] and board[row,col+1] != 0:
                    return True
                elif board[row,col] == 0 and board[row,col+1] != 0:
                    return True

    # right
    elif move == "d":
        for row in range(4):
            for col in range(3,0,-1):
                if board[row,col] == board[row,col-1] and board[row,col-1] != 0:
                    return True
                elif board[row,col] == 0 and board[row,col-1] != 0:
                    return True
    
    # down
    elif move == "s":
        for col in range(4):
            for row in range(3,0,-1):
                if board[row,col] == board[row-1,col] and board[row-1,col] != 0:
                    return True
                elif board[row,col] == 0 and board[row-1,col] != 0:
                    return True

    # up
    elif move == "w":
        for col in range(4):
            for row in range(3):
                if board[row,col] == board[row+1,col] and board[row+1,col] != 0:
                    return True
                elif board[row,col] == 0 and board[row+1,col] != 0:
                    return True
    return False

# get all valid moves on current board:
def get_moves(board):
    moves = []
    for move in ["w","a","s","d"]:
        if is_valid(move,board):
            moves.append(move)
    return moves

# check if the game is over:
def game_over(board):
    moves = ["w","a","s","d"]
    for move in moves:
        if is_valid(move,board):
            return False
    return True

# normalize function for the returned model values
def normalize(arr):
    return tf.keras.utils.normalize(arr)[0]