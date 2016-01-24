__author__ = 'Martijn Schut'

from src.world.Tile import WallTile
from src.world.Tile import FloorTile
from src.util.Rect import Rect

import random

class LevelBuilder(object):
    def __init__(self, level_width, level_height):
        self.level_height = level_height
        self.level_width = level_width
        self.map = [[ WallTile() for y in range(0, self.level_height) ] for x in range(0, self.level_width) ]

    def make_dungeon(self):
        room_amnt = random.randint(40, 80)
        room_rects = []

        w = random.randint(4, 10)
        h = random.randint(4, 10)
        x = random.randint(1, self.level_width - 1 - w)
        y = random.randint(1, self.level_height - 1 - h)

        start_room_rect = Rect(x, y, w, h)
        room_rects.append(start_room_rect)

        for x1 in range(start_room_rect.left(), start_room_rect.right()):
            for y1 in range(start_room_rect.bottom(), start_room_rect.top()):

                self.map[x1][y1] = FloorTile()

        for x in range(0, room_amnt):
            w = random.randint(4, 10)
            h = random.randint(4, 10)
            x = random.randint(w, self.level_width - w*2)
            y = random.randint(h, self.level_height - h*2)

            room_rect = Rect(x, y, w, h)
            print room_rect.left(), room_rect.right(), room_rect.bottom(), room_rect.top()

            for x1 in range(room_rect.left(), room_rect.right()):
                for y1 in range(room_rect.bottom(), room_rect.top()):
                    self.map[x1][y1] = FloorTile()

        return self.map

