__author__ = 'Martijn Schut'

from src.world.Tile import WallTile
from src.world.Tile import FloorTile
from src.util.Rect import Rect
from src.world.LevelDigger import LevelDigger

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

            for x1 in range(room_rect.left(), room_rect.right()):
                for y1 in range(room_rect.bottom(), room_rect.top()):
                    self.map[x1][y1] = FloorTile()

        return self.map

    def dig_cave(self):
        steps = 0
        max_step = 1500
        digger_count = 0
        max_digger = 19
        digger_list = []
        # I seriously regret calling these things diggers. I have to double check for typos all the time now.
        # Especially when I start killing diggers randomly.
        digger_list.append(LevelDigger(self.map, int(round(self.level_width)/2), int(round(self.level_height)/2)))

        while steps < max_step:
            for x in range(0, len(digger_list)):
                digger = digger_list[x]
                coords = digger.check_for_walls()

                if coords is not None:
                    digger.dig(coords)
                    digger.move()
                    if random.random() < 0.05 and len(digger_list) < max_digger:
                        nx = digger.x + random.choice([-1, 1])
                        ny = digger.y + random.choice([-1, 1])
                        if 0 < nx < self.level_width - 1 and 0 < ny < self.level_height - 1:
                            ndigger = LevelDigger(self.map, nx, ny)
                            digger_list.append(ndigger)
                            digger_count += 1

                else:
                    if len(digger_list) > 1:
                        digger_list.remove(digger)
                        continue
                    else:
                        if random.random < 0.5:
                            nx = digger.x + random.choice([-1, 1])
                            ny = digger.y + random.choice([-1, 1])
                            if 0 < nx < self.level_width - 1 and 0 < ny < self.level_height - 1:
                                ndigger = LevelDigger(self.map, nx, ny)
                                digger_list.append(ndigger)
                                digger_count += 1
            steps += 1

        return self.map

