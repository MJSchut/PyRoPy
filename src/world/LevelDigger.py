__author__ = 'Martijn Schut'

import random
import numpy as np

from src.world.Tile import WallTile
from src.world.Tile import FloorTile

class LevelDigger(object):
    def __init__(self, map, x, y):
        self.map = map
        self.x = x
        self.y = y


    def check_for_walls(self):
        if type(self.map[self.x][self.y] == WallTile):
            return [self.x, self.y]

        tiles_check = [[self.x - 1, self.y - 1],
                       [self.x, self.y - 1],
                       [self.x + 1, self.y - 1],
                       [self.x - 1, self.y],
                       [self.x + 1, self.y],
                       [self.x - 1, self.y + 1],
                       [self.x, self.y + 1],
                       [self.x + 1, self.y + 1]]

        np.random.shuffle(tiles_check)

        for coords in tiles_check:
            if type(self.map[coords[0]][coords[1]] == WallTile):
                return [self.x, self.y]

        return None

    def dig(self, coords):
        if coords is not None:
            self.map[coords[0]][coords[1]] = FloorTile()

    def move(self):
        dx = random.choice([-1,0,1])
        dy = random.choice([-1,0,1])

        if 1 < self.x < len(self.map) - 2 and 1 < self.y < len(self.map[0]) - 2:
            self.x += dx
            self.y += dy