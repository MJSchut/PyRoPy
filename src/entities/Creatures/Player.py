__author__ = 'Martijn Schut'

from src.entities.Creatures.Creature import Creature

class Player(Creature):
    def __init__(self, lbt, con, x, y):
        char = '@'
        color = lbt.white
        super(Player, self).__init__(lbt, con, x, y, char, color)
