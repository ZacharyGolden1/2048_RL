from tkinter import *
from tkinter import ttk
import numpy as np

# The colors associated with each level of tile (taken from https://projectgurukul.org/python-2048-game/)
bg_color={
    '2': '#eee4da',
    '4': '#ede0c8',
    '8': '#edc850',
    '16': '#edc53f',
    '32': '#f67c5f',
    '64': '#f65e3b',
    '128': '#edcf72',
    '256': '#edcc61',
    '512': '#f2b179',
    '1024': '#f59563',
    '2048': '#edc22e',
}
color={
    '2': '#776e65',
    '4': '#f9f6f2',
    '8': '#f9f6f2',
    '16': '#f9f6f2',
    '32': '#f9f6f2',
    '64': '#f9f6f2',
    '128': '#f9f6f2',
    '256': '#f9f6f2',
    '512': '#776e65',
    '1024': '#f9f6f2',
    '2048': '#f9f6f2',
}

# A class that creates a visual GUI of a board
class visualBoard:
    # on init create a window and populate it with a board
    def __init__(self) -> None:
         # Set up the window
        self.root = Tk()
        self.root.title("2048")

        # Create the content frame
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # set up tiles
        self.visual_board = []
        for i in range(1,5):
            row=[]
            for j in range(4):
                l=Label(self.mainframe,text='', background='azure4',
                        font=('arial',22,'bold'),width=4,height=2)
                l.grid(row=i,column=j,padx=7,pady=10,sticky=(N, W, E, S))
                row.append(l)
            self.visual_board.append(row)
        
        # set up the score
        self.visual_score = Label(self.mainframe,text='0',background='azure4',
                                  font = ('arial',22,'bold'),width=4,height=1)
        self.visual_score.grid(row=0,column=3)

    # upadate the board with a new board state and score
    def update(self,board,score):
        # update the score
        self.visual_score.config(text=str(score))

        # go through each tile and update it
        for i in range(4):
            for j in range(4):
                if board[i][j]==0:
                    self.visual_board[i][j].config(text='',bg='azure4')
                else:
                    self.visual_board[i][j].config(text=str(board[i][j]),
                    bg=bg_color[str(board[i][j])],
                    fg=color[str(board[i][j])])
        self.root.update_idletasks()
        self.root.update()

# print_board will print out the state of the board and score passed to it to stdout
# intended for if you want to use the terminal text based display
def print_board(board,score):
    print("\n") 
    for row in range(4):
        for col in range(4):
            if board[row,col] == 0:
                print("-","\t",end="")
            else:
                print(board[row,col],"\t",end="")
        print("\n",end="")
    print("score:",score)
    print("\n")

def demo_board():
    vboard = visualBoard()
    print("Running the visual demo:")
    board = np.zeros((4,4))
    board[1,3] = 4
    vboard.update(board,40)