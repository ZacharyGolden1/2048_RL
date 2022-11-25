def print_board(board,score):
    print("\n") 
    for row in board:
        for num in board[row]:
            if num == None:
                print("-","\t",end="")
            else:
                print(num,"\t",end="")
        print("\n",end="")
    print("score:",score)
    print("\n")
