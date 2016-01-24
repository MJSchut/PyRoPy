__author__ = 'Martijn Schut'

import random

class Point:
    def __init__(self,x, y):
        self.x = x
        self.y = y

    def neighbours(self):
        nb = []

        for nx in range(-1, 2):
            for ny in range(-1, 2):
                if nx == 0 and ny == 0:
                    continue

            nb.append(Point(self.x+nx, self.y+ny))

        random.shuffle(nb)

        return nb


