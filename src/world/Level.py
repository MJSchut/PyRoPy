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
            # check for y first, as level height will always be lower than level width
            if creature.y == y:
                    if creature.x == x:
                        return creature
        return None

    def remove(self, creature):
        self.creatures.remove(creature)

    def is_empty(self, x, y):
        if x < 0 or y < 0 or x >= self.level_width or y >= self.level_height:
            return False

        if self.map[x][y].blocked or self.check_for_creatures(x,y) is not None:
            return False
        else:
            return True

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

    def update(self):
        # we slice the list (i.e. make a copy) so we don't get stuck in a loop
        # where newly spawned fungus keep being added to the update que and break your computer
        clist = self.creatures[:]
        for creature in clist:
            creature.ai.on_update()

