__author__ = 'Martijn Schut'

from .Creatures import Creature
from .Creatures import Player
from .Limb import *

from src import constants
from src.ai.CreatureAi import PlayerAi
from src.ai.CreatureAi import BloodFungusAi
from src.ai.CreatureAi import FungusAi
from src.ai.CreatureAi import HuskFungusAi
from src.ai.CreatureAi import BatAi
from src.ai.CreatureAi import SnakeAi
from src.ai.CreatureAi import GargoyleAi
from src.ai.CreatureAi import EOozeAi

from src.effects.Effects import PoisonEffect

import random

class CreatureFactory:
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def _add_human_limbs(self, creature):
        # Add Torso
        torso = creature.add_limb(Torso(creature, None))
        ruarm = creature.add_limb(UpperArm(creature, torso, 'right upper arm'))
        rlarm = creature.add_limb(LowerArm(creature, ruarm, 'right lower arm'))
        creature.add_limb(Hand(creature, rlarm, 'right hand'))

        luarm = creature.add_limb(UpperArm(creature, torso, 'left upper arm'))
        llarm = creature.add_limb(LowerArm(creature, luarm, 'left lower arm'))
        creature.add_limb(Hand(creature, llarm, 'left hand'))

        # Neck, Head
        neck = creature.add_limb(Neck(creature, torso))
        creature.add_limb(Head(creature, neck))

        # Upper legs, Lower legs, Feet
        ruleg = creature.add_limb(UpperLeg(creature, torso, 'right upper leg'))
        rlleg = creature.add_limb(LowerLeg(creature, ruleg, 'right lower leg'))
        creature.add_limb(Foot(creature, rlleg, 'right foot'))

        luleg = creature.add_limb(UpperLeg(creature, torso, 'left upper leg'))
        llleg = creature.add_limb(LowerLeg(creature, luleg, 'left lower leg'))
        creature.add_limb(Foot(creature, llleg, 'left foot'))

    def make_player(self, messages):
        player = Player(self.lbt, self.con, self.level)
        player.set_maxhp(100)
        player.set_maxhunger(100)
        player.set_hunger(100)
        player.set_attack(5)
        player.set_defence(2)
        player.set_vision_radius(9)
        player.set_inventory_size(20)

        self._add_human_limbs(player)

        player.type = 'player'
        player.messages = messages
        player.set_Ai(PlayerAi(player, messages, self.level))

        self.level.add_at_empty_location(player)

        return player

    def make_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', (0, 255, 0))
        fungus.set_maxhp(10)
        fungus.set_attack(0)
        fungus.set_defence(0)
        fungus.set_vision_radius(0)
        fungus.set_inventory_size(0)

        fungus.blood_color = (0, 191, 0)  # Dark green
        fungus.type = 'fungus'

        fungus.set_Ai(FungusAi(fungus, self))

        self.level.add_at_empty_location(fungus)

        return fungus

    def make_blood_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', (255, 0, 0))
        fungus.set_maxhp(10)
        fungus.set_attack(0)
        fungus.set_defence(0)
        fungus.set_vision_radius(0)
        fungus.set_inventory_size(0)

        fungus.blood_color = (191, 0, 0)  # Dark red
        fungus.type = 'blood fungus'

        fungus.set_Ai(BloodFungusAi(fungus))

        self.level.add_creature_at(fungus, self.level.get_random_walkable_tile())

        return fungus

    def make_husk_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.dark_cyan)
        fungus.set_Ai(HuskFungusAi(fungus, self.level))
        fungus.set_maxhp(60 + random.randint(0,5))
        fungus.set_attack(1 + random.randint(0,1))
        fungus.set_name('Husky Fungus known as %s' %constants.random_name())
        fungus.set_type('husk fungus')
        fungus.set_taste('like smoke')
        self.level.add_at_empty_location(fungus)

        return fungus

    def make_bat(self):
        bat = Creature(self.lbt, self.con, self.level, 'b', (191, 95, 0))  # Dark orange
        bat.set_maxhp(3)
        bat.set_attack(2)
        bat.set_defence(0)
        bat.set_vision_radius(5)
        bat.set_inventory_size(0)

        bat.blood_color = (255, 0, 0)  # Red
        bat.type = 'bat'

        bat.set_Ai(BatAi(bat))

        self.level.add_at_empty_location(bat)

        return bat

    def make_snake(self):
        snake = Creature(self.lbt, self.con, self.level, 's', (0, 191, 0))  # Dark green
        snake.set_maxhp(4)
        snake.set_attack(3)
        snake.set_defence(1)
        snake.set_vision_radius(7)
        snake.set_inventory_size(0)

        snake.blood_color = (255, 0, 0)  # Red
        snake.type = 'snake'

        snake.set_Ai(SnakeAi(snake))

        self.level.add_at_empty_location(snake)

        return snake

    def make_gargoyle(self, player):
        gargoyle = Creature(self.lbt, self.con, self.level, 'G', (127, 127, 127))  # Grey
        gargoyle.set_maxhp(15)
        gargoyle.set_attack(5)
        gargoyle.set_defence(4)
        gargoyle.set_vision_radius(8)
        gargoyle.set_inventory_size(0)

        gargoyle.blood_color = (95, 95, 95)  # Dark grey
        gargoyle.type = 'gargoyle'

        gargoyle.set_Ai(GargoyleAi(gargoyle, player))

        self.level.add_at_empty_location(gargoyle)

        return gargoyle

    def make_eooze(self):
        ooze = Creature(self.lbt, self.con, self.level, 'O', self.lbt.dark_cyan)
        ooze.set_Ai(EOozeAi(ooze, self))
        ooze.set_maxhp(1)
        ooze.set_attack(3)
        ooze.set_vision_radius(1)
        ooze.set_name('Endless Ooze')
        ooze.set_type('eldritch')
        self.level.add_at_empty_location(ooze)
        ooze.blood_color = self.lbt.white

        return ooze