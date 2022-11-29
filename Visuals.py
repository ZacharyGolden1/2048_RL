def print_board(board,score):
    print("\n") 
    for row in board:
        for num in board[row]:
            if num == 0:
                print("-","\t",end="")
            else:
                print(num,"\t",end="")
        print("\n",end="")
    print("score:",score)
    print("\n")
