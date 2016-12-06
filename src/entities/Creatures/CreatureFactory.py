__author__ = 'Martijn Schut'

from Creatures import Creature
from Creatures import Player
from src.entities.creatures.Limb import *

from src import constants
from src.ai.CreatureAi import PlayerAi
from src.ai.CreatureAi import BloodFungusAi
from src.ai.CreatureAi import FungusAi
from src.ai.CreatureAi import HuskFungusAi
from src.ai.CreatureAi import BatAi
from src.ai.CreatureAi import SnakeAi
from src.ai.CreatureAi import GargoyleAi

from src.effects.Effects import PoisonEffect

import random

class CreatureFactory(object):
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def make_player(self, messages):
        player = Player(self.lbt, self.con, self.level)
        player.set_Ai(PlayerAi(player, messages, self.level))
        player.set_inventory_size(26)
        player.set_maxhp(90 + random.randint(0,20))
        player.set_attack(3 + random.randint(0,1))
        player.set_maxhunger(1500)
        player.set_defence(0)
        player.set_corpse_nutrition(100)
        player.set_taste('like chicken')
        player.set_vision_radius(11)

        player.set_name(constants.player_name)

        self._add_human_limbs(player)

        self.level.add_at_empty_location(player)

        return player

    def _add_human_limbs(self, creature):
        # Add Torso
        torso = creature.add_limb(Torso(creature, None))
        # Upper Arms, Lower Arms, Hands
        print torso
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

    def make_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.green)
        fungus.set_Ai(FungusAi(fungus, self))
        fungus.set_maxhp(1 + random.randint(0,4))
        fungus.set_attack(1 + random.randint(0,1))
        fungus.set_name('Fungal %s' %constants.random_name())
        fungus.set_type('fungus')
        fungus.set_corpse_nutrition(1)
        fungus.set_taste('grassy')
        fungus.blood_color = self.lbt.dark_green
        self.level.add_at_empty_location(fungus)

        return fungus

    def make_blood_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', self.lbt.dark_crimson)
        fungus.set_Ai(BloodFungusAi(fungus, self))
        fungus.set_maxhp(20 + random.randint(0,5))
        fungus.set_attack(10 + random.randint(0,5))
        fungus.set_name('Bloody Fungus named %s' %constants.random_name())
        fungus.set_type('blood fungus')
        fungus.set_corpse_nutrition(-10)
        fungus.set_taste('like licking pennies')
        self.level.add_at_empty_location(fungus)

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

    # TODO add hunger and food for bat
    def make_bat(self):
        bat = Creature(self.lbt, self.con, self.level, 'b', self.lbt.dark_orange)
        bat.set_Ai(BatAi(bat))
        bat.set_maxhp(2)
        bat.set_attack(random.randint(1,3))
        bat.set_name('Steven')
        bat.set_type('bat')
        bat.set_corpse_nutrition(20)
        bat.set_taste('like old shoes')
        self.level.add_at_empty_location(bat)

        return bat

    # TODO add hunger and feeding system for snake
    def make_snake(self):
        snake = Creature(self.lbt, self.con, self.level, 's', self.lbt.dark_green)
        snake.set_attack_effect(PoisonEffect)
        snake.set_attack_effect_duration(5)
        snake.set_Ai(SnakeAi(snake))
        snake.set_maxhp(2)
        snake.set_attack(1)
        snake.set_name('Slithery %s' %constants.random_name())
        snake.set_corpse_nutrition(50)
        snake.set_taste('pretty great')
        snake.set_type('snake')

        self.level.add_at_empty_location(snake)

        return snake

    def make_gargoyle(self, player):
        gargoyle = Creature(self.lbt, self.con, self.level, 'G', self.lbt.grey)
        gargoyle.set_Ai(GargoyleAi(gargoyle, player))
        gargoyle.set_maxhp(10)
        gargoyle.set_attack(3)
        gargoyle.set_vision_radius(3)
        if random.random <= 0.5:
            gargoyle.set_name('Rock-solid %s' %constants.random_name())
        else:
            gargoyle.set_name('Statuesque %s' %constants.random_name())
        gargoyle.set_type('gargoyle')
        self.level.add_at_empty_location(gargoyle)
        gargoyle.blood_color = self.lbt.dark_grey

        return gargoyle
