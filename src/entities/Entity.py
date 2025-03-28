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
        self.type = 'No-type Timmy'

    def set_postion(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_name(self, name):
        self.name = name

    def set_type(self, ntype):
        self.type = ntype

    def draw(self, wx, wy):
        self.con.print(wx, wy, self.char, self.color)

    def clear(self):
        self.con.print(self.x, self.y, ' ', (0, 0, 0))