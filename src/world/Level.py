__author__ = 'Martijn Schut'

from src import constants
from src.world.Tile import FloorTile
from src.world.Tile import WallTile

import random

class Level(object):
    def __init__(self, level_width, level_height):
        #  make a list of creatures
        self.creatures = []

        # instantiate the map
        self.level_width = level_width
        self.level_height = level_height
        self.map = [[ FloorTile()
        for y in range(0, level_height) ]
            for x in range(0, level_width) ]

        # add some barriers around the outskirts of the map
        for x in range(0, level_width):
            self.map[x][0] = WallTile()
            self.map[x][level_height-1] = WallTile()

        for y in range(0, level_height):
            self.map[0][y] = WallTile()
            self.map[level_width-1][y] = WallTile()

        # add some random noise to spice things up
        randomblocks = (level_height * level_width / 20)
        for i in range(randomblocks):
            rx = random.randint(1, level_width-1)
            ry = random.randint(1, level_height-1)
            self.map[rx][ry] = WallTile()

    def check_for_creatures(self, x, y):
        for creature in self.creatures:
            if creature.x == x and creature.y == y:
                return creature
        return None

    def remove(self, creature):
        self.creatures.remove(creature)

    def add_at_empty_location(self, entity):
        x = random.randint(1, constants.MAP_WIDTH - 1)
        y = random.randint(1, constants.MAP_HEIGHT - 1)

        while self.map[x][y].blocked or self.check_for_creatures(x,y) is not None:
            x = random.randint(1, constants.MAP_WIDTH - 1)
            y = random.randint(1, constants.MAP_HEIGHT - 1)

        entity.x = x
        entity.y = y

        # TODO: make specific for creatures
        self.creatures.append(entity)
