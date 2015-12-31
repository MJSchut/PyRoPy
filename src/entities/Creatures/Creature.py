__author__ = 'Martijn Schut'

from src.entities.Entity import Entity

class Creature(Entity):
    def __init__ (self, lbt, con, x, y, char, color):
        super(Creature, self).__init__(lbt, con, x, y, char, color)