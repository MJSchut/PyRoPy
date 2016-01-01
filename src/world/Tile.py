__author__ = 'Martijn Schut'

from src import constants
from src.entities.Entity import Entity

class Tile(Entity):
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.char = None
        self.front_color = None
        if self.blocked:
            self.color = constants.colors['wall_color']
        else:
            self.color = constants.colors['floor_color']

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

    def set_color(self, color):
        self.color = color

    def set_front_color(self, color):
        self.front_color = color

    def set_char(self, char):
        self.char = char

class WallTile(Tile):
    def __init__(self):
        super(WallTile, self).__init__(True)
        self.set_color(constants.colors['wall_color'])
        self.set_front_color(constants.colors['wall_color_front'])
        self.set_char(constants.chars['wall_char'])

class FloorTile(Tile):
    def __init__(self):
        super(FloorTile, self).__init__(False)
        self.set_color(constants.colors['floor_color'])
        self.set_char(constants.chars['floor_char'])
        self.set_front_color(constants.colors['floor_color_front'])

class Darkness(Tile):
    def __init__(self):
        super(Darkness, self).__init__(False, block_sight = True)
        self.set_color(constants.colors['darkness_color'])
        self.set_char(constants.chars['darkness_char'])

