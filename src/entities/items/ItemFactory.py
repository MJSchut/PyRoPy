__author__ = 'Martijn Schut'

from Items import Item

import random

class ItemFactory(object):
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def make_rock(self):
        rock = Item(self.lbt, self.con, self.level, ',', self.lbt.yellow)
        if random.random() < 0.5:
            rock.set_name('rock')
        else:
            rock.set_name('stone')
        self.level.add_at_empty_location(rock)

        return rock
