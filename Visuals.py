def print_board(board,score):
    for row in range(4):
        for col in range(4):
            if board[row,col] == 0:
                print("-","\t",end="")
            else:
                print(board[row,col],"\t",end="")
        print("\n",end="")
    print("score:",score)
    print("\n")
