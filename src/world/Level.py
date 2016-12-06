__author__ = 'Martijn Schut'

# TODO add decal, splatters of blood, etc.

from src import constants
from src.constants import debug_msg
from src.entities.creatures.Creatures import Creature
from src.entities.creatures.Creatures import Player
from src.entities.items.Items import Item
from src.world.Tile import FloorTile
from src.world.Tile import WallTile
from src.world.LevelBuilder import LevelBuilder

import random

class Level(object):
    def __init__(self, level_width, level_height):
        #  make a list of creatures & items
        self.creatures = []
        self.items = []

        # instantiate the map
        self.level_width = level_width
        self.level_height = level_height

        self.builder = LevelBuilder(self.level_width, self.level_height)
        self.map = self.builder.dig_cave()

    def check_for_creatures(self, x, y):
        for creature in self.creatures:
            # check for y first, as level height will always be lower than level width
            if creature.y == y:
                    if creature.x == x:
                        return creature
        return None

    def check_for_creatures_in_range(self, cen_x, cen_y, radius, ignore = None):
        creatures_in_range = []

        for creature in self.creatures:
            dif_x = creature.x - cen_x
            dif_y = creature.y - cen_y
            if dif_x ** 2 + dif_y ** 2 <= radius ** 2:
                if creature not in ignore:
                    creatures_in_range.append(creature)

        return creatures_in_range

    def check_for_items(self, x, y):
        for item in self.items:
            # check for y first, as level height will always be lower than level width
            if item.y == y:
                    if item.x == x:
                        return item
        return None

    def check_for_items_in_range(self, cen_x, cen_y, radius, ignore = None):
        items_in_range = []

        for item in self.items:
            dif_x = item.x - cen_x
            dif_y = item.y - cen_y
            if dif_x ** 2 + dif_y ** 2 <= radius ** 2:
                if item not in ignore:
                    items_in_range.append(item)

        return items_in_range

    def get_tile(self, x, y):
        return self.map[x][y]

    def get_random_surrounding_tile(self, x, y):
        nx = random.choice([-1, 0, 1]) + x
        ny = random.choice([-1, 0, 1]) + y

        return self.map[nx][ny]

    def remove_creature(self, creature):
        if creature is not None:
            try:
                self.creatures.remove(creature)
            except:
                debug_msg('Tried to remove_creature creature %s in the creature list, '
                      'but it was not found.' %creature)
        else:
            debug_msg('Tried to remove_creature for %s of Nonetype' %creature)

    def add_item(self, item, x, y):
        self.items.append(item)
        item.x = x
        item.y = y

    def remove_item(self, item):
        if item is not None:
            self.items.remove(item)
        else:
            debug_msg('Tried to remove_creature creature %s in the creature list, '
                      'but it was not found.' %item)

    def space_for_creature(self, x, y):
        if x < 0 or y < 0 or x >= self.level_width or y >= self.level_height:
            return False

        if self.map[x][y].blocked or self.check_for_creatures(x,y) is not None:
            return False
        else:
            return True

    def space_for_item(self, x, y):
        if x < 0 or y < 0 or x >= self.level_width or y >= self.level_height:
            return False

        if self.map[x][y].blocked or self.check_for_items(x, y) is not None:
            return False
        else:
            return True


    def add_at_empty_location(self, entity):
        x = random.randint(2, self.level_width - 2)
        y = random.randint(2, self.level_height - 2)

        while not self.space_for_creature(x, y):
            x = random.randint(2, self.level_width - 2)
            y = random.randint(2, self.level_height - 2)

        entity.x = x
        entity.y = y

        if type(entity) == Creature or type(entity) == Player:
            self.creatures.append(entity)
        if type(entity) == Item:
            self.items.append(entity)

    def update(self):
        # we slice the list (i.e. make a copy) so we don't get stuck in a loop
        # where newly spawned fungus keep being added to the update que and break your computer
        clist = self.creatures[:]
        for creature in clist:
            if creature.ai is not None:
                creature.ai.on_update()
            else:
                self.remove_creature(creature)

