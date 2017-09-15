"""
Tile Class representing a 2048 tile
"""


class Tile:

    # Tile with value = 0 is an empty tile
    def __init__(self, value: int, x_cor: int=0, y_cor: int=0):
        self.value = value
        self.x = x_cor
        self.y = y_cor

        # References to tile that formed this
        self.source = None
        self.target = None

    def set_location(self, x_cor: int, y_cor: int):
        self.x = x_cor
        self.y = y_cor

    def __add__(self, other):
        # We should be able to add two tiles of differing values
        if self.value != other.value:
            raise ValueError("Tile values are not equal")

        new_tile = Tile(self.value + other.value)
        # new_tile.set_location(other.value.x, other.value.y)

        # remove self and other's source and targets to save some memory
        self.source = None
        self.target = None
        other.source = None
        other.target = None

        new_tile.source = self
        new_tile.target = other

        return new_tile

    def __repr__(self):
        return str(self.value)