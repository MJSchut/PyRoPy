__author__ = 'Martijn Schut'

from Creatures import Creature
from Creatures import Player

from src import constants
from src.ai.CreatureAi import PlayerAi

import random

class CreatureFactory(object):
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def make_player(self):
        player = Player(self.lbt, self.con, self.level)
        player.set_Ai(PlayerAi(player))
        player.set_maxhp(10 + random.randint(0,3))
        player.set_attack(1 + random.randint(0,1))
        player.set_defence(1)
        player.set_name(constants.player_name)
        self.level.add_at_empty_location(player)

        return player

    def make_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.green)
        fungus.set_maxhp(1 + random.randint(0,4))
        fungus.set_attack(2 + random.randint(0,1))
        fungus.set_name('Fungal %s' %constants.random_name())
        self.level.add_at_empty_location(fungus)

        return fungus
