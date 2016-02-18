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
        rock.set_equip_to_hand()
        rock.set_attack_value(1)
        if random.random() < 0.5:
            rock.set_name('rock')
        else:
            rock.set_name('stone')
        self.level.add_at_empty_location(rock)

        return rock

    def make_sword(self):
        sword = Item(self.lbt, self.con, self.level, '/', self.lbt.white)
        sword.set_equip_to_hand()
        sword.set_name('unremarkable sword')
        sword.set_attack_value(2)
        self.level.add_at_empty_location(sword)

    def make_gauntlet(self):
        glove = Item(self.lbt, self.con, self.level, ']', self.lbt.white)
        glove.set_equip_to_hand(wearable=True)
        glove.set_name('iron gauntlet')
        glove.set_defence_value(1)
        self.level.add_at_empty_location(glove)