__author__ = 'Martijn Schut'

class Entity(object):
    def __init__(self, lbt, con, level, char, color):
        self.lbt = lbt
        self.con = con
        self.x = 0
        self.y = 0
        self.char = char
        self.level = level
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


    def draw(self, wx, wy):
        self.lbt.console_set_default_foreground(self.con, self.color)
        self.lbt.console_put_char(self.con, wx, wy, self.char, self.lbt.BKGND_NONE)

    def clear(self):
        self.lbt.console_put_char(self.con, self.x, self.y, ' ', self.lbt.BKGND_NONE)