__author__ = 'Martijn Schut'

from Creatures import Creature
from Creatures import Player

from src import constants
from src.ai.CreatureAi import PlayerAi
from src.ai.CreatureAi import BloodFungusAi
from src.ai.CreatureAi import FungusAi
from src.ai.CreatureAi import HuskFungusAi
from src.ai.CreatureAi import BatAi

import random

class CreatureFactory(object):
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def make_player(self, messages):
        player = Player(self.lbt, self.con, self.level)
        player.set_Ai(PlayerAi(player, messages))
        player.set_maxhp(10 + random.randint(0,3))
        player.set_attack(1 + random.randint(0,1))
        player.set_defence(1)
        player.set_name(constants.player_name)
        self.level.add_at_empty_location(player)

        return player

    def make_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.green)
        fungus.set_Ai(FungusAi(fungus, self))
        fungus.set_maxhp(1 + random.randint(0,4))
        fungus.set_attack(1 + random.randint(0,1))
        fungus.set_name('Fungal %s' %constants.random_name())
        fungus.set_type('Fungus')
        self.level.add_at_empty_location(fungus)

        return fungus

    def make_blood_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.dark_crimson)
        fungus.set_Ai(BloodFungusAi(fungus, self))
        fungus.set_maxhp(20 + random.randint(0,5))
        fungus.set_attack(10 + random.randint(0,5))
        fungus.set_name('Bloody Fungus named %s' %constants.random_name())
        fungus.set_type('Blood Fungus')
        self.level.add_at_empty_location(fungus)

        return fungus

    def make_husk_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.dark_cyan)
        fungus.set_Ai(HuskFungusAi(fungus, self))
        fungus.set_maxhp(60 + random.randint(0,5))
        fungus.set_attack(1 + random.randint(0,1))
        fungus.set_name('Husky Fungus known as %s' %constants.random_name())
        fungus.set_type('Husk Fungus')
        self.level.add_at_empty_location(fungus)

        return fungus

    def make_bat(self):
        bat = Creature(self.lbt, self.con, self.level, 'b', self.lbt.dark_orange)
        bat.set_Ai(BatAi(bat))
        bat.set_maxhp(2)
        bat.set_attack(random.randint(1,3))
        bat.set_name('Steven')
        bat.set_type('Bat')
        self.level.add_at_empty_location(bat)

        return bat
