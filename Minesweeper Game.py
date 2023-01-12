from tkinter import *
from tkinter import messagebox
import random

class MinesweeperSquare(Label):
    '''represents a Minesweeper square'''

    def __init__(self, master, coord):
        '''MinesweeperSquare(master, coord) -> MinesweeperSquare
        creates a new MinesweeperSquare with (row, column) coord'''
        Label.__init__(self, master, height = 1, width = 2, text = '', \
                       bg = 'white', font = ('Trebuchet MS', 16), relief = 'raised')
        self.coord = coord  # (row, column) coordinate tuple
        self.exposed = False    # starts as blank
        self.flagged = False    # starts as blank
        self.number = 0     # changes after first click
        # set up listeners
        self.bind('<Button-1>', self.reveal)
        self.bind('<Button-2>', self.flag)
        self.bind('<Button-3>', self.flag)

    def get_coord(self):
        '''MinesweeperSquare.get_coord() -> tuple
        returns the (row, column) coordinate of the square'''
        return self.coord

    def get_number(self):
        '''MinesweeperSquare.get_number() -> int
        returns the number of the square'''
        return self.number

    def is_bomb(self):
        '''MinesweeperSquare.is_bomb() -> bool
        returns True if the square is a bomb'''
        if self.number == -1:
            return True
        return False

    def is_exposed(self):
        '''MinesweeperSquare.is_exposed() -> bool
        returns True if the square is exposed'''
        return self.exposed

    def is_flagged(self):
        '''MinesweeperSquare.is_flagged() -> bool
        returns True if the square has been flagged'''
        return self.flagged

    def set_number(self, number):
        '''MinesweeperSquare.set_number(number)
        sets the number of the square'''
        self.number = number

    def auto_reveal(self):
        '''MinesweeperSquare.auto_reveal()
        reveals the squares signified in master.auto_expose()'''
        if self.exposed == False and not self.flagged:
            self.exposed = True
            self['bg'] = 'light gray'
            self['relief'] = 'sunken'
            if self.number == 0:
                self.master.auto_expose(self.coord)
            elif self.number > 0:
                colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
                self['fg'] = colormap[self.number]
                self['text'] = str(self.number)
        
    def reveal(self, event):
        '''MinesweeperSquare.reveal(event)
        handler function for left mouse click
        exposes the square clicked on'''
        if not self.flagged and not self.master.done:
            if self.master.get_firstMove():
                self.master.set_up(self.coord)
            if self.number == -1:
                self['text'] = '*'
                self['bg'] = 'red'
                self.master.lose()
            elif self.number == 0:
                self.exposed = True
                self['bg'] = 'light gray'
                self['relief'] = 'sunken'
                self.master.auto_expose(self.coord)
            else:
                self.exposed = True
                colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
                self['bg'] = 'light gray'
                self['relief'] = 'sunken'
                self['fg'] = colormap[self.number]
                self['text'] = str(self.number)
        self.master.win()

    def flag(self, event):
        '''MinesweeperSquare.flag(event)
        handler funtion for right mouse click
        flags the square clicked on'''
        if not self.exposed and not self.master.done:
            if self.flagged == False:
                self.flagged = True
                self['text'] = '*'
                self.master.set_numBombs(-1)
            else:
                self.flagged = False
                self['text'] = ''
                self.master.set_numBombs(1)
            

class MinesweeperBoard(Frame):
    '''object for a Minesweeper board'''

    def __init__(self, master, width, height, numBombs):
        '''MinesweeperBoard(master, width, height, numBombs) -> MinesweeperBoard
        creates a new Minesweeper board'''
        self.width = width
        self.height = height
        self.ogNumBombs = numBombs
        self.numBombs = numBombs
        self.firstMove = True    # the player has not done anything yet
        self.done = False
        # initialize a new Frame
        Frame.__init__(self, master, bg = 'black')
        self.grid()
        # create the squares
        self.squares = {}   # set up dictionary for squares
        for column in range(width):
            for row in range(height):
                coord = (column, row)
                self.squares[coord] = MinesweeperSquare(self, coord)
                self.squares[coord].grid(row = row, column = column)
        # create the counter
        self.counter = Label(self, height=1, width=3, text= str(numBombs), \
                       bg = 'white', font = ('Trebuchet MS', 24))
        self.counter.grid(row = height + 1, columnspan = width)

    def lose(self):
        '''MinesweeperBoard.lose()
        displays lose message and exposes remaining bombs'''
        self.done = True
        messagebox.showerror('Mineweeper', 'KABOOM! You lose.', parent = self)
        squares = list(self.squares.values())
        for square in squares:  # reveal unmarked bombs
            if square.is_bomb() and not square.is_flagged():
                square['text'] = '*'
                square['bg'] = 'red'
            elif not square.is_bomb() and square.is_flagged():  # reveal wrongfully marked squares
                square['text'] = str(square.get_number())
                square['bg'] = 'red'
        self.counter.grid_remove()
        Button(self, text='Play Again',command=self.play_again).grid(row=self.height+1,columnspan=self.width)

    def win(self):
        '''MinesweeperBoard.win()
        displays win message'''
        for square in self.squares.values():
            if square.is_exposed():
                win = True
            elif not square.is_exposed() and not square.is_bomb():
                win = False
                break
        if win:
            self.done = True
            messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent = self)
            self.counter.grid_remove()
            Button(self, text='Play Again',command=self.play_again).grid(row=self.height+1,columnspan=self.width)            

    def auto_expose(self, coord):
        '''MinesweeperBoard.auto_expose(coord)
        reveals all squares next to square at coord'''
        for column in range(coord[0] - 1, coord[0] + 2):
            for row in range(coord[1] - 1, coord[1] + 2):
                if column!=-1 and row!=-1 and column!=self.width and row!=self.height:
                    coordinate = (column, row)
                    self.squares[coordinate].auto_reveal()

    def set_up(self, coord):
        '''MinesweeperBoard.set_up(coord)
        sets up the board after the first click
        coord cannot be a bomb'''
        self.firstMove = False
        squares = list(self.squares.values())
        surroundSquares = list()    # the squares surrounding the first click cannot be bombs
        for x in range(coord[0]-1,coord[0]+2):
            for y in range(coord[1]-1,coord[1]+2):
                surroundSquares.append((x,y))
        for i in range(self.numBombs):  # set up the bombs
            bomb = random.choice(squares)
            while bomb.get_number() == -1 or bomb.get_coord() in surroundSquares:
                bomb = random.choice(squares)
            bomb.set_number(-1)
        for square in squares:  # set the number of the other squares
            if square.get_number() != -1:
                number = 0
                coordinate = square.get_coord()
                for column in range(coordinate[0] - 1, coordinate[0] + 2):
                    for row in range(coordinate[1] - 1, coordinate[1] + 2):
                        if column!=-1 and row!=-1 and column!=self.width and row!=self.height:
                            adjacent = (column, row)
                            if self.squares[adjacent].is_bomb():
                                number += 1
                square.set_number(number)

    def get_firstMove(self):
        '''MinesweeperBoard.get_firstMove() -> bool
        returns self.firstMove'''
        return self.firstMove

    def set_numBombs(self, change):
        '''MinesweeperBoard.set_numBombs(change)
        adds change to numBombs and updates counter'''
        self.numBombs += change
        self.counter['text'] = str(self.numBombs)

    def play_again(self):
        '''MinesweeperBoard.play_again()
        resets the board'''
        self.destroy()
        MinesweeperBoard(self.master, self.width, self.height, self.ogNumBombs)

def minesweeper(width=15, height=15, numBombs=25):
    root = Tk()
    root.title('Minesweeper')
    MinesweeperBoard(root, width, height, numBombs)
    root.mainloop()

minesweeper()
