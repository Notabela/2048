"""
An Implementation of the 2048 game
"""
from random import randrange
from numpy import array_equal
from Tile import *

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    :param line: list()
    :return: merged row or col list for 2048 game
    """

    length = len(line)

    # Slide all non-zeroes to the right
    result_list = [val for val in line if val > 0]
    result_list += [Tile(0)] * (length - len(result_list))

    # Merge all numbers possible and slide while merging
    for index in range(1, length):
        if result_list[index-1] == result_list[index]:
            result_list[index-1] += result_list[index]
            result_list[index] = Tile(0)

            # Slide all zeroes to right
            for index_2 in range(index+1, length):
                temp = result_list[index_2-1]
                result_list[index_2-1] = result_list[index_2]
                result_list[index_2] = temp

    return result_list


class TwentyFortyEight:
    """
    A 2048 Game Class
    """

    def __init__(self, grid_height, grid_width):
        """
        Initializer
        """
        self._grid_height = grid_height
        self._grid_width = grid_width

        self.grid = [[]]
        self.old_grid = {"grid": [[]], "move": None}

        self.new_tiles = []

        # Compute indices of initial tiles
        _up = [(0, col) for col in range(0, grid_width)]
        down = [(grid_height - 1, col) for col in range(0, grid_width)]
        left = [(row, 0) for row in range(0, grid_height)]
        right = [(col, grid_width - 1) for col in range(0, grid_height)]

        # Dictionary of tiles
        self._move_dict = {UP: _up, DOWN: down, LEFT: left, RIGHT: right}

        # Dictionary specificing num_steps for offsett
        self._steps_dict = {1: self._grid_height, 2: self._grid_height, 3: self._grid_width, 4: self._grid_width}

        # init board and I get the row and cols of the new tiles inserted
        self.reset()

    def reset(self):
        """
        Create a new empty board with 2 tiles and init for gameplay
        """
        self.grid = [[Tile(0, row, col) for col in range(self._grid_width)] for row in range(self._grid_height)]

        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Print version of the game
        """
        return str(self.grid)

    def new_tile(self):
        """
        Inserts a new tile to a 0 box of grid if any and return the
        """

        #Check if there is zero in grid
        zero = True if 0 in [num for row in self.grid for num in row] else False
        if not zero:
            return

        # recursive function to return a zero row and col
        def get_rand():
            """
            :return: A random row and col of the new tile
            """
            row_ = randrange(0, self._grid_height)
            col_ = randrange(0, self._grid_width)

            if self.grid[row_][col_] == 0:
                return row_, col_
            else:
                return get_rand()

        # Get row and col from function
        (row, col) = get_rand()

        # Add new tile to the board with 90% chance of 2 and 10% chance of 4
        self.grid[row][col] = Tile(4, row, col) if randrange(1, 11) == 10 else Tile(2, row, col)

        # return the coordinate of the tile
        self.new_tiles.append((row, col))

    def get_grid_height(self):
        """
        Returns height of grid
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Returns height of grid
        """
        return self._grid_width

    def set_tile(self, row, col, tile):
        """
        :param row: int
        :param col: int
        :param tile: Tile
        :return: void
        sets value at grid[row][col] to value
        """
        self.grid[row][col] = tile

    def get_tile(self, row, col):
        """
        Gets a tile at row col
        """
        return self.grid[row][col]

    def check_game_over(self):
        test_grid = [[i for i in j] for j in self.grid]
        test_game_class = self.__class__(len(test_grid), len(test_grid[0]))
        test_game_class.grid = [[i for i in j] for j in self.grid]

        directions = [UP, DOWN, LEFT, RIGHT]

        for direction in directions:
            test_game_class.move(direction)
            for i, _ in enumerate(test_grid):
                    if not array_equal(test_grid[i], test_game_class.grid[i]):
                        return False
        else:
            return True

    def move(self, direction):
        """
        Get list of numbers in move direction - returns the row and col of the new tile inserted
        """
        # store old grid before altering
        self.old_grid["grid"] = [[i for i in j] for j in self.grid]
        self.old_grid["move"] = direction

        # Create a temporary move_list to be passed to merge
        def make_move_list(start_cell, direc, num_steps):
            """
            :param start_cell: Beginning cell
            :param direc:  Direction to move in
            :param num_steps: Number of steps
            :return: Returns a tuple with grid list and indexes
            """
            move = []
            indexes = []
            for step in range(num_steps):
                row_ = start_cell[0] + step * direc[0]
                col_ = start_cell[1] + step * direc[1]
                indexes.append((row_, col_))
                move.append(self.grid[row_][col_])

            return move, indexes

        tiles = self._move_dict[direction]
        steps = self._steps_dict[direction]
        offset = OFFSETS[direction]

        changed = False

        for start_tile in tiles:
            (move_list, indices) = make_move_list(start_tile, offset, steps)
            updated_line = merge(move_list)

            for index, (row, col) in enumerate(indices):
                if self.grid[row][col] != updated_line[index]:
                    changed = True
                self.grid[row][col] = updated_line[index]

        if changed:
            return self.new_tile()