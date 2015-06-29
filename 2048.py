"""
A simple clone of the popular game 2048.
Implemented in Python 2. Can be run in any
web browser - visit www.codeskulptor.org to 
view, edit, run & play the game as you like.
"""

import poc_2048_gui
import random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    temp_line = []
    for element in line:
        if element>0:
            temp_line.append(element)
    num_zeros = len(line)-len(temp_line)
    temp_line.extend([0]*num_zeros)
    
    counter_k = 0
    while counter_k < len(temp_line) - 1:
        if (temp_line[counter_k] == temp_line[counter_k+1]):
            temp_line[counter_k] *= 2
            temp_line[counter_k+1] = 0
        counter_k += 1
    
    new_line = []
    for element in temp_line:
        if element>0:
            new_line.append(element)
    num_zeros = len(temp_line)-len(new_line)
    new_line.extend([0]*num_zeros)  
    
    
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Initialise the game.
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        
        downrows = range(grid_height)
        uprows = range(grid_height)
        downrows.reverse()

        rightcols = range(grid_width)
        leftcols = range(grid_width)
        rightcols.reverse()

        up_lines = [[(dummy_i,dummy_j) for dummy_i in uprows]
                                       for dummy_j in leftcols]
        down_lines = [[(dummy_i,dummy_j) for dummy_i in downrows]
                                       for dummy_j in leftcols]
        left_lines = [[(dummy_i,dummy_j) for dummy_j in leftcols]
                                       for dummy_i in uprows]
        right_lines = [[(dummy_i,dummy_j) for dummy_j in rightcols]
                                       for dummy_i in uprows]

        self._indices = {1:up_lines,
                         2:down_lines,
                         3:left_lines,
                         4:right_lines}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)] 
                         for dummy_row in range(self._grid_height)]
        self._empties = [(x_coord,y_coord) for y_coord in range(0,self._grid_width) 
                                           for x_coord in range(0,self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""
        for row in self._grid:
            string += str(row)+"\n"
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tempgrid = list(list(self._grid[dummy_i]) for dummy_i in range(len(self._grid)))
        for dummy_i in range(len(self._indices[direction])):
            indices = self._indices[direction][dummy_i]
            line = merge([self._grid[row][col] for (row,col) in self._indices[direction][dummy_i]])
            for dummy_j in range(len(line)):
                self._grid[indices[dummy_j][0]][indices[dummy_j][1]] = line[dummy_j]
        self._empties = []
        for dummy_i in range(self._grid_height):
            self._empties.extend([(dummy_i,dummy_j) for dummy_j, dummy_e in enumerate(self._grid[dummy_i]) if dummy_e == 0])
        if self._grid != tempgrid:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if len(self._empties)>0:
            tile_location = random.choice(self._empties)
            self._empties.remove(tile_location)
            self._grid[tile_location[0]][tile_location[1]] = random.choice([2]*9+[4])

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value
        if value == 0:
            if (row,col) not in self._empties:
                self._empties.append((row,col))

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
    

