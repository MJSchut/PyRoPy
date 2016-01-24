__author__ = 'Martijn Schut'

import math
from Point import Point

class Line:
    def __init__(self, x0, y0, x1, y1):
        self.points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        if x0 < x1:
            sx = 1
        else:
            sx = -1

        if y0 < y1:
            sy = 1
        else:
            sy = -1

        err = dx - dy

        while True:
            self.points.append(Point(x0, y0))

            if x0 == x1 and y0 == y1:
                break

            e2 = err * 2
            if e2 > -dx:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

    def get_points(self):
        return self.points
