# Note: This game does not work exactly as it's supposed to
# There is a small glitch where sometimes the tile does not move all the way
# If the two tiles in front of it merge

from tkinter import *
import random
import math

class NumberTile(Label):
    '''represents a number tile'''

    def __init__(self, master, coord):
        '''NumberTile(master, identifier, coord) -> NumberTile
        creates a new NumberTile with identifier and (row, column) coord'''
        Label.__init__(self, master, height=2, width=4, text = '', \
                       bg = ('#ccc2b4'), font = ('Arial',32,'bold'), relief = 'solid')
        self.coord = coord  # (row, column) coordinate tuple
        self.number = 0
        self.justChanged = False

    def change_number(self):
        '''NumberTile.change_number()
        changes the value and color of the tile'''
        colormap = ['','#eee5dB','#eee1c9','#f4b279','#f79664','#f77d60', \
                    '#f65f3b','#edd073','#eecc62','#edc951','#edc53e','#edc22f']
        if self.number == 0:
            self.number = random.choice((2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        else:
            self.number *= 2
        self['text'] = str(self.number) #display number
        if self.number > 2048:  #set background color
            self['bg'] = '#3d3a32'
        else:
            self['bg'] = colormap[int(math.log(self.number, 2))]
        if self.number < 8: #set font color
            self['fg'] = '#776d66'
        else:
            self['fg'] = '#fcf4f3'

    def reset(self):
        '''NumberTile.reset()
        changes the value of the tile to 0'''
        self.number = 0
        self['text'] = str('')
        self['bg'] = ('#ccc2b4')
        
    def change_coord(self, coord):
        '''NumberTile.change_coord
        changes the (row, column) coordinates of the tile'''
        self.coord = coord

    def is_blank(self):
        '''NumberTile.is_numbered -> boolean
        returns the number status of the tile'''
        if self.number == 0:
            return True
        return False

    def get_number(self):
        '''NumberTile.get_number() -> int
        returns the number value of the tile'''
        return self.number

    def get_coord(self):
        '''NumberTile.get_coord() -> tuple
        returns the (row, column) coordinate of the tile'''
        return self.coord

    def just_changed(self):
        '''NumberTile.just_changed() -> boolean
        returns self.justChanged status'''
        return self.justChanged

    def switch_justChanged(self):
        '''NumberTile.switch_justChanged()
        changes the status of self.justChanged'''
        if self.justChanged:
            self.justChanged = False
        else:
            self.justChanged = True

class GameBoard(Frame):
    '''object for a 2048 board'''

    def __init__(self, master):
        '''GameBoard(master) -> GameBoard
        creates a new 2048 board'''
        # initialize a new frame
        Frame.__init__(self, master)
        self.grid()
        # create the tiles
        self.tiles = []     # set up list for tiles
        identifier = 0
        for row in range(4):
            for column in range(4):
                coord = (row, column)
                self.tiles.append(NumberTile(self, coord))
                self.tiles[identifier].grid(row=row, column=column)
                identifier += 1
        random.choice(self.tiles).change_number()
        # set up listeners
        self.master.bind('<Left>', self.left)
        self.master.bind('<Right>', self.right)
        self.master.bind('<Up>', self.up)
        self.master.bind('<Down>', self.down)

    def new_number(self):
        '''GameBoard.new_number()
        creates a new 2 or 4 on a random blank tile'''
        blanks = []
        for tile in self.tiles:
            if tile.is_blank():
                blanks.append(tile)
        random.choice(blanks).change_number()

    def sort_tiles(self, tile, blanks):
        '''GameBoard.sort_tiles(tile, blanks)
        sorts self.tiles list'''
        temp = self.tiles.index(tile)
        self.tiles.remove(tile)
        self.tiles.insert(self.tiles.index(blanks[0]), tile)
        self.tiles.remove(blanks[0])
        self.tiles.insert(temp, blanks[0])
        blanks.append(blanks[0])
        blanks.pop(0)

    def combine_tiles(self, tile, rowDiff, colDiff):
        '''Gameboard.combine_tiles(tile, rowDiff, colDiff)
        combines two tile if they are the same
        rowDiff and colDiff depend on the direction the tile movess'''
        for tile2 in self.tiles:
            if tile2.get_coord() == (tile.get_coord()[0] + rowDiff, tile.get_coord()[1] + colDiff):
                if tile.get_number() == tile2.get_number() and not tile.is_blank():
                    tile2.change_number()
                    tile2.switch_justChanged()
                    tile.reset()
                    return True
        return False

    def left(self, event):
        '''GameBoard.left(event)
        moves all numbered tiles to the left'''
        legalMove = False
        for row in range(4):
            blanks = []
            for tile in self.tiles:
                if tile.get_coord()[0] == row:
                        if tile.is_blank():
                            blanks.append(tile)
                        else:
                            if len(blanks) > 0:
                                blanks[0].change_coord((row, tile.get_coord()[1]))
                                tile.change_coord((row, tile.get_coord()[1]-len(blanks)))
                                blanks[0].grid(row=row, \
                                               column=blanks[0].get_coord()[1])
                                tile.grid(row=row, column=tile.get_coord()[1])
                                self.sort_tiles(tile, blanks)
                                self.combine_tiles(tile, 0, -1)
                                legalMove = True
        for tile in self.tiles:
            if not tile.just_changed():
                if not legalMove:
                    legalMove = self.combine_tiles(tile, 0, -1)
                else:
                    self.combine_tiles(tile, 0, -1)
        for tile in reversed(self.tiles):
            if tile.just_changed():
                tile.switch_justChanged()
        if legalMove:
            self.new_number()

    def right(self, event):
        '''GameBoard.right(event)
        moves all numbered tiles to the right'''
        legalMove = False
        for row in range(4):
            blanks = []
            for tile in reversed(self.tiles):
                if tile.get_coord()[0] == row:
                    if tile.is_blank():
                        blanks.append(tile)
                    else:
                        if len(blanks) > 0:
                            blanks[0].change_coord((row, tile.get_coord()[1]))
                            tile.change_coord((row, tile.get_coord()[1]+len(blanks)))
                            blanks[0].grid(row=row, \
                                           column=blanks[0].get_coord()[1])
                            tile.grid(row=row, column=tile.get_coord()[1])
                            self.sort_tiles(tile, blanks)
                            self.combine_tiles(tile, 0, 1)
                            legalMove = True
        for tile in reversed(self.tiles):
            if not tile.just_changed():
                if not legalMove:
                    legalMove = self.combine_tiles(tile, 0, 1)
                else:
                    self.combine_tiles(tile, 0, 1)
        for tile in reversed(self.tiles):
            if tile.just_changed():
                tile.switch_justChanged()
        if legalMove:
            self.new_number()

    def up(self, event):
        '''GameBoard.up(event)
        moves all numbered tiles up'''
        legalMove = False
        for column in range(4):
            blanks = []
            for tile in self.tiles:
                if tile.get_coord()[1] == column:
                    if tile.is_blank():
                        blanks.append(tile)
                    else:
                        if len(blanks) > 0:
                            blanks[0].change_coord((tile.get_coord()[0], column))
                            tile.change_coord((tile.get_coord()[0]-len(blanks), column))
                            blanks[0].grid(row=blanks[0].get_coord()[0], \
                                           column=column)
                            tile.grid(row=tile.get_coord()[0], column=column)
                            self.sort_tiles(tile, blanks)
                            self.combine_tiles(tile, -1, 0)
                            legalMove = True
        for tile in self.tiles:
            if not tile.just_changed():
                if not legalMove:
                    legalMove = self.combine_tiles(tile, -1, 0)
                else:
                    self.combine_tiles(tile, -1, 0)
        for tile in reversed(self.tiles):
            if tile.just_changed():
                tile.switch_justChanged()
        if legalMove:
            self.new_number()

    def down(self, event):
        '''GameBoard.down(event)
        moves all numbered tiles down'''
        legalMove = False
        for column in range(4):
            blanks = []
            for tile in reversed(self.tiles):
                if tile.get_coord()[1] == column:
                    if tile.is_blank():
                        blanks.append(tile)
                    else:
                        if len(blanks) > 0:
                            blanks[0].change_coord((tile.get_coord()[0], column))
                            tile.change_coord((tile.get_coord()[0]+len(blanks), column))
                            blanks[0].grid(row=blanks[0].get_coord()[0], \
                                           column=column)
                            tile.grid(row=tile.get_coord()[0], column=column)
                            self.sort_tiles(tile, blanks)
                            self.combine_tiles(tile, 1, 0)
                            legalMove = True
        for tile in reversed(self.tiles):
            if not tile.just_changed():
                if not legalMove:
                    legalMove = self.combine_tiles(tile, 1, 0)
                else:
                    self.combine_tiles(tile, 1, 0)
        for tile in reversed(self.tiles):
            if tile.just_changed():
                tile.switch_justChanged()
        if legalMove:
            self.new_number()

def play2048():
    root = Tk()
    root.title('2048')
    GameBoard(root)
    root.mainloop()

play2048()
