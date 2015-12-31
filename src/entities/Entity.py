__author__ = 'Martijn Schut'

class Entity(object):
    def __init__(self, lbt, con, x, y, char, color):
        self.lbt = lbt
        self.con = con
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = 'No-name Simon'

    def set_name(self, name):
        self.name = name

    def set_postion(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        self.lbt.console_set_default_foreground(self.con, self.color)
        self.lbt.console_put_char(self.con, self.x, self.y, self.char, self.lbt.BKGND_NONE)

    def clear(self):
        self.lbt.console_put_char(self.con, self.x, self.y, ' ', self.lbt.BKGND_NONE)