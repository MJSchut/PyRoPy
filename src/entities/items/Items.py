__author__ = 'Martijn Schut'

from src.entities.Entity import Entity

class Item(Entity):
    def __init__(self, lbt, con, level, char, color):
        super(Item, self).__init__(lbt, con, level, char, color)

        self.name = 'Unnamed artifact'
        self.nutrition = 0
        self.taste = None

    def get_name(self):
        return self.name

    def set_nutrition(self, value):
        self.nutrition = value

    def set_taste(self, taste):
        self.taste = taste


