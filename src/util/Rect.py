__author__ = 'Martijn Schut'

class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def top(self):
        return self.height + self.y

    def bottom(self):
        return self.y

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def intersects(self, otherrect):
        return (self.left() <= otherrect.right() and self.right() >= otherrect.left() and
                self.bottom() <= otherrect.top() and self.top() >= otherrect.bottom())